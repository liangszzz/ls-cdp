import boto3
from botocore.exceptions import ClientError


def create_job():
    pass

def update_job():
    pass

def create_bucket():
    pass

def create_role():
    pass

# Set your AWS credentials
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'
aws_session_token = 'your_session_token'  # (if you are using temporary credentials)

# Set the AWS region and clients for IAM and Glue
region_name = 'your_region'
iam_client = boto3.client('iam', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
glue_client = boto3.client('glue', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

# Define the IAM role name and S3 bucket name
role_name = 'your_glue_role'
s3_bucket_name = 'your-s3-bucket-name'

# Check if the IAM role already exists
try:
    role_response = iam_client.get_role(RoleName=role_name)
    print("IAM role already exists. Reusing existing role.")
    role_arn = role_response['Role']['Arn']

except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity':
        # The IAM role does not exist, create it
        print("IAM role does not exist. Creating a new role.")

        # Define the trust relationship policy document for Glue
        trust_relationship_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "glue.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        # Create the IAM role
        role_response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=str(trust_relationship_policy)
        )

        # Define the IAM policy for S3 read and write access
        s3_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{s3_bucket_name}/*",
                        f"arn:aws:s3:::{s3_bucket_name}"
                    ]
                }
            ]
        }

        # Attach the S3 policy to the IAM role
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName='S3AccessPolicy',
            PolicyDocument=str(s3_policy)
        )

        # Print the ARN of the created role
        role_arn = role_response['Role']['Arn']
        print("IAM Role ARN:", role_arn)

    else:
        # An unexpected error occurred
        raise e

# Define the Glue job parameters
job_name = 'your_glue_job'
script_location = 's3://your-bucket/your-script.py'  # S3 path to your Python script
etl_script = {
    'S3Uri': script_location,
    'PythonVersion': '3',
}

# Check if the Glue job already exists
try:
    job_response = glue_client.get_job(JobName=job_name)
    print("Glue job already exists. Updating existing job.")

    # Update the Glue job
    response = glue_client.update_job(
        JobName=job_name,
        JobUpdate={
            'Role': role_arn,
            'Command': {
                'Name': 'pythonshell',
                'ScriptLocation': etl_script['S3Uri'],
            },
            'DefaultArguments': {
                '--job-language': 'python',
            },
            'MaxCapacity': 10,  # Specify the number of Data Processing Units (DPUs) for your job
        }
    )

    # Print the response
    print("Glue Job Updated:", response)

except ClientError as e:
    if e.response['Error']['Code'] == 'EntityNotFoundException':
        # The Glue job does not exist, create it
        print("Glue job does not exist. Creating a new job.")

        # Create the Glue job
        response = glue_client.create_job(
            Name=job_name,
            Role=role_arn,
            Command={
                'Name': 'pythonshell',
                'ScriptLocation': etl_script['S3Uri'],
            },
            DefaultArguments={
                '--job-language': 'python',
            },
            AllocatedCapacity=10,  # Specify the number of Data Processing Units (DPUs) for your job
        )

        # Print the response
        print("Glue Job Created:", response)

    else:
        # An unexpected error occurred
        raise e
