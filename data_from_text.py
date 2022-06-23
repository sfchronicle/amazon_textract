from mailbox import linesep
import csv
import json
import sys
from numpy import single
from text_config import districts
import pandas as pd
from itertools import groupby
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

data = data_1 + data_2
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


doc_type = districts[district]['doc_type']
dates = districts[district]['incident_date']
# all_time = districts[district]['incident_time']
grades = districts[district]['grade']
durations = districts[district]['duration']
#locations = districts[district]['location']
types = districts[district]['restraint_type']
#print(types)
#staffs = districts[district]['staff']
injuries = districts[district]['injury']
description = districts[district]['description']
#restraint_des = districts[district]['restraint_description']

def get_next_line(lst,element):
  index = lst.index(element)
  return lst[index +1]

def has_number(line):
  #return bool(re.search(r'/', line))
  return bool(re.search(r'\d', line))

doc_types = []
#incident_dates = []
# incident_time = []
restraint_durations = []
student_grades = []
#restraint_location = []
restraint_types = []
#staff = []
injuries = []
incident_descriptions = []
#restraint_description = []

AllIncidents = []
# any(ext in url_string for ext in extensionsToCheck)
for incident in data:
  indicient_dict = {}
  for line in incident:
    if any(type in line for type in doc_type):
      doc_types.append(line)
   
    # if any(date in line for date in dates):
    #   print(line)
    #   if has_number(line):
    #     incident_dates.append(line)
    #   else:
    #     incident_dates.append(get_next_line(incident,line))
    # else:
    #   print('False')
    #   incident_dates.append('NA')


    if any(date in line for date in dates):
        if has_number(line):
            indicient_dict['date'] = line
        else:
            indicient_dict['date'] = get_next_line(incident,line)
  
    if any(grade in line for grade in grades):
      if has_number(line):
        student_grades.append(line)
      else:
        student_grades.append(get_next_line(incident,line))
    else:
      student_grades.append('NA')
    
    # if any(time in line for time in all_time):
    #   time = get_next_line(incident,line)
    #   incident_time.append(time)
    if any(duration in line for duration in durations):
      if has_number(line):
        duration = line
      else:
        duration = get_next_line(incident,line)
      restraint_durations.append(duration)
    else:
      restraint_durations.append('NA')

    # if any(location in line for location in locations):
    #   restraint_location.append(line)

    if any(type in line for type in types):
      if "Emergency Intervention(s)" in line:
        restraint_type = get_next_line(incident,line)
      else:
        restraint_type = line
      restraint_types.append(restraint_type)
    # else:
    #   restraint_types.append('NA')
      # try:
        #restraint_type.append(line.split(': ')[1])
      # except:
      #   pass
        #print('N/A')

    #if any(staff in line for staff in staffs):
      #staffs.append(line)
    # if any(injury in line for injury in injuries):
    #   injury.append(line)

    if any(des in line for des in description):
      des = get_next_line(incident,line)
      incident_descriptions.append(des)

  AllIncidents.append(indicient_dict)
    # if any(des in line for des in restraint_des):
    #   restraint_description.append(line)      

#print(incident_dates)
print('--------------------------------')
print(AllIncidents[0:6])
print('--------------------------------')
print(doc_types[0:5])
print('--------------------------------')
# print(incident_time[0:5])
# print('--------------------------------')
print(restraint_durations[0:5])
print('--------------------------------')
print(student_grades[0:5])
print('--------------------------------')
# # print(restraint_location)
# # print('--------------------------------')
print(restraint_types[0:5])
print('--------------------------------')
# #print(staffs[1])
# # print('--------------------------------')
# print(injury)
# print('--------------------------------')
print(incident_descriptions[0:5])
print('--------------------------------')




