from mailbox import linesep
import csv
import json
import sys
# from numpy import single
from text_config import districts
import pandas as pd
#from itertools import groupby
import re

# 1. get the total number of incidents in a pdf
# def get_total_incident(district_config,text_fn):
#   with open(text_fn) as file:
#     lines = file.readlines()
#     lines = [line.rstrip() for line in lines]

#     clean_lines = []
#     for line in lines:
#       line = line.replace('\x1b[94m','')
#       line = line.replace('\x1b[0m','')
#       clean_lines.append(line)

#     docs = district_config['doc_name']
    
#     total = 0
#     for doc in docs:
#       total += sum(doc in line for line in clean_lines)
#     return clean_lines,total

# lines, syr_total = get_total_incident(districts['syr'],'text.txt')

# print("The estimated number of incidents in this pdf is", syr_total)

# #
# # 2. split the pdf by incidents
# delimiters =  districts['syr']['doc_name']

# bigList = []
# smallList = []
# words_to_split_by = districts['syr']['doc_name']
# for line in lines:    
#     if line not in words_to_split_by:
#        smallList.append(line)
#     else:
#        bigList.append(smallList)
#        smallList = []

# print('We could read',len(bigList), 'of them.')
# print('----------------------------------')

# 3. now, let's pull data out of the incidents
district = 'NOCO'

with open('json/NOCO/NOCO_1-499.json') as f:
  data_1 = json.load(f)

with open('json/NOCO/NOCO500-999.json') as f:
  data_2 = json.load(f)

with open('json/NOCO/NOCO1000_1499.json') as f:
  data_3 = json.load(f)

with open('json/NOCO/NOCO2000_2499.json') as f:
  data_4 = json.load(f)

with open('json/NOCO/NOCO2500_.json') as f:
  data_5 = json.load(f)

# I think Health Office Visit Report is attached to incident report, need to remove them
data = data_1 + data_2 + data_3 + data_4 + data_5
new_data = [item for item in data if 'Health Office Visit Report' not in item]

print(len(new_data))

# print(new_data[0])
# print('-------------------------------')
# print(new_data[1])
# print('-------------------------------')
# print(new_data[2])
# print('-------------------------------')
# print(new_data[3])
# print('-------------------------------')
# print(new_data[4])
# print('-------------------------------')
# print(new_data[5])


doc_type = districts[district]['doc_type']
dates = districts[district]['incident_date']
grades = districts[district]['grade']
durations = districts[district]['duration']
#locations = districts[district]['location']
types = districts[district]['restraint_type']
injuries = districts[district]['injury']
description = districts[district]['description']
#restraint_des = districts[district]['restraint_description']

def get_next_line(lst,element):
  index = lst.index(element)
  return lst[index +1]

def get_next_five_lines(lst,element):
  index = lst.index(element)
  return lst[index + 1] + lst[index + 2] + lst[index + 3] + lst[index + 4] + lst[index + 5]

def has_number(line):
  #return bool(re.search(r'/', line))
  return bool(re.search(r'\d', line))

AllIncidents = []
# any(ext in url_string for ext in extensionsToCheck)
for incident in new_data:
  incident_dict = {}
  incident_dict['id'] = incident[0]
  for line in incident:
    if any(type in line for type in doc_type):
      incident_dict['doc_type'] = line

    if any(date in line for date in dates):
        if has_number(line):
            incident_dict['date'] = line
        else:
            incident_dict['date'] = get_next_line(incident,line)


    if any(grade in line for grade in grades):
          if has_number(line):
              incident_dict['grade'] = line
          else:
              incident_dict['grade'] = get_next_line(incident,line)
    # if any(time in line for time in all_time):
    #   time = get_next_line(incident,line)
    #   incident_time.append(time)
    if any(duration in line for duration in durations):
      if has_number(line):
        incident_dict['duration']=line
      else:
        incident_dict['duration'] = get_next_line(incident,line)
    try:
      if any(type in line for type in types):
        if "Emergency Intervention(s)" in line:
          incident_dict['restrict_type'] = get_next_line(incident,line)
        else:
          incident_dict['restrict_type']  = line
    except:
      pass

    try:
      if any(injury in line for injury in injuries):
        if 'If yes, please describe.' in line:
          incident_dict['injury'] = get_next_line(incident,line)
        else:
          incident_dict['injury']  = line
    except:
      pass

    if any(des in line for des in description):
      incident_dict['description']  = get_next_five_lines(incident,line)

  AllIncidents.append(incident_dict)

print(len(AllIncidents))

# print('--------------------------------')
# print(AllIncidents[0])
# print('--------------------------------')
# print(AllIncidents[1])
# print('--------------------------------')
# print(AllIncidents[2])
# print('--------------------------------')
# print(AllIncidents[3])
# print('--------------------------------')
# print(AllIncidents[4])
# print('--------------------------------')
# print(AllIncidents[5])
# print('--------------------------------')
# print(AllIncidents[6])
# print('--------------------------------')
# print(AllIncidents[7])
# print('--------------------------------')
# print(AllIncidents[8])
# print('--------------------------------')
# print(AllIncidents[9])
# print('--------------------------------')
# print(AllIncidents[10])
# print('--------------------------------')
# print(AllIncidents[11])
# print('--------------------------------')
# print(AllIncidents[12])
# print('--------------------------------')
# print(AllIncidents[13])
# print('--------------------------------')




df = pd.DataFrame(AllIncidents)
df.to_csv('csv/NOCO.csv')