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
district = 'SCH'

with open('json/SCH_02.json') as f:
  data = json.load(f)
#print(len(data_1))



# I think Health Office Visit Report is attached to incident report, need to remove them
#new_data = [item for item in data if 'Health Office Visit Report' not in item]

print(len(data))

print(data[0])
print('-------------------------------')
print(data[1])
print('-------------------------------')
print(data[2])
print('-------------------------------')
print(data[3])
print('-------------------------------')
print(data[4])
print('-------------------------------')
print(data[5])
print('-------------------------------')
print(data[6])
print('-------------------------------')
print(data[7])
print('-------------------------------')
print(data[8])
print('-------------------------------')
print(data[9])
print('-------------------------------')
print(data[10])


doc_type = districts[district]['doc_type']
school_building = districts[district]['school']
incident_date = districts[district]['incident_date']
student_id = districts[district]['student_id']
grade = districts[district]['grade']
duration = districts[district]['duration']
start_time = districts[district]['start_time']
end_time = districts[district]['end_time']
types = districts[district]['restraint_type']
student_injury = districts[district]['student_injury']
adult_injury = districts[district]['adult_injury']
description = districts[district]['description']

def get_next_line(lst,element):
  index = lst.index(element)
  return lst[index +1]

def get_next_three_lines(lst,element):
  index = lst.index(element)
  return lst[index + 1] + lst[index + 2] + lst[index + 3]

def get_next_five_lines(lst,element):
  index = lst.index(element)
  return lst[index + 1] + lst[index + 2] + lst[index + 3] + lst[index + 4] + lst[index + 5]

def get_next_six_lines(lst,element):
  index = lst.index(element)
  return lst[index + 1] + lst[index + 2] + lst[index + 3] + lst[index + 4] + lst[index + 5] + lst[index + 6]

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


    if any(building in line for building in school_building):
              incident_dict['school_building'] = line 

    if any(time in line for time in start_time):
      if has_number(line):
        incident_dict['start_time']=line
      else:
        incident_dict['start_time'] = get_next_line(incident,line)

    if any(time in line for time in end_time):
      if has_number(line):
        incident_dict['end_time']=line
      else:
        incident_dict['end_time'] = get_next_line(incident,line)

    if any(time in line for time in duration):
      if has_number(line):
        incident_dict['duration']=line
      else:
        incident_dict['duration'] = get_next_line(incident,line)

    if any(time in line for time in student_id):
      if has_number(line):
        incident_dict['student_id']=line
      else:
        incident_dict['student_id'] = get_next_line(incident,line)

    if any(time in line for time in grade):
      if has_number(line):
        incident_dict['grade']=line
      else:
        incident_dict['grade'] = get_next_line(incident,line)

    if any(time in line for time in student_injury):
        incident_dict['student_injury'] = get_next_line(incident,line)

    if any(time in line for time in adult_injury):
        incident_dict['adult_injury'] = get_next_three_lines(incident,line)

    try:
      if any(type in line for type in types):
          incident_dict['restraint_type'] = get_next_six_lines(incident,line)
    except:
      pass

    if any(des in line for des in description):
      incident_dict['description']  = get_next_five_lines(incident,line)

  AllIncidents.append(incident_dict)

print(len(AllIncidents))

print('+++++++++++++++++++++++++++++++++++++++++++++')
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
df.to_csv('csv/SCH_02.csv')