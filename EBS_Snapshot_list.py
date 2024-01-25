import boto3
import openpyxl

# AWS credentials
aws_access_key = ""
aws_secret_key = ""
region_name = "us-east-1"  # Update with your desired region

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2', region_name=region_name,
                         aws_access_key_id=aws_access_key,
                         aws_secret_access_key=aws_secret_key)

# Fetch Snapshot details
snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])

# Create an Excel workbook and add a sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "EBS Snapshots"

# Add headers
headers = ["Snapshot ID", "Snapshot Name", "Volume ID", "Volume Size (GiB)",
           "State", "Progress", "Description", "Start Time"]
sheet.append(headers)

# Iterate through snapshots and populate the sheet
for snapshot in snapshots['Snapshots']:
    snapshot_id = snapshot['SnapshotId']
    snapshot_name = None
    for tag in snapshot.get('Tags', []):
        if tag['Key'] == 'Name':
            snapshot_name = tag['Value']
            break
    
    volume_id = snapshot['VolumeId']
    volume_size_gib = snapshot['VolumeSize']
    state = snapshot['State']
    progress = snapshot.get('Progress', 'N/A')
    description = snapshot.get('Description', 'N/A')
    start_time = snapshot['StartTime'].strftime('%Y-%m-%d %H:%M:%S')
    
    snapshot_details = [snapshot_id, snapshot_name, volume_id, volume_size_gib,
                        state, progress, description, start_time]
    sheet.append(snapshot_details)

# Save the workbook
output_filename = "EBS_Snapshot_Details.xlsx"
workbook.save(output_filename)
print(f"Excel file '{output_filename}' created successfully.")
