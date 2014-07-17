#!/usr/bin/env python


import json
import os,sys,random, datetime

import import_utilities

from pprint import pprint
import re
import codecs

type_of_run="ALL"

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
titles_ls=codecs.open(DATA_DIR+ "ALL_poetryFoundation_BIO_ALL_TITLES.txt",'r',encoding='utf-8').read().split(" !~*~! ")

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
def extractFeaturesAndWriteBio(READ_PATH,file_type):
    
    cnt=0
    

    global ALL_bios,bio

    for subdir, dirs, files in os.walk(READ_PATH):
        for file in files:
            
            num_of_files = len(files)-1 # deduct the DS_store
            #print (num_of_files,'readDirectory',READ_PATH)
            
            if file_type in file  and 'readme' not in file:

                # ID
                id=file.split(".")[0]

                filenames.append(id)
                cnt+=1

                # print('')
                # print('')
                # print('OPENED:',id)
                # print('')
                # print('')

                bio_replaced = ""
                author=""
                titles=""

                ##########################
                # Load BIO TEXT FILE     #
                ##########################

                txt_fn_path = DATA_DIR + READ_TXT_PATH + id.split("_")[1]+".txt"
                #print "txt_fn_path:",txt_fn_path

                txt_data=open(txt_fn_path).read()

                # http://blog.webforefront.com/archives/2011/02/python_ascii_co.html
                # txt_data.decode('ISO-8859-2') .decode('utf-8')
                # unicode(txt_data)

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
                #print "TITLES"
                for t in titles:
                    if t in bio_replaced and t != ".":
                        #print t#.decode('utf-8')
                        bio_replaced = bio_replaced.replace(t,getNewTitle(t).encode('utf-8'))

                #######################
                # replace She with He
                #######################
                bio_replaced = bio_replaced.replace("She ","He ")
                bio_replaced = bio_replaced.replace(" she"," he ")
                bio_replaced = bio_replaced.replace("Her ","His ")
                bio_replaced = bio_replaced.replace(" her"," his")
                bio_replaced = bio_replaced.replace(" husband"," wife")

                ############################
                # replace years with another
                ############################
                for w1 in bio_replaced.split("("):
                    for w2 in w1.split(")"):
                        if w2 is not None and w2.isdigit():
                            new_num = random.randint(int(w2)-5,int(w2)+5)
                            #print "REPLACING #:",w2,new_num
                            bio_replaced = bio_replaced.replace(w2,str(new_num))                            
                                           

                #################
                # Load JSON     #
                #################
                response = loadJSONfile(READ_JSON_PATH+"poetryFoundation_"+id.split("_")[1]+"_Alchemy_JSON.txt")

                if response.get('entities') is not None:
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

                            #replacement_entity.decode('utf-8')
                            #unicode(replacement_entity)
                            cr = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, replacement_entity)

                            bio_replaced = bio_replaced.replace(content,replacement_entity)
            
                    
                if len(response) >0:
                    ALL_bios +="\n\n~\n\n"+bio_replaced#.encode('utf-8','ignore')
                    # print "\n\n",author
                    print "based on:", author
                    print "\n~~~~~~\n\n", bio_replaced
                    # print "\n\nbio",bio

                    txt_fn = type_of_run+"_poetryFoundation_generatedBIOs.txt"

                    # WRITE_BIO_PATH = DATA_DIR+"generated"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"/"
                    # if not os.path.exists(WRITE_BIO_PATH):
                    #         os.makedirs(WRITE_BIO_PATH)

                    # txt_fn_path = WRITE_BIO_PATH+txt_fn
                    # f_txt=open(txt_fn_path,'w')
                    # f_txt.write(bio_replaced.encode('utf-8'))       
                    # f_txt.close();   
                    # print "\nTXT file created at:",txt_fn_path
                else:
                    "~~~~~~~~~~~~~~~~!!!!!!!!!! EMPTY response:", author






#################
# get NEW title    #
#################

def getNewTitle(old_title):
    new_title=""
    total_str = random.choice(titles_ls)+ " "+random.choice(titles_ls)+ " "+random.choice(titles_ls)
    total = total_str.split(' ')
    random.shuffle(total)
    for w in total:
        if total.index(w)%3:
            new_title += w +" " 

    #print old_title,"::", new_title
    return new_title



#################
# Load JSON     #
#################

def loadJSONfile(fn):

    id=fn.split(".")[0]
    #print "Inside loadJSONfile id=",id

    json_data=open(fn)
    response = json.load(json_data)

    #pprint(response)
    json_data.close()   

    return response

#############################
# find Similare entities    #
#############################
def findSimilarEntityinRandomJSON(orig,typ):

    not_found=True
    cnt =-1
    

    #print "ENTERING findSimilarEntityinRandomJSON",orig,typ

    while (not_found):

        cnt+=1
        if cnt>len(json_files)-1:
            cnt=0
            random.shuffle(json_files)
            #print "EXITING find Similar Without FINDING"
            break

        fn = READ_JSON_PATH+json_files[cnt]
        

        json_data=open(fn)
        response = json.load(json_data)
        json_data.close() 

        #print "findSimilarEntityinRandomJSON in fn=",fn,len(response)
        
        if response.get('entities') is not None:
            random.shuffle(response['entities'])
            for idx,entity in enumerate(response['entities']):
                if orig.encode('utf-8') not in entity['text'].encode('utf-8')  and entity['type']==typ:
                    #print orig.encode('utf-8') ,"::",entity['text'].encode('utf-8')

                    ce = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, entity['text'])
                    return ce.encode('utf-8')
        else:
            print "entities response empty?",random.shuffle(json_files)

    return "**** DID NOT FIND ****"




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


    STRATEGY


    """






##############################
#    READ DIRECTORY          #
##############################
extractFeaturesAndWriteBio(READ_JSON_PATH,"txt")



# #   &  ...
# #############################
# # STASH THE DATA           #
# #############################
txt_fn = type_of_run+"_"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"_poetryFoundation_generatedBIOs.txt"
txt_fn_path = DATA_DIR+"generated/"+txt_fn
f_txt=open(txt_fn_path,'w')
f_txt.write(ALL_bios)       
f_txt.close();   
print "\nTXT file created at:",txt_fn_path


