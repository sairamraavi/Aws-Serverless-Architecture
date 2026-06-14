import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    instance_id = event['detail']['instance-id']

    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                'Key': 'LaunchDate',
                'Value': current_date
            },
            {
                'Key': 'Environment',
                'Value': 'Assignment5'
            }
        ]
    )

    print(f"Successfully tagged instance: {instance_id}")

    return {
        'statusCode': 200,
        'body': f'Tagged {instance_id}'
    }
