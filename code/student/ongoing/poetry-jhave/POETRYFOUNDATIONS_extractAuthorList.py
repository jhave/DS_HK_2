
#!/usr/bin/env python

"""

1. 
Load all txt files in "txt" folder from poetryfoundation.org

2.
Create one string. Save to file.

2.
Check for collocations. Save results to file.

"""



import os, datetime
import sys

# SOURCE files
type_of_run="ALL"

DATA_DIR  =  "../../../../data/poetryFoundation/"
READ_TXT_DIR = "txt_poems_"+type_of_run+"/"
READ_PATH=DATA_DIR+READ_TXT_DIR

WRITE_PATH = DATA_DIR+"ALL/"
WRITE_ALL_PATH = DATA_DIR+"ALL/"+type_of_run+"_AUTHORS_poetryFoundation_POEMS.txt"


ALL_poems=""

#################################################
#                                               #
#   READ FILES, CALL Alchemy, WRITE to json     #
#                                               #
#################################################
def readDirectory(PATH,file_type):
    
    cnt=0
    global ALL_poems
    #print "read", PATH

    for subdir, dirs, files in os.walk(PATH):

        #print subdir,dirs,files

        for file in files:

            #print file

            if file_type in file  and 'readme' not in file:

                # ID
                id=file.split(".")[0]
                print ("id:",cnt,id)

                cnt+=1

                # 
                if cnt>0 and cnt<11000:

                    # READ txt file
                    pf = open(subdir+file, 'r')
                    demo_text = pf.read()
                    pf.close()

                    ALL_poems += demo_text.split("****!****")[0].strip(' \t\n\r').replace("  "," ")+" ~!~ "


    # CREATE dir
    if not os.path.exists(WRITE_PATH):
        os.makedirs(WRITE_PATH)

    ##############################
    # END with writing           #
    ##############################
    #print ALL_poems
    all_ls=ALL_poems.split("~!~")
    all_ls= set(all_ls)
    ALL_poems=" ~!~ ".join(w for w in all_ls)

    wf = open(WRITE_ALL_PATH, 'w')
    wf.write(ALL_poems)
    wf.close()
                  
##############################
# START with writing         #
##############################
print READ_PATH
readDirectory(READ_PATH,"txt")
print ALL_poems

