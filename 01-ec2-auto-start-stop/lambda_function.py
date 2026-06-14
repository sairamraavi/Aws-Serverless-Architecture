import boto3
ec2 = boto3.client('ec2')
def lambda_handler(event, context):
    # Checking for Auto-Stop instances 
    stop_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            }
        ]
    )
    stop_ids = []
    for reservation in stop_instances['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped Instances: {stop_ids}")

    # Checking for Auto-Start instances
    start_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            }
        ]
    )

    start_ids = []

    for reservation in start_instances['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started Instances: {start_ids}")

    return {
        'statusCode': 200,
        'body': {
            'stopped': stop_ids,
            'started': start_ids
        }
    }