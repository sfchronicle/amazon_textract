import boto3
# import io
# from io import BytesIO
import os
import sys
import configparser
import base64
import time
import json
import math
# from PIL import Image, ImageDraw, ImageFont

# Parse the config 
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


#get text
# with open("GLEN_RI_01.pdf", "rb") as pdf_file:
#     encoded_string = base64.b64encode(pdf_file.read())


# client = boto3.client('textract', region_name='us-west-1')
# response = client.analyze_document(Document={'Bytes': encoded_string},
#         FeatureTypes=["TABLES", "FORMS"])

# print(response)

def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract', region_name='us-east-1')
    response = client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        }
    })

    return response["JobId"]

def isJobComplete(jobId):
    time.sleep(5)
    client = boto3.client('textract', region_name='us-east-1')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

def getJobResults(jobId):

    pages = []

    time.sleep(5)

    client = boto3.client('textract', region_name='us-east-1')
    response = client.get_document_text_detection(JobId=jobId)
    
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']

    while(nextToken):
        time.sleep(5)

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages

# Document
s3BucketName = "sfc-project-files"
district_name = 'ASSS/ASSS_SI'
prefix =f'restraint-seclusion/{district_name}/'

# get file names of all pdfs in S3 folder
file_names = []
result = client.list_objects_v2(Bucket=s3BucketName, Prefix=prefix)
for item in result['Contents']:
    files = item['Key'].split('/')
    files = files[3].replace('.pdf','')
    print(files)
    file_names.append(files)  
#print(file_names)

# get all lines from the pdfs and save them into one json file
all_lines = []
for file in file_names[1:]: # the first file name is '', so we should start from the second one
    documentName = f"restraint-seclusion/{district_name}/{file}.pdf"
    print(documentName)

    jobId = startJob(s3BucketName, documentName)
    print("Started job with id: {}".format(jobId))
    if(isJobComplete(jobId)):
        response = getJobResults(jobId)

    # Print detected text
    lines = []
    for resultPage in response:
        for item in resultPage["Blocks"]:
            if item["BlockType"] == "LINE":
                lines.append(item['Text'])
                #print ('\033[94m' +  item["Text"] + '\033[0m')
    lines.insert(0,file)
    all_lines.append(lines)

print(len(all_lines))

#district_folder = "/restraint-seclusion/text/"
object = s3.Object(s3BucketName,f'restraint-seclusion/text/{district_name}2000_2199.json').put(Body=json.dumps(all_lines))

