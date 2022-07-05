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
district = 'BALL'

with open('json/BALL.json') as f:
  data = json.load(f)

# I think Health Office Visit Report is attached to incident report, need to remove them
#new_data = [item for item in data if 'Health Office Visit Report' not in item]

print(len(data))

print(data[0])
print('-------------------------------')
print(data[1])
print('-------------------------------')
print(data[2])
print('-------------------------------')
print(data[10])
print('-------------------------------')
print(data[11])
print('-------------------------------')
print(data[12])
print('-------------------------------')
print(data[13])

doc_type = districts[district]['doc_type']
school_name = districts[district]['school_name']
incident_date = districts[district]['incident_date']
duration = districts[district]['duration']
types = districts[district]['restraint_type']
start_time = districts[district]['start_time']
exit_time = districts[district]['exit_time']

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


    if any(building in line for building in school_name):
      incident_dict['school_name'] = line + get_next_line(incident,line)

    if any(time in line for time in duration):
      if has_number(line):
        incident_dict['duration']=line
      else:
        incident_dict['duration'] = get_next_line(incident,line)

    if any(time in line for time in start_time):
        if has_number(line):
          incident_dict['start_time']=line
        else:
          incident_dict['start_time'] = get_next_line(incident,line)

    if any(time in line for time in exit_time):
        if has_number(line):
          incident_dict['exit_time']=line
        else:
          incident_dict['exit_time'] = get_next_line(incident,line)

    if any(type in line for type in types):
        incident_dict['restraint_type'] = line + get_next_five_lines(incident,line)


    

  AllIncidents.append(incident_dict)

print(len(AllIncidents))

print('--------------------------------')
print(AllIncidents[0])
print('--------------------------------')
print(AllIncidents[1])
print('--------------------------------')
print(AllIncidents[2])
print('--------------------------------')
print(AllIncidents[3])
print('--------------------------------')
print(AllIncidents[4])
print('--------------------------------')
print(AllIncidents[5])
print('--------------------------------')
print(AllIncidents[6])
print('--------------------------------')
print(AllIncidents[7])
print('--------------------------------')
print(AllIncidents[8])
print('--------------------------------')
print(AllIncidents[9])
print('--------------------------------')
print(AllIncidents[10])
print('--------------------------------')
print(AllIncidents[11])
print('--------------------------------')
print(AllIncidents[12])
print('--------------------------------')
print(AllIncidents[13])
print('--------------------------------')




df = pd.DataFrame(AllIncidents)
df.to_csv('csv/BALL.csv')