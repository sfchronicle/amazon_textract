import webbrowser, os
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import configparser
from os import listdir
from os.path import isfile,join

# Prep AWS
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


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text


def get_table_csv_results(file_name):

    # process using image bytes
    # get the results
    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract

    with open(file_name, "rb") as document:
        response = textract.analyze_document(
            Document={
                'Bytes': document.read(),
            },
            FeatureTypes=["TABLES"])

    # Get the text blocks
    blocks=response['Blocks']
    # pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index +1)
        csv += '\n\n'

    return csv

def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'
        
    csv += '\n\n\n'
    return csv

def main(file_name):
    table_csv = get_table_csv_results(file_name)

    output_file = f'{file_name}.csv'

    # replace content
    with open(output_file, "wt") as fout:
        fout.write(table_csv)

    # show the results
    print('CSV OUTPUT FILE: ', output_file)


# Document
path = "image/MON/MON2_SI_01_table"

files = [f for f in listdir(path) if isfile(join(path, f))]


for file in files:
    file_name = f"{path}/{file}"
    print(file_name)
    if __name__ == "__main__":
        main(file_name)
    