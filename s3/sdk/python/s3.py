# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

import logging
import os
import boto3
import random
import uuid
from botocore.exceptions import ClientError



bucket_name = os.environ.get('BUCKET_NAME')

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    create_bucket(bucket_name, 'af-south-1')

    number_of_files = random.randrange(0, 6)

    for i in range(number_of_files):
        filename = f"file_{i}.txt"
        output_path = f"/tmp/{filename}"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(uuid.uuid4()))

        s3_client = boto3.client('s3')
        try:
            resp = s3_client.upload_file(output_path, bucket_name, filename)
        except ClientError as e:
            logging.error(e)
