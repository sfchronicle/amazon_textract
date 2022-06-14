import boto3
# import io
# from io import BytesIO
import os
import sys
import configparser
import base64
import time

import math
# from PIL import Image, ImageDraw, ImageFont

# Parse the config 
cp = configparser.ConfigParser(interpolation=None)
# read env file based on location
if os.path.exists('../../.env'): 
    cp.read('../../.env')  
else: # production
    cp.read("/home/ec2-user/Projects/deploy-engine/.env")

# Prep AWS
os.environ["AWS_ACCESS_KEY_ID"] = cp.get('aws', 'textract_user')
os.environ["AWS_SECRET_ACCESS_KEY"] = cp.get('aws', 'textract_pass')

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
documentName = "restraint-seclusion/pdf/SYR_RI_01.pdf"

jobId = startJob(s3BucketName, documentName)
print("Started job with id: {}".format(jobId))
if(isJobComplete(jobId)):
    response = getJobResults(jobId)

#print(response)

# Print detected text
lines = []
for resultPage in response:
    for item in resultPage["Blocks"]:
        if item["BlockType"] == "LINE":
            lines.append(item['Text'])
            #print ('\033[94m' +  item["Text"] + '\033[0m')