import boto3
from botocore.exceptions import ClientError
import configparser
import json
import pandas as pd

config = configparser.ConfigParser()
config.read_file(open("dwh.cfg"))

# Step 0: Make sure you have an AWS secret and access key
# - Create a new IAM user in your AWS account
# - Give it AdministratorAccess, From Attach existing policies directly Tab
# - Take note of the access key and secret
# - Edit the file dwh.cfg in the same folder as this notebook and fill

KEY = config.get("AWS", "KEY")
SECRET = config.get("AWS", "SECRET")

DWH_CLUSTER_TYPE = config.get("DWH", "DWH_CLUSTER_TYPE")
DWH_NUM_NODES = config.get("DWH", "DWH_NUM_NODES")
DWH_NODE_TYPE = config.get("DWH", "DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER = config.get("DWH", "DWH_CLUSTER_IDENTIFIER")
DWH_DB = config.get("DWH", "DWH_DB")
DWH_DB_USER = config.get("DWH", "DWH_DB_USER")
DWH_DB_PASSWORD = config.get("DWH", "DWH_DB_PASSWORD")
DWH_PORT = config.get("DWH", "DWH_PORT")

DWH_IAM_ROLE_NAME = config.get("DWH", "DWH_IAM_ROLE_NAME")

(DWH_DB_USER, DWH_DB_PASSWORD, DWH_DB)

pd.DataFrame(
    {
        "Param": [
            "DWH_CLUSTER_TYPE",
            "DWH_NUM_NODES",
            "DWH_NODE_TYPE",
            "DWH_CLUSTER_IDENTIFIER",
            "DWH_DB",
            "DWH_DB_USER",
            "DWH_DB_PASSWORD",
            "DWH_PORT",
            "DWH_IAM_ROLE_NAME",
        ],
        "Value": [
            DWH_CLUSTER_TYPE,
            DWH_NUM_NODES,
            DWH_NODE_TYPE,
            DWH_CLUSTER_IDENTIFIER,
            DWH_DB,
            DWH_DB_USER,
            DWH_DB_PASSWORD,
            DWH_PORT,
            DWH_IAM_ROLE_NAME,
        ],
    }
)

# create clients
ec2 = boto3.resource(
    "ec2", region_name="us-west-2", aws_access_key_id=KEY, aws_secret_access_key=SECRET
)

s3 = boto3.resource(
    "s3", region_name="us-west-2", aws_access_key_id=KEY, aws_secret_access_key=SECRET
)

iam = boto3.client(
    "iam", aws_access_key_id=KEY, aws_secret_access_key=SECRET, region_name="us-west-2"
)

redshift = boto3.client(
    "redshift",
    region_name="us-west-2",
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET,
)


# check out sample data resources in s3
sampleDbBucket = s3.Bucket("awssampledbuswest2")

for obj in sampleDbBucket.objects.filter(Prefix="ssbgz"):
    print(obj)

for obj in sampleDbBucket.objects.all():
    print(obj)

# Step 1: create IAM role
try:
    print("Creating a new IAM Role...")
    dwhRole = iam.create_role(
        Path="/",
        RoleName=DWH_IAM_ROLE_NAME,
        Description="Allows Redshift clusters to call AWS services on your behalf.",
        AssumeRolePolicyDocument=json.dumps(
            {
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {"Service": "redshift.amazonaws.com"},
                    }
                ],
                "Version": "2012-10-17",
            }
        ),
    )
except Exception as e:
    print(e)

print("Attaching Policy...")
iam.attach_role_policy(
    RoleName=DWH_IAM_ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
)["ResponseMetadata"]["HTTPStatusCode"]

print("Getting the IAM role ARN...")
role_arn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)["Role"]["Arn"]
print(role_arn)

# Step 2: create Redshift cluster
try:
    response = redshift.create_cluster(
        # HW
        ClusterType=DWH_CLUSTER_TYPE,
        NodeType=DWH_NODE_TYPE,
        NumberOfNodes=int(DWH_NUM_NODES),
        # Identifiers & Credentials
        DBName=DWH_DB,
        ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
        MasterUsername=DWH_DB_USER,
        MasterUserPassword=DWH_DB_PASSWORD,
        # Roles (for s3 access)
        IamRoles=[role_arn],
    )
except Exception as e:
    print(e)

# describe the cluster to see its status
def prettyRedshiftProps(props):
    pd.set_option("display.max_colwidth", -1)
    keysToShow = [
        "ClusterIdentifier",
        "NodeType",
        "ClusterStatus",
        "MasterUsername",
        "DBName",
        "Endpoint",
        "NumberOfNodes",
        "VpcId",
    ]
    x = [(k, v) for k, v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])


cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)[
    "Clusters"
][0]
prettyRedshiftProps(cluster_props)

DWH_ENDPOINT = cluster_props["Endpoint"]["Address"]
DWH_ROLE_ARN = cluster_props["IamRoles"][0]["IamRoleArn"]

# Step 3: open an incoming TCP port to access the cluster endpoint
try:
    vpc = ec2.Vpc(id=cluster_props["VpcId"])
    default_sg = list(vpc.security_groups.all())[0]
    print(default_sg)
    default_sg.authorize_ingress(
        GroupName=default_sg.group_name,
        CidrIp="0.0.0.0/0",
        IpProtocol="TCP",
        FromPort=int(DWH_PORT),
        ToPort=int(DWH_PORT),
    )
except Exception as e:
    print(e)

# make sure you can connect
conn_string = "postgresql://{}:{}@{}:{}/{}".format(
    DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB
)

# Step 5: cleanup
redshift.delete_cluster(
    ClusterIdentifier=DWH_CLUSTER_IDENTIFIER, SkipFinalClusterSnapshot=True
)
# run this block several times until the cluster really deleted
cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)[
    "Clusters"
][0]
prettyRedshiftProps(cluster_props)

iam.detach_role_policy(
    RoleName=DWH_IAM_ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
)
iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
