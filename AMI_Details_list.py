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

# Fetch AMI details
amis = ec2_client.describe_images(Owners=['self'])

# Create an Excel workbook and add a sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "AMIs"

# Add headers
headers = ["Image ID", "Image Name", "Description", "Architecture",
           "Root Device Type", "Creation Date"]
sheet.append(headers)

# Iterate through AMIs and populate the sheet
for ami in amis['Images']:
    image_id = ami['ImageId']
    image_name = None
    for tag in ami.get('Tags', []):
        if tag['Key'] == 'Name':
            image_name = tag['Value']
            break
    
    description = ami.get('Description', 'N/A')
    architecture = ami['Architecture']
    root_device_type = ami['RootDeviceType']
    creation_date = ami['CreationDate']
    
    ami_details = [image_id, image_name, description, architecture,
                   root_device_type, creation_date]
    sheet.append(ami_details)

# Save the workbook
output_filename = "AMI_Details.xlsx"
workbook.save(output_filename)
print(f"Excel file '{output_filename}' created successfully.")
