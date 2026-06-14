import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'sairam-s3-cleanup-bucket-175200623108-ap-south-1-an'

def lambda_handler(event, context):

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    deleted_files = []

    if 'Contents' in response:

        for obj in response['Contents']:

            file_name = obj['Key']
            last_modified = obj['LastModified']

            # Assignment demo:
            # Treat files older than 30 minutes as old

            if last_modified < datetime.now(timezone.utc) - timedelta(minutes=30):

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=file_name
                )

                deleted_files.append(file_name)

                print(f"Deleted: {file_name}")

    return {
        'statusCode': 200,
        'deleted_files': deleted_files
    }