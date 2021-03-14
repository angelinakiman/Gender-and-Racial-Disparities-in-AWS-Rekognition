# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 08:43:52 2021

@author: Angelina Kiman
"""

# import
import json
import csv
import os
import copy

# read file
csvfile = open('C:\\Users\\angel\\OneDrive\\Documents\\FairFace\\fairface_label_val.csv', 'r')

# write file
jsonfile = open('C:\\Users\\angel\\OneDrive\\Documents\\FairFace\\fairface_label_val.manifest', 'w')

# s3 bucket path
s3bucket = 's3://fairface-dataset/'

# loop over rows
csv_reader = csv.reader(csvfile, delimiter=',')
line_count = 0
max_lines = 10954
jsons = {}
for row in csv_reader:
    if line_count == 0:
        line_count += 1
    else:
        filename = row[0]
        
        # meta json
        metat = {}
        metat['confidence'] = 1
        metat['human-annotated'] = "yes"
        metat['creation-date'] = "2020-03-06T17:46:39.176"
        metat['type'] = "groundtruth/image-classification"
        metarace = copy.deepcopy(metat)
        metarace['class-name'] = row[3]
        metagender = copy.deepcopy(metat)
        metagender['class-name'] = row[2]
        
        # final json item
        jsonitem = {}
        jsonitem['source-ref'] = os.path.join(s3bucket, filename)
        jsonitem["gender"] = 0
        jsonitem["gender-metadata"] = metagender
        
        jsonitem["race"] = 1
        jsonitem["race-metadata"] = metarace
        line_count += 1
        
        # write line
        json.dump(jsonitem, jsonfile)
        jsonfile.write("\n")
        
        if line_count > max_lines:
            break
print(f'Processed {line_count} lines.')

csvfile.close()
jsonfile.close()

#{
#    "source-ref": "s3://bucket/images/sunrise.png",
#    "testdataset-classification_Sunrise": 1,
#    "testdataset-classification_Sunrise-metadata": {
#        "confidence": 1,
#        "job-name": "labeling-job/testdataset-classification_Sunrise",
#        "class-name": "Sunrise",
#        "human-annotated": "yes",
#        "creation-date": "2020-03-06T17:46:39.176",
#        "type": "groundtruth/image-classification"
#    }
#}