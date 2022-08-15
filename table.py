import boto3
import trp
import boto3
import configparser
import os

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

# Document
documentName = "image/SCH_SI_01_Page_001.jpg"

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.analyze_document(
        Document={
            'Bytes': document.read(),
        },
        FeatureTypes=["TABLES"])

#print(response)

doc = trp.Document(response)

for page in doc.pages:
     # Print tables
    for table in page.tables:
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}".format(r, c, cell.text))