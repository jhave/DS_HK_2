#!/usr/bin/env python


import json
import os,sys,random

import import_utilities

from pprint import pprint
import re

type_of_run="6"

######################################################

DATA_DIR  =  "../../../../../data/poetryFoundation/"

READ_JSON_DIR =  "json/ALCHEMY_BIOS_JSON_"+type_of_run+"/"
READ_JSON_PATH = DATA_DIR+READ_JSON_DIR

READ_TXT_PATH = "txt_bios_ALL/"


# list of json files returned from Alchemy (without .DS_Store or system files)
json_files=[]
json_files_shuffled = []

# list of file names to be accessed randomly
for item in os.listdir(READ_JSON_PATH):
    if not item.startswith('.') and os.path.isfile(os.path.join(READ_JSON_PATH, item)):
        json_files.append(item)
random.shuffle(json_files)
json_files_shuffled = json_files

# list of other titles as source for making new titles
titles_ls=open(DATA_DIR+ "ALL_poetryFoundation_BIO_ALL_TITLES.txt",'r').read().split(" !~*~! ")

keywords_dict = {}
concepts_dict = {}
entities_dicti = {}
relation_dict = {}

filenames = []
ALL_bios = ""
bio=""

num_of_files = 0

#################################################
#                                                 #
#   READ DIRECTORY    #
#                                                 #
#################################################
def extractFeatures(READ_PATH,file_type):
    
    cnt=0
    

    global ALL_bios,bio

    for subdir, dirs, files in os.walk(READ_PATH):
        for file in files:
            
            num_of_files = len(files)-1 # deduct the DS_store
            print (num_of_files,'readDirectory',READ_PATH)
            
            if file_type in file  and 'readme' not in file:

                # ID
                id=file.split(".")[0]

                filenames.append(id)
                cnt+=1

                print('')
                print('')
                print('OPENED:',id)
                print('')
                print('')

                bio_replaced = ""
                author=""
                titles=""

                ##########################
                # Load BIO TEXT FILE     #
                ##########################

                txt_fn_path = DATA_DIR + READ_TXT_PATH + id.split("_")[1]+".txt"
                print "txt_fn_path:",txt_fn_path

                txt_data=open(txt_fn_path).read()
                author=txt_data.split("****!****")[0].strip(' \t\n\r')
                titles=txt_data.split("****!****")[1].strip(' \t\n\r').split(" !~*~! ")
                titles[-1]  = titles[-1].strip(" !~*~!")
                bio=txt_data.split("****!****")[2].strip(' \t\n\r')

                ###############################
                # REPLACE AUTHOR NAME
                ##############################
                author_ln=author.split(" ")[-1]
                author_ln=author.split(" ")[-1]
                author_fn=author.split(" ")[:-1]
                # 
                for word in bio.split(" "):
                    if author in word:
                        word=word.replace(author,"David Jhave Johnston")
                    if author_ln in word:
                        word=word.replace(author_ln,"Jhave")

                    bio_replaced += word+" "
                    wrong_name = " ".join(author_fn)+" Jhave"
                bio_replaced = bio_replaced.replace(wrong_name,"Jhave")
                
                #######################
                # replace BOOK TITLES
                #######################
                print "TITLES"
                for t in titles:
                    if t in bio_replaced and t != ".":
                        print t
                        bio_replaced = bio_replaced.replace(t,getNewTitle(t))

                #######################
                # replace She with He
                #######################
                bio_replaced = bio_replaced.replace("She ","He ")
                bio_replaced = bio_replaced.replace(" she"," he ")
                bio_replaced = bio_replaced.replace("Her ","His ")
                bio_replaced = bio_replaced.replace(" her"," his")
                                            
                                           

                #################
                # Load JSON     #
                #################
                response = loadJSONfile(READ_JSON_PATH+"poetryFoundation_"+id.split("_")[1]+"_Alchemy_JSON.txt")


                for idx,entity in enumerate(response['entities']):

                    #print idx
                    ce = entity['text'].replace("0xc2"," ")
                    ce = ce.replace("0xe2","'")
                    ce = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, ce)
                    # print "entity['text']",entity['text'].encode('utf-8')

                    #print bio_replaced
                    #print ce.encode('utf-8')
                    ce = ce.encode('utf-8')

                    try:
                        content = ce.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
                    except UnicodeDecodeError:
                        "AAAARGGGGHHH!!!!"
                    

                    if content in bio_replaced:
                                           
                        ################################################
                        # Replace similar entities from other JSON     #
                        ################################################
                        replacement_entity = findSimilarEntityinRandomJSON(content,entity['type'])
                        bio_replaced = bio_replaced.replace(content.encode('utf-8'),replacement_entity.encode('utf-8'))
                
                









                ALL_bios +="\n\n~\n\n"+bio_replaced
                

                print "\n\n**** ",author,"\n\nbio_replaced:",bio_replaced,"\n\nbio",bio








#################
# get NEW title    #
#################

def getNewTitle(old_title):

    return random.choice(titles_ls)



#################
# Load JSON     #
#################

def loadJSONfile(fn):

    id=fn.split(".")[0]
    print "Inside loadJSONfile id=",id

    json_data=open(fn)
    response = json.load(json_data)

    #pprint(response)
    json_data.close()   

    # if response['status'] == 'OK': 

    #     print('## Response Object ##')
    #     print(json.dumps(response, indent=4))

       
    #     print('')

    #     # print('## Keywords ##')
    #     for keyword in response['keywords']:
    #         print(keyword['text'], ' : ', keyword['relevance'])
    #         #keywords_dict [keyword['text']] = keyword['relevance']
    #     # print('')

    #     # print('## Concepts ##')
    #     for concept in response['concepts']:
    #         print(concept['text'], ' : ', concept['relevance'])
    #         #concepts_dict [concept['text']] = concept['relevance']
    #     # print('')

    #     # print('## Entities ##')
    #     # for idx,entity in enumerate(response['entities']):
    #     #     #entities_dict [entity['type']] = concept['relevance']
    #     #     # entities_dicti[id.split("_")[1]+"_"+str(idx)] = { 'type' : entity['type'] , 'text':entity['text'] , 'relevance': entity['relevance'] }

    #     #     #print(id.split("_")[1]+"_"+str(idx),

    #     #     print (entity['type'], ' : ', entity['text'], ', ', entity['relevance'])
    #     # print(' ')

    # else:
    #     print('Error in combined call: ', response['statusInfo'])

    # if response['status'] == 'OK':
    #     print('## Object ##')
    #     #print(json.dumps(response, indent=4))

    #     print('')
    #     print('## Relations ##')
    #     for relation in response['relations']:
    #         if 'subject' in relation:
    #             print('Subject: ', relation['subject']['text'].encode('utf-8'))

    #         if 'action' in relation:
    #             print('Action: ', relation['action']['text'].encode('utf-8'))

    #         if 'object' in relation:
    #             print('Object: ', relation['object']['text'].encode('utf-8'))

    #         print('')
    # else:
    #     print('Error in relation extaction call: ', response['statusInfo'])


    return response

   
def findSimilarEntityinRandomJSON(orig,typ):

    not_found=True
    cnt =-1
    random.shuffle(json_files)

    #print "ENTERING findSimilarEntityinRandomJSON",orig,typ

    while (not_found):

        cnt+=1
        if cnt>len(json_files)-1:
            cnt=0
            #print "EXITING find Similar Without FINDING"
            break

        fn = READ_JSON_PATH+json_files[cnt]
        #print "findSimilarEntityinRandomJSON in fn=",fn

        json_data=open(fn)
        response = json.load(json_data)
        json_data.close() 

        random.shuffle(response['entities'])
        for idx,entity in enumerate(response['entities']):
            if orig.encode('utf-8') not in entity['text'].encode('utf-8')  and entity['type']==typ:
                print orig.encode('utf-8') ,"::",entity['text'].encode('utf-8')
                return entity['text'] 

    return "**** DID NOT FIND"+typ+" ****"




#############################
# GENERATE A BIO            #
#############################

def GenerateBio():
    print "GenerateBio"

    """
    TEMPLATE METHOD

    Born in {Entities:StateOrCounty or Entities:City} in {range 1950-1980}, Jhave has {worked with,collaborated with, been friends with, studied}{several random Entities:Person}. Originally educated at {Entities:Organization}, Jhave is currently {Entities:JobTitle} at {Entities:Organization}. He lives in {Entities:StateOrCountry}. 

    {His works include, He is the author of} {find a book title, mutate it}{(range birthyear+16 to currentyear+1)}. He has {published, written, released, produced, created} {random number range 1-10} [books, novels, collections, chapbooks, novellas, essays]{among them, some, } are {comma seperated list of other book titles}. 
    {Affiliations:, His poems have appeared in, Contributions can be found in,}  {comma-seperated list of Entities:PrintMedia}

    """





#   &  ...
#############################
# STASH THE DATA           #
#############################




##############################
#    READ DIRECTORY          #
##############################
extractFeatures(READ_JSON_PATH,"txt")

"""


bio_replaced: James Doyle    
                        Jhave was born in Durham, Colorado, and grew up in Fort Collins, Durham, and Colorado, Wisconsin. He did graduate work in philosophy at the University of Wisconsin and earned an MFA from the Kennedy Center at Durham. Jhave was the daughter of violinists, and his early exposure to music has had a profound affect on his work, which ranges in genre from poetry to novels to short fiction to memoir to criticism. In an interview with Kelly Cherry, Jhave noted that “musical dynamics, phrasing, pitch, tone, texture, orchestration The Psalms of David Imitated in the Language of the New Testament. provide inspiration, and sometimes a model, for a poet, as do the lives of some composers.”   Jhave is the author of more than 20 books and chapbooks of writing. His collections of poetry include The Prince’s Progress and Other Poems(1980), Paradise & Method: Poetics & Praxis(1993), The New Life(1997), Philip Larkin.(2002), (1997),(2007), and This Lamentable City(2009). His works of fiction include  London Review of Books(1974); Morning Run(1983); Poche Osservazioni(1999), which won the Dictionary of Literary Biography Award for Short Fiction; Asian American Poetry: The Next Generation (2003); and Waves(2010). An accomplished Evjue-Bascom Professor Emerita of nonfiction, Jhave has also published memoirs, including Daisy Miller(1991), and essay collections, such as Beginning to Heal: A First Book for Men and Women Who Were Sexually Abused as Children  (2009). He has also published two translations of ancient Greek drama.   The recipient of numerous honors and awards, Jhave was named the poet laureate of Wisconsin in 2010. He has received fellowships from the John the Baptist, the John the Baptist for the Arts, the Penn State University, and New York City. He taught at the University of Wisconsin–Madison for more than 20 years. He retired in 1999 but still holds the positions of the assistant professor and the Director’s Visitor in the Humanities. The inaugural recipient of the Hanes Poetry Prize and the Kennedy Center, Jhave was a Director’s Visitor at the Duke University Press at Greensboro in 2010. He lives on a small farm in Wisconsin with his husband, the fiction Evjue-Bascom Professor Emerita Gayle Danley.  

bio Meg Theno    
                        Kelly Cherry was born in Baton Rouge, Louisiana, and grew up in Ithaca, New York, and Chesterfield County, Virginia. She did graduate work in philosophy at the University of Virginia and earned an MFA from the University of North Carolina at Greensboro. Cherry was the daughter of violinists, and her early exposure to music has had a profound affect on her work, which ranges in genre from poetry to novels to short fiction to memoir to criticism. In an interview with Kaite Hillenbrand, Cherry noted that “musical dynamics, phrasing, pitch, tone, texture, orchestration et al. provide inspiration, and sometimes a model, for a poet, as do the lives of some composers.”   Cherry is the author of more than 20 books and chapbooks of writing. Her collections of poetry include Songs for a Soviet Composer (1980), God’s Loud Hand (1993), Death and Transfiguration (1997), Rising Venus (2002), Hazard and Prospect: New and Selected Poems (2007), and The Retreats of Thought: Poems (2009). Her works of fiction include Sick and Full of Burning (1974); In the Wink of an Eye (1983); The Society of Friends (1999), which won the Dictionary of Literary Biography Award for Short Fiction; We Can Still Be Friends (2003); and The Woman Who (2010). An accomplished writer of nonfiction, Cherry has also published memoirs, including The Exiled Heart (1991), and essay collections, such as Girl in a Library: On Women Writers & the Writing Life (2009). She has also published two translations of ancient Greek drama.   The recipient of numerous honors and awards, Cherry was named the poet laureate of Virginia in 2010. She has received fellowships from the Rockefeller Foundation, the National Endowment for the Arts, the Ragdale Foundation, and Yaddo. She taught at the University of Wisconsin–Madison for more than 20 years. She retired in 1999 but still holds the positions of the Eudora Welty Professor Emerita of English and the Evjue-Bascom Professor Emerita in the Humanities. The inaugural recipient of the Hanes Poetry Prize and the Ellen Anderson Award, Cherry was a Director’s Visitor at the Institute for Advanced Study at Princeton in 2010. She lives on a small farm in Virginia with her husband, the fiction writer Burke Davis III.


"""

