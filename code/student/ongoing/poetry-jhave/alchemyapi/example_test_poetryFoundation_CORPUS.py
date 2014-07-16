#!/usr/bin/env python

# modified to feed text file...


from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

import re
import os, datetime
import sys
import json

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

# SOURCE files
type_of_run="6"
DATA_DIR  =  "../../../../../data/poetryFoundation/"
TXT_DIR = "txt_"+type_of_run+"/"

WRITE_JSON_PATH = DATA_DIR+"json/ALCHEMY_"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"/"

# sample different segments of archive
break_cnt=0
break_cnt_min=0
break_cnt_max=60000


#################################################
#                                               #
#    ALCHEMY                                    #
#                                               #
#################################################
def alchemy(id,demo_text):

    print('ALchemy processing ID: ', id)
    # print('Processing text: ', demo_text)
    combined_dict={}
    relation_dict={}

    # print('############################################')
    # print('#   Combined                       #')
    # print('############################################')

    response = alchemyapi.combined('text', demo_text)

    if response['status'] == 'OK':
        #print('## Response Object ##')
        #print(json.dumps(response, indent=4))
        combined_dict = response

    else:
        print('Error in combined call: ', response['statusInfo'])

    # print('############################################')
    # print('#   Relation Extraction                    #')
    # print('############################################')

    response = alchemyapi.relations('text', demo_text)

    if response['status'] == 'OK':
        #print(json.dumps(response, indent=4))
        relation_dict = response
        

    else:
        print('Error in relation extaction call: ', response['statusInfo'])

    merged_dict = {key: value for (key, value) in (combined_dict.items() + relation_dict.items())}

    json.dump(merged_dict, f_json)

#################################################
#                                               #
#   READ FILES, CALL Alchemy, WRITE to json     #
#                                               #
#################################################
for subdir, dirs, files in os.walk(DATA_DIR+TXT_DIR):
    for file in files:

        # take subset of files for testing
        break_cnt+=1
        if break_cnt<break_cnt_min:
            continue

        if ".txt" in file  and 'readme' not in file:

            # ID
            id=file.split(".")[0]

            # READ txt file
            pf = open(subdir+file, 'r')
            demo_text = pf.read()
            pf.close()

            # OPEN json for writing
            json_fn = "poetryFoundation_"+id+"_Alchemy_JSON.txt"
            json_fn_path = WRITE_JSON_PATH+json_fn

            # CREATE json dir
            if not os.path.exists(WRITE_JSON_PATH):
                os.makedirs(WRITE_JSON_PATH)

            # try:
            #     if os.path.isfile(json_fn_path):
            #         os.unlink(json_fn_path)
            # except Exception, e:
            #     print e

            # OPEN json file for WRITE
            f_json=open(json_fn_path,'a')

            #CALL Alchemy
            alchemy(id,demo_text)

            # CLOSE json
            f_json.close()

