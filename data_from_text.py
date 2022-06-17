from mailbox import linesep

from numpy import single
from text_config import districts
import pandas as pd
from itertools import groupby

# 1. get the total number of incidents in a pdf
def get_total_incident(district_config,text_fn):
  with open(text_fn) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

    clean_lines = []
    for line in lines:
      line = line.replace('\x1b[94m','')
      line = line.replace('\x1b[0m','')
      clean_lines.append(line)

    docs = district_config['doc_name']
    
    total = 0
    for doc in docs:
      total += sum(doc in line for line in clean_lines)
    return clean_lines,total

lines, syr_total = get_total_incident(districts['syr'],'text.txt')

print("The estimated number of incidents in this pdf is", syr_total)

#
# 2. split the pdf by incidents
delimiters =  districts['syr']['doc_name']

bigList = []
smallList = []
words_to_split_by = districts['syr']['doc_name']
for line in lines:    
    if line not in words_to_split_by:
       smallList.append(line)
    else:
       bigList.append(smallList)
       smallList = []

print('We could read',len(bigList), 'of them.')
print('----------------------------------')

# 3. now, let's pull data out of the incidents
incident_date = []
incident_time = []
restraint_duration = []
restraint_location = []
restraint_type = []
staff = []
injury = []
incident_description = []
restraint_description = []


dates = districts['syr']['incident_date']
times = districts['syr']['incident_time']
durations = districts['syr']['duration']
locations = districts['syr']['location']
types = districts['syr']['restraint_type']
staffs = districts['syr']['staff']
injuries = districts['syr']['injury']
incident_des = districts['syr']['incident_description']
restraint_des = districts['syr']['restraint_description']


# any(ext in url_string for ext in extensionsToCheck)
for incident in bigList:
  for line in incident:
    if any(date in line for date in dates):
      incident_date.append(line)
    
    if any(time in line for time in times):
      incident_time.append(line)
    
    if any(duration in line for duration in durations):
      restraint_duration.append(line)

    if any(location in line for location in locations):
      restraint_location.append(line)
    
    if any(type in line for type in types):
      try:
        restraint_type.append(line.split(': ')[1])
      except:
        pass
        #print('N/A')

    if any(staff in line for staff in staffs):
      staffs.append(line)

    if any(injury in line for injury in injuries):
      injury.append(line)

    if any(des in line for des in incident_des):
      incident_description.append(line)

    if any(des in line for des in restraint_des):
      restraint_description.append(line)      

print(incident_date[1])
print('--------------------------------')
print(incident_time[1])
print('--------------------------------')
print(restraint_duration[1])
print('--------------------------------')
print(restraint_location[1])
print('--------------------------------')
print(restraint_type[1])
print('--------------------------------')
print(staffs[1])
print('--------------------------------')
print(injury[1])
print('--------------------------------')
print(incident_description[1])
print('--------------------------------')
print(restraint_description[1])
