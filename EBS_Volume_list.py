import boto3
import openpyxl

# AWS credentials
aws_access_key = ""
aws_secret_key = ""
region_name = "ap-south-1"  # Update with your desired region

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2', region_name=region_name,
                         aws_access_key_id=aws_access_key,
                         aws_secret_access_key=aws_secret_key)

# Fetch EBS volume details
volumes = ec2_client.describe_volumes()
instances = ec2_client.describe_instances()

# Create an Excel workbook and add a sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "EBS Volumes"

# Add headers
headers = ["Volume ID", "Volume Name", "Size (GiB)", "Volume Type", "State", "Attachment State",
           "Attached To", "Creation Time"]
sheet.append(headers)

# Iterate through volumes and populate the sheet
for instance in reservation['Instances']:
        instance_id = instance["InstanceId"]

for volume in volumes['Volumes']:
    volume_id = volume['VolumeId']
    volume_name = None
    for tag in volume.get('Tags', []):
        if tag['Key'] == 'Name':
            volume_name = tag['Value']
            break

    size = volume['Size']
    volume_type = volume['VolumeType']
    state = volume['State']
    
    attachment_state = "Not Attached"
    attached_to = "N/A"
    if volume.get('Attachments'):
        attachment = volume['Attachments'][0]
        attachment_state = attachment['State']
        attached_to = attachment.get('InstanceId', 'N/A')
    
    creation_time = volume['CreateTime']
    
    volume_details = [volume_id, volume_name, size, volume_type, state, attachment_state,
                      attached_to, creation_time.strftime('%Y-%m-%d %H:%M:%S')]
    sheet.append(volume_details)

# Save the workbook
output_filename = "EBS_Volume_Details.xlsx"
workbook.save(output_filename)
print(f"Excel file '{output_filename}' created successfully.")
