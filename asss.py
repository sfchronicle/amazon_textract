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
district = 'ASSS'

with open('json/ASSS/ASSS_RI.json') as f:
  data_1 = json.load(f)

with open('json/ASSS/ASSS_SI1_998.json') as f:
  data_2 = json.load(f)

with open('json/ASSS/ASSS_SI999_1999.json') as f:
  data_3 = json.load(f)

with open('json/ASSS/ASSS_SI2000_2199.json') as f:
  data_4 = json.load(f)

data_RI = data_1
data_SI = data_2 + data_3 + data_4

# I think Health Office Visit Report is attached to incident report, need to remove them
#new_data = [item for item in data if 'Health Office Visit Report' not in item]

print(len(data_RI))

print(data_RI[0])
print('-------------------------------')
print(data_RI[1])
print('-------------------------------')
print(data_RI[2])
print('-------------------------------')
print(data_RI[3])
print('-------------------------------')
print(data_RI[4])
print('-------------------------------')
print(data_RI[5])


doc_type = districts[district]['doc_type']
student_id = districts[district]['student_id']
incident_date = districts[district]['incident_date']
start_time = districts[district]['start_time']
end_time = districts[district]['end_time']
types = districts[district]['restraint_type']
description = districts[district]['description']

def get_next_line(lst,element):
  index = lst.index(element)
  return lst[index +1]

def get_second_line(lst,element):
  index = lst.index(element)
  return lst[index + 2] 

def get_next_three_lines(lst,element):
  index = lst.index(element)
  return lst[index + 1] +" "+ lst[index + 2] + " " + lst[index + 3]

def has_number(line):
  #return bool(re.search(r'/', line))
  return bool(re.search(r'\d', line))

AllIncidents = []
# any(ext in url_string for ext in extensionsToCheck)
for incident in data_RI:
  incident_dict = {}
  incident_dict['id'] = incident[0]
  for line in incident:
    if any(type in line for type in doc_type):
      incident_dict['doc_type'] = line

    if any(date in line for date in incident_date):
        if has_number(line):
            incident_dict['date'] = line
        elif 'Start Time:' in get_next_line(incident,line):
          incident_dict['date'] = get_second_line(incident,line)
        else:
            incident_dict['date'] = get_next_line(incident,line)


    if any(building in line for building in student_id):
          if has_number(line):
              incident_dict['student_id'] = line
          else:
              incident_dict['student_id'] = get_next_line(incident,line)
    # if any(time in line for time in all_time):
    #   time = get_next_line(incident,line)
    #   incident_time.append(time)
    if any(time in line for time in start_time):
      if has_number(line):
        incident_dict['start_time']=line
      else:
        incident_dict['start_time'] = get_second_line(incident,line)

    if any(time in line for time in end_time):
      if has_number(line):
        incident_dict['end_time']=line
      else:
        incident_dict['end_time'] = get_next_three_lines(incident,line)

    try:
      if any(type in line for type in types):
          incident_dict['restraint_type'] = line + get_next_three_lines(incident,line)
    except:
      pass

    if any(des in line for des in description):
      incident_dict['description']  = get_next_three_lines(incident,line)

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
df.to_csv('csv/ASSS_RI.csv')