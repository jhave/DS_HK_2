import matplotlib.pyplot as plt
import os, datetime


type_of_run="ALL"
READ_PATH = "../../../../../data/poetry/ohhla/ohhla_txt_files_"+type_of_run+"/"
WRITE_PATH = "../../../../../data/poetry/ohhla/txt_poems_"+type_of_run+"/"


for subdir, dirs, files in os.walk(READ_PATH):
    for file in files:
        if ".txt" in file  and 'readme' not in file:
            if os.path.isfile(subdir+file):
                #print subdir+file
                with open(subdir+file) as infile:
                    with open(WRITE_PATH+file,"w") as outfile:
                        for i,line in enumerate(infile):
                            if i == 0 :
                                line = ""
                                
                            if i==1 or i==2 or i==3 or i==4:
                                #l=line.split(":")
                                #outfile.write(l[1].strip()+"\n****!****\n")
                                outfile.write(line+"****!****\n")
                            else:
                                outfile.write(line)
