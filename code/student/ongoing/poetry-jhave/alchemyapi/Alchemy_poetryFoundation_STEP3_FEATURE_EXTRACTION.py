#!/usr/bin/env python

import json
import os,sys

from pprint import pprint

type_of_run="6"

######################################################

DATA_DIR  =  "../../../../../data/poetryFoundation/"

READ_JSON_DIR =  "json/ALCHEMY_BIOS_JSON_"+type_of_run+"/"
READ_JSON_PATH = DATA_DIR+READ_JSON_DIR

READ_TXT_PATH = "txt_bios_ALL/"

#################################################
#                                                 #
#   READ FILES, extract features, WRITE to json     #
#                                                 #
#################################################
def readDirectory(READ_PATH,file_type):
    
    cnt=0
    print ('readDirectory',READ_PATH)

    for subdir, dirs, files in os.walk(READ_PATH):
        for file in files:

            if file_type in file  and 'readme' not in file:

                # ID
                id=file.split(".")[0]

                cnt+=1

                print('')
                print('')
                print('OPENED:',id)
                print('')
                print('')

            
                #################
                # Load JSON     #
                #################

                json_data=open(READ_PATH+file)
                response = json.load(json_data)

                #pprint(response)
                json_data.close()   

                if response['status'] == 'OK':
                    print('## Response Object ##')
                    #print(json.dumps(response, indent=4))

                    print('')

                    print('## Keywords ##')
                    for keyword in response['keywords']:
                        print(keyword['text'], ' : ', keyword['relevance'])
                    print('')

                    print('## Concepts ##')
                    for concept in response['concepts']:
                        print(concept['text'], ' : ', concept['relevance'])
                    print('')

                    print('## Entities ##')
                    for entity in response['entities']:
                        print(entity['type'], ' : ', entity['text'], ', ', entity['relevance'])
                    print(' ')

                else:
                    print('Error in combined call: ', response['statusInfo'])

                if response['status'] == 'OK':
                    print('## Object ##')
                    #print(json.dumps(response, indent=4))

                    print('')
                    print('## Relations ##')
                    for relation in response['relations']:
                        if 'subject' in relation:
                            print('Subject: ', relation['subject']['text'].encode('utf-8'))

                        if 'action' in relation:
                            print('Action: ', relation['action']['text'].encode('utf-8'))

                        if 'object' in relation:
                            print('Object: ', relation['object']['text'].encode('utf-8'))

                        print('')
                else:
                    print('Error in relation extaction call: ', response['statusInfo'])



                ##########################
                # Load BIO TEXT FILE     #
                ##########################

                txt_fn_path = DATA_DIR + READ_TXT_PATH + id.split("_")[1]+".txt"
                print "txt_fn_path:",txt_fn_path

                txt_data=open(txt_fn_path).read()
                author=txt_data.split("****!****")[0].strip(' \t\n\r')

                bio=txt_data.split("****!****")[1].strip(' \t\n\r')
                print "author:",author,"\nbio",bio


                #############################
                # GENERATE A BIO            #
                #############################
                #   OR  ...
                #############################
                # STASH THE DATA           #
                #############################




##############################
#    READ DIRECTORY          #
##############################
readDirectory(READ_JSON_PATH,"txt")





   
