import boto3
import os
import json

# Creating a new IAM role and attach policy
iam = boto3.client("iam")

iam_role = iam.create_role(
    Path="/",
    RoleName="string",
    AssumeRolePolicyDocument=json.dump(
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
    Description="Allows Redshift clusters to call AWS services on your behalf",
)

iam.attach_role_policy(
    RoleName="string", PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
)["ResponseMetadata"]["HTTPStatusCode"]

# open an incoming TCP port to access the cluster
ec2 = boto3.resource("ec2")
vpc = ec2.Vpc("id")
default_sg = list(vpc.security_groups.all())[0]
response = default_sg.authorize_ingress(
    CidrIp="0.0.0.0/0", FromPort=123, GroupName=default_sg.group_name, IpProtocol="TCP",
)

# Creating Redshift cluster
redshift = boto3.client(
    "redshift",
    region_name="us-west-2",
    aws_access_key=os.environ.get("REDSHIFT_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("REDSHIFT_ACCESS_SECRET"),
)

response = redshift.create_cluster(
    # DWH
    ClusterType="",
    NodeType="",
    NumberOfNodes=int(2),
    # identifiers and credentials
    DBName="string",
    ClusterIdentifier="string",
    MasterUsername=os.environ.get("REDSHIFT_DB_USER"),
    MasterUserPassword=os.environ.get("REDSHIFT_DB_PASSWORD"),
    # roles
    IamRoles=["string",],
    ClusterSecurityGroups=["string",],
    VpcSecurityGroupIds=["string",],
)
