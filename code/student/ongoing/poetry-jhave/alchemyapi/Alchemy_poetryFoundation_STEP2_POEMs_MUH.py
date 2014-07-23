#!/usr/bin/env python

"""

1. 
Load all txt files in "bio" folder from poetryfoundation.org

2.
Send them to Alchemy API

2.
Write each response to a single JSON file for later import and incorporation into pipeline

"""


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
type_of_run="6"#18497
DATA_DIR  =  "../../../../../data/poetryFoundation/"
READ_TXT_DIR = "txt_poems_"+type_of_run+"/"
READ_PATH=DATA_DIR+READ_TXT_DIR

WRITE_JSON_PATH = DATA_DIR+"json/ALCHEMY_POEMS_"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"/"


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

    return merged_dict




#################################################
#                                               #
#   READ FILES, CALL Alchemy, WRITE to json     #
#                                               #
#################################################
def readDirectory(PATH,file_type):
    
    cnt=0

    for subdir, dirs, files in os.walk(PATH):
        for file in files:

            if file_type in file  and 'readme' not in file:

                # ID
                id=file.split(".")[0]

                cnt+=1

                # DAILY TRANSACTION LIMIT FOR ACADEMIC LICENSE IS 25,000 calls,
                # 66063 items at 4 transactions each
                # July 22nd : up to 247632 done.....
                if cnt>6061 and cnt<11000:

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

                    f_json=open(json_fn_path,'a')

                    # CALL Alchemy
                    merged_dict = alchemy(id,demo_text)

                    # dump
                    json.dump(merged_dict, f_json)
                    
                    # CLOSE json
                    f_json.close()


readDirectory(READ_PATH,"txt")
