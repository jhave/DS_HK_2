#!/usr/bin/env python


import json
import os,sys,random, datetime

import import_utilities

from pprint import pprint
import re
import codecs

import nltk
from nltk.corpus import stopwords

# import simplejson as json

################## WHEN TESTING CHANGE THIS ##########

type_of_run="ALL"

######################################################

DATA_DIR  =  "../../../../../data/poetryFoundation/"

READ_JSON_DIR =  "json/ALCHEMY_BIOS_JSON_"+type_of_run+"/"
READ_JSON_PATH = DATA_DIR+READ_JSON_DIR

READ_TXT_PATH = "txt_bios_ALL/"

READ_LIST_PATH = DATA_DIR+"NLTK_POS_LISTS_poetryFoundation_BIOs.txt"

# adjectives (JJ), adverbs (RB), foreign words (FW), interjection (UH)
JJ = []
RB = []
FW = []
UH = []
VBD = []
VBZ = []

#################################################
#                                                 #
#   READ NLTK LISTS
#                                                 #
#################################################

list_data=open(READ_LIST_PATH).read()
LISTS_ls = list_data.split("=")
RB=LISTS_ls[1].split(",")
JJ=LISTS_ls[3].split(",")
VBD=LISTS_ls[5].split(",")
VBZ=LISTS_ls[7].split(",")
FW=LISTS_ls[9].split(",")
UH=LISTS_ls[11].split(",")

#print JJ

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
for t in titles_ls:
    # import_utilities.strip_punctuation(t)
    if t.count(" ") > len(t)/2  or " , " in t:
        titles_ls.remove(t)
        # print "removing '"+t+"'"
    if t in import_utilities.stopwords_ls:
        titles_ls.remove(t)
        #print "removing '"+t+"'"

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
                print "\n\n*********\nID:",id

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

                replaced_ls =[]
                new_titles_ls = []

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

                ######  CLEAN BIO
                #bio =  re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, bio)

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
                replaced_ls.append(author)


                #######################
                # replace BOOK TITLES
                #######################
                #print "TITLES"]
                for t in titles:
                    if (t.count(" ") > len(t)/3) or (len(t)<5 and t.count(" ") > 3):
                        titles.remove(t)
                        #print "removing '"+t+"'"
                if len(titles)>1:
                    for t in titles:
                        if t in bio_replaced and t != "." and t != " "  and t != "  " and len(t)>3:
                            nt = getNewTitle(t).encode('utf-8')
                           
                            #bio_replaced = re.sub(r'\b' +t  + r'\b', "<i>"+nt+"</i>", bio_replaced)

                            nti="<i> "+nt+" </i>"
                            bio_replaced = bio_replaced.replace(t, nti)
                            #print t, nti
                            replaced_ls.append(nt)
                            new_titles_ls.append(nt)

                #######################
                # replace She with He
                #######################
                # bio_replaced = bio_replaced.replace("She ","He ")
                # bio_replaced = bio_replaced.replace(" she"," he ")
                # bio_replaced = bio_replaced.replace("Her ","His ")
                # bio_replaced = bio_replaced.replace(" her "," his ")
                # bio_replaced = bio_replaced.replace(" husband"," wife")

                ############################
                # replace years with another
                ############################
                for w1 in bio_replaced.split("("):
                    for w2 in w1.split(")"):
                        if w2 is not None and w2.isdigit():
                            new_num = random.randint(int(w2)-5,int(w2)+5)
                            #print "REPLACING #:",w2,new_num
                            bio_replaced = bio_replaced.replace(w2,str(new_num))
                            replaced_ls.append(new_num)                            
                                           

                #################
                # Load JSON     #
                #################
                response = loadJSONfile(READ_JSON_PATH+"poetryFoundation_"+id.split("_")[1]+"_Alchemy_JSON.txt")

                if response != "failed":

                    if response.get('entities') is not None:
                        for idx,entity in enumerate(response['entities']):

                            #print idx
                            ce = entity['text'].replace("0xc2"," ")
                            ce = ce.replace("0xe2","'")
                            ce = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, ce)
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

                                cr = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, replacement_entity)

                                bio_replaced = bio_replaced.replace(content,replacement_entity)
                                replaced_ls.append(replacement_entity)
                
                # if response.get('relations') is not None:
                #     for idx,relation in enumerate(response['relations']):
                #         if 'subject' in relation:
                #             print('Subject: ', relation['subject']['text'].encode('utf-8'))

                #         if 'action' in relation:
                #             print('Action: ', relation['action']['text'].encode('utf-8'))

                #         if 'object' in relation:
                #             print('Object: ', relation['object']['text'].encode('utf-8'))

                ##########################
                #   POS REPLACMENT       #
                ##########################

                token_tuples = nltk.word_tokenize(bio_replaced)
                tt = nltk.pos_tag(token_tuples)

                #################
                #  ADJECTIVES   #
                #################
                for i in tt:
                    if "/i" not in i[0] and len(i[0])>3:
                        origw =  re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, i[0])
                        origw =import_utilities.strip_punctuation(origw) 
                        if i[1]=='JJ':
                            JJr = random.choice(JJ)
                            # # JJr =  re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, JJr)
                            # JJr = import_utilities.strip_punctuation(JJr)
                            JJr = import_utilities.moveBeginAndEndPunctuationFromStrToString(i[0],JJr.lstrip().lstrip())
                            
                            if i[0].istitle():
                                JJr = JJr.title()

                            bio_replaced = re.sub(r'\b' + import_utilities.strip_punctuation(i[0]) + r'\b', JJr, bio_replaced,1)#bio_replaced.replace(i[0],JJr,1)
                            replaced_ls.append(JJr)
                        if i[1]=='RB':
                            RBr = random.choice(RB)
                            RBr = import_utilities.moveBeginAndEndPunctuationFromStrToString(i[0],RBr.lstrip().lstrip())

                            if i[0].istitle():
                                RBr = RBr.title()
                            bio_replaced = re.sub(r'\b' + import_utilities.strip_punctuation(i[0])  + r'\b', RBr, bio_replaced,1)
                            replaced_ls.append(RBr)



                #######################################################
                # MAIN EXCHANGE PROCESS CALL >>>>>>>   GET WN SYNSET #
                #######################################################  
                # for w in bio_replaced.split(" "):

                #     print "W:",w

                #     if w not in replaced_ls and len(w)>4 and w not in import_utilities.stopwords_ls and w not in new_titles_ls:

                #         word_nopunct = import_utilities.strip_punctuation(w)

                #         if word_nopunct[-4:].lower()=="here":
                #             similarterm=random.choice(import_utilities.heres)
                #         else:
                #             #print "WORD:",word_nopunct
                #             similarterm = import_utilities.find_synset_word(word_nopunct)

                #         similarterm = import_utilities.moveBeginAndEndPunctuationFromStrToString(w,similarterm.lstrip().lstrip())
                #         print w," SIMILAR to ",similarterm
                #         bio_replaced = bio_replaced.replace(" "+w," "+similarterm)

                                            

                #         #print idx
                #         ce = entity['text'].replace("0xc2"," ")
                #         ce = ce.replace("0xe2","'")
                #         ce = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, ce)
                #         ce = ce.encode('utf-8')

                #         try:
                #             content = ce.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
                #         except UnicodeDecodeError:
                #             "AAAARGGGGHHH!!!!"

                #         if content in bio_replaced:
                                               
                #             ################################################
                #             # Replace similar entities from other JSON     #
                #             ################################################
                #             replacement_entity = findSimilarEntityinRandomJSON(content,entity['type'])

                #             cr = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, replacement_entity)

                #             bio_replaced = bio_replaced.replace(content,replacement_entity)

                    
                if len(response) >0:
                    ALL_bios +="<br><br>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>[ A bio generated from : "+ author+" ]<br><br>"+bio_replaced

                    print "<br><br>~~~~~~~~~~~~~~~~~~~~~~~~~~<br>[ A bio generated from : "+ author+" ]<br><br>"
                    print bio_replaced

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
    total_str = random.choice(titles_ls)+ " "+random.choice(titles_ls)+ " "+import_utilities.strip_punctuation(random.choice(titles_ls))
    total = total_str.split(' ')
    random.shuffle(total)
    for w in total:
        if total.index(w)%3:
            new_title += w +" " 

    new_title = " ".join(w for w in new_title.split(" ") if " , " not in w)

    new_title = new_title.replace("Review","")

    new_title = ' '.join(unique_list(new_title.split()))
    # check last word
    if new_title.lower().split(" ")[-1] in import_utilities.stopwords_ls:
        new_title = new_title.rsplit(' ', 1)[0]
    
    # 
    new_title = new_title.rsplit(' ', 1)[0] +" "+ new_title.split(" ")[-1].rstrip(",:;").title()
    return new_title

##################
# remove repeat words
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist and x not in import_utilities.stopwords_ls]
    return ulist

#################
# Load JSON     #
#################

def loadJSONfile(fn):

    id=fn.split(".")[0]
    #print "Inside loadJSONfile id=",id

    try:
        json_data=open(fn)
        response = json.load(json_data)
        json_data.close()   

        return response

    except ValueError:
        print "############# decoding JSON failed",fn
        pass

    return "failed"
    

#############################
# find Similare entities    #
#############################
def findSimilarEntityinRandomJSON(orig,typ):

    not_found=True
    cnt =-1
    
    random.shuffle(json_files)
    #print "\nENTERING findSimilarEntityinRandomJSON",orig,typ

    while (not_found):

        cnt+=1
        if cnt>len(json_files)-1:
            cnt=0
            
            #print "EXITING find Similar Without FINDING"
            break

        fn = READ_JSON_PATH+json_files[cnt]
        
        try:
            json_data=open(fn)
            response = json.load(json_data)
            json_data.close() 

        except ValueError:
            print "############# decoding JSON failed",fn
            response = "failure"
            pass



        #print "findSimilarEntityinRandomJSON in fn=",fn,len(response)
        
        if response != "failure" and response.get('entities') is not None:
            random.shuffle(response['entities'])
            for idx,entity in enumerate(response['entities']):
                if orig.encode('utf-8') not in entity['text'].encode('utf-8')  and entity['type']==typ:
                    #print orig.encode('utf-8') ,"::",entity['text'].encode('utf-8')

                    ce = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, entity['text'])
                    return ce.encode('utf-8')
        else:
            pass
            #print "entities response empty?",random.shuffle(json_files)

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
txt_fn = type_of_run+"_ITALICIZED_"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"_poetryFoundation_generatedBIOs.txt"
txt_fn_path = DATA_DIR+"generated/"+txt_fn
f_txt=open(txt_fn_path,'w')
f_txt.write(ALL_bios)       
f_txt.close();   
print "\nTXT file created at:",txt_fn_path


