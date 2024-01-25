import boto3
import openpyxl

# AWS credentials
aws_access_key = ""
aws_secret_key = ""
region_name = "us-east-1"  # Update with your desired region

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2', region_name=region_name, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Fetch EC2 instance details
instances = ec2_client.describe_instances()

# Create an Excel workbook and add a sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "EC2 Instances"

# Add headers
headers = ["instance_id", "instance_name", "instance_type", "instance_state", "Private IP", "Public IP", "Security Group", "VPC ID",
           "Subnet ID", "IAM Role", "Platform", "Key Pair"]
sheet.append(headers)

# Iterate through instances and populate the sheet
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance["InstanceId"]
        instance_tags = instance.get("Tags", [])
        instance_tag_dict = {tag["Key"]: tag["Value"] for tag in instance_tags}
        instance_name = instance_tag_dict.get("Name", "")
        instance_type = instance["InstanceType"]
        instance_state = instance["State"]["Name"]
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        public_ip = instance.get('PublicIpAddress', 'N/A')
        security_groups = ', '.join([sg['GroupName'] for sg in instance['SecurityGroups']])
        vpc_id = instance['VpcId']
        subnet_id = instance['SubnetId']
        iam_role = instance.get('IamInstanceProfile', {}).get('Arn', 'N/A')
        platform = instance.get('Platform', 'Linux/Unix')
        key_name = instance.get('KeyName', 'N/A')
        
        instance_details = [instance_id, instance_name, instance_type, instance_state, private_ip, public_ip, security_groups, vpc_id,
                            subnet_id, iam_role, platform, key_name]
        sheet.append(instance_details)

# Save the workbook
output_filename = "EC2_Instance_Details.xlsx"
workbook.save(output_filename)
print(f"Excel file '{output_filename}' created successfully.")
