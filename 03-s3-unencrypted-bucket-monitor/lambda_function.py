import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):

    buckets = s3.list_buckets()

    encryption_report = {}

    for bucket in buckets['Buckets']:

        bucket_name = bucket['Name']

        try:
            response = s3.get_bucket_encryption(
                Bucket=bucket_name
            )

            encryption_type = response[
                'ServerSideEncryptionConfiguration'
            ]['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']

            encryption_report[bucket_name] = encryption_type

            print(f"{bucket_name} -> {encryption_type}")

        except ClientError:

            encryption_report[bucket_name] = "No Encryption"

            print(f"{bucket_name} -> No Encryption")

    return {
        "statusCode": 200,
        "encryption_report": encryption_report
    }