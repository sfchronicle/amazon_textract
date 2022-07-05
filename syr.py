from mailbox import linesep
import csv
import json
import sys
# from numpy import single
from text_config import districts
import pandas as pd
#from itertools import groupby
import re



# let's pull data out of the incidents
district = 'SYR'

with open('json/SYR.json') as f:
  data = json.load(f)



# I think Health Office Visit Report is attached to incident report, need to remove them
#new_data = [item for item in data if 'Health Office Visit Report' not in item]

print(len(data))

print(data[14])
print('-------------------------------')
print(data[15])
print('-------------------------------')
print(data[16])
print('-------------------------------')
print(data[17])
print('-------------------------------')
print(data[18])
print('-------------------------------')
print(data[19])
print('-------------------------------')
print(data[20])
print('-------------------------------')
print(data[21])
print('-------------------------------')
print(data[22])
print('-------------------------------')
print(data[23])
print('-------------------------------')
print(data[-4])
print('-------------------------------')
print(data[-3])
print('-------------------------------')
print(data[-2])
print('-------------------------------')
print(data[-1])

doc_type = districts[district]['doc_type']
incident_date = districts[district]['incident_date']
types = districts[district]['restraint_type']
time_began = districts[district]['time_began']
time_ended = districts[district]['time_ended']
duration = districts[district]['duration']
injury = districts[district]['injury']
description = districts[district]['description']

def get_next_line(lst,element):
  index = lst.index(element)
  return lst[index +1]

def get_second_line(lst,element):
  index = lst.index(element)
  return lst[index + 2] 

def get_next_five_lines(lst,element):
  index = lst.index(element)
  return lst[index + 1] + lst[index + 2]  + lst[index + 3] + lst[index + 4] +  lst[index + 5]

def has_number(line):
  #return bool(re.search(r'/', line))
  return bool(re.search(r'\d', line))

AllIncidents = []
# any(ext in url_string for ext in extensionsToCheck)
for incident in data:
  incident_dict = {}
  incident_dict['id'] = incident[0]
  for line in incident:
    if any(type in line for type in doc_type):
      incident_dict['doc_type'] = line

    if any(date in line for date in incident_date):
        if has_number(line):
            incident_dict['date'] = line
        else:
            incident_dict['date'] = get_next_line(incident,line)

    if any(time in line for time in time_began):
      if has_number(line):
        incident_dict['time_began']=line
      else:
        incident_dict['time_began'] = get_next_line(incident,line)


    if any(time in line for time in time_ended):
      if has_number(line):
        incident_dict['time_ended']=line
      else:
        incident_dict['time_ended'] = get_next_line(incident,line)



    if any(time in line for time in duration):
      if has_number(line):
        incident_dict['duration']=line
      else:
        incident_dict['duration'] = get_next_line(incident,line)

    if any(type in line for type in types):
        incident_dict['restraint_type'] = line + get_second_line(incident,line)


    if any(des in line for des in description):
      incident_dict['description']  = get_next_five_lines(incident,line)


    if any(des in line for des in injury):
      incident_dict['injury']  = line + get_next_line(incident,line)

  AllIncidents.append(incident_dict)

print("HELLO THERE")
print(len(AllIncidents))

df = pd.DataFrame(AllIncidents)
df.to_csv('csv/SYR.csv')