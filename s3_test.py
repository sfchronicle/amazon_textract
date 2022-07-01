import boto3
import os
import sys
import configparser


cp = configparser.ConfigParser(interpolation=None)
# read env file based on location
if os.path.exists('/Users/yzhao/.env'): 
    cp.read('/Users/yzhao/.env')  
else: # production
    cp.read("/home/ec2-user/Projects/deploy-engine/.env")

# Prep AWS
os.environ["AWS_ACCESS_KEY_ID"] = cp.get('aws', 'textract_user')
os.environ["AWS_SECRET_ACCESS_KEY"] = cp.get('aws', 'textract_pass')
session = boto3.Session(
    aws_access_key_id= cp.get('aws', 's3_user'),
    aws_secret_access_key=cp.get('aws', 's3_pass'),
)
s3 = session.resource('s3')
client = boto3.client('s3')

s3BucketName = "sfc-project-files"
prefix ='restraint-seclusion/SCH'

file_names = []
result = client.list_objects_v2(Bucket=s3BucketName, Prefix=prefix)
for item in result['Contents']:
    files = item['Key'].split('/')
    files = files[3].replace('.pdf','')
    print(files)
    file_names.append(files)  
print(len(file_names))
