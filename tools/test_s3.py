import boto3

s3 = boto3.client('s3', endpoint_url="http://localstack:4566")

# Example: List objects in a bucket
response = s3.list_objects_v2(Bucket='cdp-input1')

# Process the response
for obj in response.get('Contents', []):
    print(obj['Key'])
