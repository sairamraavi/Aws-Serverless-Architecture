import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

# Replace with your EBS Volume ID
VOLUME_ID = 'vol-0a90dd3c5f467cd39'

def lambda_handler(event, context):

    created_snapshots = []
    deleted_snapshots = []

    # Create Snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated Backup Snapshot'
    )

    snapshot_id = snapshot['SnapshotId']
    created_snapshots.append(snapshot_id)

    print(f"Created Snapshot: {snapshot_id}")

    # Find snapshots older than 30 days
    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )['Snapshots']

    retention_date = datetime.now(timezone.utc) - timedelta(days=30)

    for snap in snapshots:

        if snap['StartTime'] < retention_date:

            snap_id = snap['SnapshotId']

            try:
                ec2.delete_snapshot(
                    SnapshotId=snap_id
                )

                deleted_snapshots.append(snap_id)

                print(f"Deleted Snapshot: {snap_id}")

            except Exception as e:
                print(f"Unable to delete {snap_id}: {str(e)}")

    return {
        'statusCode': 200,
        'created_snapshots': created_snapshots,
        'deleted_snapshots': deleted_snapshots
    }