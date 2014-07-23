#!/usr/bin/env python


import json
import os,sys,random, datetime

import import_utilities

from pprint import pprint
import re
import codecs

import nltk
from nltk.corpus import stopwords

personal_pronouns = ["i","me","we","us","you","she","her","he","him","it","they","them"]

import time
start_time = time.time()

################## WHEN TESTING CHANGE THIS ##########

type_of_run="ALL"

######################################################

DATA_DIR  =  "../../../../../data/poetryFoundation/"

READ_JSON_DIR =  "json/ALCHEMY_POEMS_JSON_"+type_of_run+"/"
READ_JSON_PATH = DATA_DIR+READ_JSON_DIR

READ_TXT_PATH = "txt_poems_ALL/"

READ_LIST_PATH = DATA_DIR+"NLTK_POS_LISTS_poetryFoundation_POEMs.txt"

the_vowels = ["a","e","i","o","u"]

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
print len(LISTS_ls)
RB=LISTS_ls[1].split(",")
JJ=LISTS_ls[3].split(",")
VBD=LISTS_ls[5].split(",")
VBZ=LISTS_ls[7].split(",")
#FW=LISTS_ls[9].split(",")
#UH=LISTS_ls[11].split(",")
print len(LISTS_ls),len(RB),len(JJ),len(VBD),len(VBZ)

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

print "len(titles_ls):",len(titles_ls)

keywords_dict = {}
concepts_dict = {}
entities_dicti = {}
relation_dict = {}

filenames = []
ALL_poems = "<html xmlns='http://www.w3.org/1999/xhtml'><head>   <title>POEMs on BDP: Big-Data-Poetry</title><style type='text/css'>    body { margin: 40; padding: 20px; width: 85%; font: 14px Helvetica, Arial; }     table { border-collapse: collapse; }     form, td, p { margin: 20; padding: 0; } img { border: none; }  h4  { font: 18px ;}   a { color: #949494; text-decoration: none; } a:hover, .footer a { color: #2c2c2c; text-decoration: underline; }     a:focus { outline: none; }    .white { background: #fff; color: #949494; } .black { background: #121212; color: #949494; } .black a:hover, .black .footer a { color: #ddd; text-decoration: underline; } .header { padding: 70px 0 117px; position: relative;} .header, .footer { width: 750px; margin: 0 auto; } .body { width: 700px; margin: 20 auto; } .switcher { float: right; margin: 43px 0 0 0; cursor: pointer; } .switcher div { float: left; } .rss { float: right; margin-top: -53px;} </style> </head> <body class='white'> <table  width='70%' height='100%' border=0' align='center'> <tr><h1>$$cnt$$ Poems</h1><h2>generated in $$gentime$$ seconds on $$datetime$$</h2>" 
bio=""

num_of_files = 0
cnt=0

RESERVOIR=["Jha"]

#################################################
#                                                 #
#   READ DIRECTORY    #
#                                                 #
#################################################
def extractFeaturesAndWriteBio(READ_PATH,file_type):
    
    

    global ALL_poems,bio,cnt

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

                poem_replaced = ""
                replacement_word = ""
                author=""
                titles=""
                title=""
                new_title=""

                replaced_ls =[]
                new_titles_ls = []
                quit_language=0

                ##########################
                # Load  POEM TEXT FILE     #
                ##########################

                txt_fn_path = DATA_DIR + READ_TXT_PATH + id.split("_")[1]+".txt"
                #print "txt_fn_path:",txt_fn_path

                if os.path.isfile(txt_fn_path) and cnt>2160:
                    txt_data=open(txt_fn_path).read()

                    # http://blog.webforefront.com/archives/2011/02/python_ascii_co.html
                    # txt_data.decode('ISO-8859-2') .decode('utf-8')
                    # unicode(txt_data)

                    author=txt_data.split("****!****")[0].strip(' \t\n\r')
                    
                    title=txt_data.split("****!****")[1].strip(' \t\n\r')
                    
                    bio=txt_data.split("****!****")[2]#.strip(' \t\n\r')

                    ######  CLEAN BIO
                    bio.replace("\t","&#9;")
                    bio.replace("\n"," <br>")
                    bio.replace("\r"," <br>")
                    poem_replaced=bio
                    #print poem_replaced

                    ###############################
                    # REPLACE AUTHOR NAME
                    ##############################
                    author_ln=author.split(" ")[-1]
                    author_fn=author.split(" ")[:-1]
                    #
                    poem_replaced = poem_replaced.replace(author_ln,"Jhave")

                    #######################
                    # replace BOOK TITLES
                    #######################
                    #print "TITLES"]
                    new_title = getNewTitle("title").encode('utf-8')
                             

                    ############################
                    # replace years with another
                    ############################
                    for w1 in poem_replaced.split("("):
                        for w2 in w1.split(")"):
                            if w2 is not None and w2.isdigit():
                                new_num = random.randint(int(w2)-5,int(w2)+5)
                                #print "REPLACING #:",w2,new_num
                                poem_replaced = poem_replaced.replace(w2,str(new_num))
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

                                if content in poem_replaced:
                                                       
                                    ################################################
                                    # Replace similar entities from other JSON     #
                                    ################################################
                                    replacement_entity = findSimilarEntityinRandomJSON(content,entity['type'])

                                    cr = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, replacement_entity)

                                    poem_replaced = poem_replaced.replace(content,replacement_entity)
                                    replaced_ls.append(replacement_entity)
                    

                    ##########################
                    #   POS REPLACMENT       #
                    ##########################

                    token_tuples = nltk.word_tokenize(poem_replaced)
                    tt = nltk.pos_tag(token_tuples)

                    #################
                    #  ADJECTIVES   #
                    #################
                    for i in tt:
                        if "/i" not in i[0] and len(i[0])>3 and i[0] != "died":
                            origw =  re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, i[0])
                            origw =import_utilities.strip_punctuation(origw) 
                            if i[1]=='JJ' :
                                JJr = random.choice(JJ)
                                # # JJr =  re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, JJr)
                                # JJr = import_utilities.strip_punctuation(JJr)
                                JJr = import_utilities.moveBeginAndEndPunctuationFromStrToString(i[0],JJr.lstrip().lstrip())
                                
                                if i[0].istitle():
                                    JJr = JJr.title()

                                poem_replaced = re.sub(r'\b' + import_utilities.strip_punctuation(i[0]) + r'\b', JJr, poem_replaced,1)#poem_replaced.replace(i[0],JJr,1)
                                replaced_ls.append(JJr)
                            if i[1]=='RB':
                                RBr = random.choice(RB)
                                RBr = import_utilities.moveBeginAndEndPunctuationFromStrToString(i[0],RBr.lstrip().lstrip())

                                if i[0].istitle():
                                    RBr = RBr.title()
                                poem_replaced = re.sub(r'\b' + import_utilities.strip_punctuation(i[0])  + r'\b', RBr, poem_replaced,1)
                                replaced_ls.append(RBr)


                    ########################
                    # IS IT ENGLISH?       #
                    ########################
                    for line  in poem_replaced.split('\n\r'):
                        if len(line)>0 :
                            if "english" not in import_utilities.get_language(line):
                                quit_language+=1
                                #print "NOT english:",quit_language,line
                            else:
                                quit_language-=1

                    
                    #########################
                    #   SYNSET REPLACE      #
                    #########################
                    for idx,word in enumerate(poem_replaced.split(' ')):




                        if "<br>" not in word and "&#9;" not in word and len(word)>0:




                            #########################
                            #   PRONOUN ' VERB      #
                            #########################
                            if len(word.split("'"))>1:
                                if word.split("'")[0] in personal_pronouns:
                                    replacement_word = random.choice(personal_pronouns)+"'"+word.split("'")[1]+' '
                                poem_replaced.replace(word,replacement_word)             
                                #print "word,",word,"replacement_word:",replacement_word
                           
                            ####################################################
                            # Replacement of OTHERs                            #
                            ####################################################

                            elif not word.lower().strip(" \n\t\r") in stopwords.words('english'):

                                # take off leading brackets, commas etc...
                                word_punct_nopunct = import_utilities.strip_punctuation_bool(word)
                                word_nopunct = word_punct_nopunct['word'].strip(" \n\t\r")
                                word_punct = word_punct_nopunct['punct']
                                punct_bool = word_punct_nopunct['punct_bool']

                             

                                #######################################################
                                # MAIN EXCHANGE PROCESS CALL >>>>>>>   GET THE SYNSET #
                                #######################################################    
                                if word_nopunct[-4:].lower()=="here":
                                    similarterm=random.choice(import_utilities.heres)
                                else:
                                    #print "WORD:",word_nopunct
                                    similarterm = import_utilities.find_synset_word(word_nopunct)#(word.lstrip().rstrip())

                                
                                ############################################
                                # manually get rid of some terrible choices
                                ############################################
                                if similarterm == "ilk":
                                    ##print "like"
                                    similarterm = "like"
                                if similarterm == "ope":
                                    ##print "doth"
                                    similarterm = "does"

                                #######################################                      
                                # abbreviations for fucking states!   #
                                #######################################
                                if word_nopunct.upper() in import_utilities.state_abbrev and word_nopunct.lower() not in stopwords.words('english') :
                                    tmp = similarterm
                                    if word_nopunct == "oh": 
                                        similarterm = random.choice(import_utilities.exclaims)
                                    else:
                                        similarterm = random.choice(RESERVOIR)
                                    #print word_nopunct," replaced by", tmp, "replaced with:",similarterm, "in:",line

                                ##############
                                # hyphenated #
                                ##############
                                hyp =word.split("-")
                                #print word,len(hyp)
                                if len(hyp) >1:
                                    similarterm=""
                                    for w in hyp:
                                        if len(w) > 2:
                                            similarterm +=  import_utilities.find_synset_word(w)+"-"
                                    similarterm = import_utilities.strip_underscore(similarterm[:-1])
                                    #print "hyphenated:",word,"replaced by: "+similarterm
                                        


                                
                                #########################################################    
                                # is it a TRUNCATED VERB slang as in singin or wishin   #
                                #########################################################
                                if similarterm == word_nopunct and len(word)>2 and 'in' in word_nopunct[-2:]:
                                    similarterm = import_utilities.find_synset_word(word_nopunct+'g')
                                    ## #print "TRUNCATED SLANG word: '"+word+"'",similarterm
                                    interim = import_utilities.lemma(similarterm)
                                    ## #print interim
                                    similarterm = import_utilities.conjugate(interim, tense=import_utilities.PARTICIPLE, parse=True)[:-1] 
                                    # # # #print word,"widx:",widx," line_pos_tags[widx][0]:",line_pos_tags[widx][0]," line_pos_tags[widx][1]:",line_pos_tags[widx][1]
                                   

                                #################      
                                # SWEAR WORD    #
                                #################
                                ##print "at the garden of if:", word
                                if word_nopunct in import_utilities.curses:
                                    similarterm = random.choice(import_utilities.curses)
                                    ##print "SWEAR WORD word: '"+word+"'",similarterm


                                if len(hyp) >1:
                                    replacement_word = similarterm
                                else:
                                    replacement_word = word.replace(word_nopunct, similarterm)
                                    replacement_word = import_utilities.strip_underscore(replacement_word)
                                    replacement_word = import_utilities.replaceNumbers(replacement_word)

                                #########################
                                # RESERVOIR_OF_WEIRDNESS  #
                                #########################  

                                if word_nopunct.lower() in import_utilities.impera:
                                    replacement_word=random.choice(import_utilities.impera)
                                    #print word,"IMPERA:",replacement_word
                                elif word_nopunct.lower() in import_utilities.conjuncts:
                                    replacement_word=random.choice(import_utilities.conjuncts)
                                    #print word," CONJUNCTION replaced with",replacement_word
                                elif word_nopunct.lower() in import_utilities.indef_prono:
                                    replacement_word=random.choice(import_utilities.indef_prono)
                                    #print word," INDEF_prono replaced with",replacement_word
                                elif word_nopunct.lower() in import_utilities.prepo:
                                    replacement_word=random.choice(import_utilities.prepo)
                                    #print word," prepo replaced with",replacement_word
                                elif word_nopunct.lower() in import_utilities.rel_prono:
                                    replacement_word=word
                                    #print word," rel_prono LEAVE alone: ",replacement_word
                                elif word_nopunct.lower()[-2:] =="ly":
                                    replacement_word=import_utilities.strip_underscore(import_utilities.find_synset_word(word))#(word[:-2])
                                    #print word," ADVERB: ",replacement_word
                                    # if replacement_word[-2:] !="ly":
                                    #     replacement_word +="ly"
                                                                            
                                else:
                                    if len(hyp) <2 and "like" not in word_nopunct and import_utilities.singularize(word_nopunct) ==  import_utilities.singularize(replacement_word) and word_nopunct.lower() not in import_utilities.stopwords_ls:

                                        if word_nopunct not in RESERVOIR and quit_language<0 and import_utilities.countPunctuation(word)<1: 
                                            RESERVOIR.append(word)
                                            #print "add to RESERVOIR: ",import_utilities.countPunctuation(word),word,"RESERVOIR:",RESERVOIR
                                        replacement_word = random.choice(RESERVOIR)
                                       # print "'"+word_nopunct+"'  vs RESERVOIR  replacement_word:",replacement_word #,"    new_line:",new_line
                                if quit_language>1:
                                    #print quit_language, "Probably foreign language: make a word salad in english"
                                    replacement_word = random.choice(RESERVOIR)
                                

                                # REPLACEMENT
                                poem_ls = poem_replaced.split(' ')
                                idx =  poem_ls.index(word)


                                # #print idx,",", poem_ls[idx],",", word ,",",replacement_word

                                if poem_ls[idx]==word:
                                    poem_ls[idx]=replacement_word
                                poem_replaced = " ".join(poem_ls)


                                #poem_replaced = poem_replaced.replace(word,replacement_word)



                    # CORRECT the "A" to "An"    
                    for idx,word in enumerate(poem_replaced.split(" ")):
                        # poem_replaced = poem_replaced+"A organism"
                        if len(word)>0 and word[0].lower() in the_vowels and poem_replaced.split(" ")[idx-1].lower() =="a" :      
                                if poem_replaced.split(" ")[idx-1] =="a":
                                    old_str = "a "+poem_replaced.split(" ")[idx]    
                                    new_str = "an "+poem_replaced.split(" ")[idx]
                                else:
                                    old_str = "A "+poem_replaced.split(" ")[idx]    
                                    new_str = "An "+poem_replaced.split(" ")[idx]
                                poem_replaced = poem_replaced.replace(old_str,new_str)

                        # poem_replaced = poem_replaced+"An consonant"
                        if len(word)>0 and word[0].lower() not in the_vowels and poem_replaced.split(" ")[idx-1].lower() =="an" :      
                                if poem_replaced.split(" ")[idx-1] =="an":
                                    old_str = "an "+poem_replaced.split(" ")[idx]    
                                    new_str = "a "+poem_replaced.split(" ")[idx]
                                else:
                                    old_str = "An "+poem_replaced.split(" ")[idx]    
                                    new_str = "A "+poem_replaced.split(" ")[idx]
                                poem_replaced = poem_replaced.replace(old_str,new_str)
                                #print "FOUND correction needed",old_str,new_str


                    #########################
                    #   WRITE SINGLE POEM   #
                    #########################
                    tmp_poem=""   

                    # poem_replaced.replace("\t","&#9;")
                    # poem_replaced.replace("\n"," <br>")
                    # poem_replaced.replace("\r"," <br>")

                    HTML_poem=""
                    for line in poem_replaced.split("\n"):
                        #print "LINE", line
                        HTML_poem += line+"<br>"

                    if len(response) >0 and len(id.split("_"))>1:
                        ALL_poems +="<br><br>~~~~~~~~~~~~~~~~~~~~~~~~~~<br>[ A poem generated from template : <b>"+ author+"</b>, <i>"+ title +"</i> ]<br><br><b>"+new_title+"<br><br></b>"+HTML_poem

                        tmp_poem= "[A poem generated from template: "+ author+", "+ title +"]\n\n"+new_title+"\n\n"+poem_replaced

                        #print tmp_poem
                            #print "\nORIGINAL:",bio

                        txt_fn = id.split("_")[1]+"_POEMs.txt"

                        WRITE_BIO_PATH = DATA_DIR+"generated/POEMS/POEMS_"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"/"
                        if not os.path.exists(WRITE_BIO_PATH):
                                os.makedirs(WRITE_BIO_PATH)

                        txt_fn_path = WRITE_BIO_PATH+txt_fn
                        f_txt=open(txt_fn_path,'w')
                        f_txt.write(tmp_poem)#.encode('utf-8'))       
                        f_txt.close();   
                        print "\nTXT file created at:",txt_fn_path
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





##############################
#    READ DIRECTORY          #
##############################
extractFeaturesAndWriteBio(READ_JSON_PATH,"txt")



# #############################
# # STASH THE DATA           #
# #############################

ALL_poems = ALL_poems.replace("$$datetime$$",datetime.datetime.now().strftime('%Y-%m-%d at %H:%M'))
ALL_poems = ALL_poems.replace("$$cnt$$",str(cnt))
ALL_poems = ALL_poems.replace("$$gentime$$",str(time.time() - start_time))


# ALL POEMS
txt_fn = datetime.datetime.now().strftime('%Y-%m-%d_%H')+"_poetryFoundation_generatedPOEMS_"+type_of_run+".html"
txt_fn_path = DATA_DIR+"generated/POEMS/"+txt_fn
f_txt=open(txt_fn_path,'w')
f_txt.write(ALL_poems+"</hmtl>")       
f_txt.close();   
print "\nTXT file created at:",txt_fn_path


# RESERVOIR
txt_fn = datetime.datetime.now().strftime('%Y-%m-%d_%H')+"_poetryFoundation_RESERVOIR_"+type_of_run+".txt"
txt_fn_path = DATA_DIR+"generated/"+txt_fn
f_txt=open(txt_fn_path,'w')
f_txt.write(", ".join(RESERVOIR))       
f_txt.close();   
print "\nRESERVOIR TXT file created at:",txt_fn_path


print "RESERVOIR:",RESERVOIR


