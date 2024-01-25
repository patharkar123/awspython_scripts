import boto3
import openpyxl

# AWS credentials
aws_access_key = ""
aws_secret_key = ""
region_name = "ap-south-1"  # Update with your desired region

# Initialize the Boto3 S3 client
s3_client = boto3.client('s3', region_name=region_name,
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key)

# Fetch S3 bucket details
buckets = s3_client.list_buckets()

# Create an Excel workbook and add a sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "S3 Buckets"

# Add headers
headers = ["Bucket Name", "Creation Date"]
sheet.append(headers)

# Iterate through buckets and populate the sheet
for bucket in buckets['Buckets']:
    bucket_name = bucket['Name']
    creation_date = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')
    
    bucket_details = [bucket_name, creation_date]
    sheet.append(bucket_details)

# Save the workbook
output_filename = "S3_Bucket_Details.xlsx"
workbook.save(output_filename)
print(f"Excel file '{output_filename}' created successfully.")
