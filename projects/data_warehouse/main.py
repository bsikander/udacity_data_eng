import sys
import logging


def main(run_test: bool = False, refresh_database: bool = False):
    pass


if __name__ == "__main__":
    args = sys.argv[1:]
    refresh_database = "--refresh" in args
    if refresh_database:
        logger.info(f"running with a fresh database")

    main(refresh_database=refresh_database)
