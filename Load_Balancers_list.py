import boto3
import openpyxl

# AWS credentials
aws_access_key = ""
aws_secret_key = ""
region_name = "ap-south-1"  # Update with your desired region

# Initialize the Boto3 ELB client
elbv2_client = boto3.client('elbv2', region_name=region_name,
                         aws_access_key_id=aws_access_key,
                         aws_secret_access_key=aws_secret_key)

# Fetch Load Balancer details
load_balancers = elbv2_client.describe_load_balancers()

# Create an Excel workbook and add a sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Load Balancers"

# Add headers
headers = ["Load Balancer Name", "Private IP", "Public IP", "DNS Name", "Type", "Scheme","VPC ID"]
sheet.append(headers)

# Iterate through load balancers and populate the sheet
for lb in load_balancers['LoadBalancers']:
    lb_name = lb['LoadBalancerName']
    private_ips = []
    public_ips = []
    
    # Fetch target groups associated with the load balancer
    target_groups = elbv2_client.describe_target_groups(LoadBalancerArn=lb['LoadBalancerArn'])
    
    for target_group in target_groups['TargetGroups']:
        target_health = elbv2_client.describe_target_health(TargetGroupArn=target_group['TargetGroupArn'])
        
        for target in target_health['TargetHealthDescriptions']:
            private_ip = target['Target']['Id']
            private_ips.append(private_ip)
            
            # Fetch instance information to get the public IP
            ec2_client = boto3.client('ec2', region_name=region_name,
                                     aws_access_key_id=aws_access_key,
                                     aws_secret_access_key=aws_secret_key)
            instance_info = ec2_client.describe_instances(InstanceIds=[private_ip])
            public_ip = instance_info['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')
            public_ips.append(public_ip)
    
    private_ip_str = ', '.join(private_ips)
    public_ip_str = ', '.join(public_ips)
    dns_name = lb['DNSName']
    lb_type = lb['Type']
    scheme = lb['Scheme']
    vpc_id = lb['VpcId']
    
    
    
    lb_details = [lb_name, private_ip_str, public_ip_str, dns_name, lb_type, scheme, vpc_id]
    sheet.append(lb_details)

# Save the workbook
output_filename = "Load_Balancer_Details.xlsx"
workbook.save(output_filename)
print(f"Excel file '{output_filename}' created successfully.")
