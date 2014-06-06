#! /usr/bin/env python

import os
import sys

# for parsing html
from bs4 import BeautifulSoup

# for export of labels
import json

DIR = "../../../../data/poetryFoundation/"

 # remove JSON file and begin again
json_fn = "poetryFoundation_JSON.txt"
dir = DIR+'json'
json_fn_path = dir+"/"+json_fn
try:
    if os.path.isfile(json_fn_path):
            os.unlink(json_fn_path)
except Exception, e:
        print e


for root, subFolders, files in os.walk(DIR+"html/"):

        for filename in files:
            
            filePath = os.path.join(root, filename)
            html_num = filename.split(".")[0]
            print "\n",html_num
            
            soup = BeautifulSoup(open(filePath))
            
            poem = soup.find("div", { "class" : "poem" })
            
            pa = soup.select('span.author a')
            
            if pa:
                poem_author = soup.select('span.author a')[0].text
                print 'Author:',poem_author.encode('utf-8')
                title_id = soup.find(id="poem-top")

                poet_DOB = soup.select('span.author span.birthyear')[0].text
                #if poet_DOB.encode('utf-8').split("b. "):
                #    poet_DOB = poet_DOB.encode('utf-8').split("b. ")[1]
                print poet_DOB.encode('utf-8')

                poem_title = title_id.find("h1").text
                print 'Title:',poem_title.encode('utf-8')
                credits = soup.find('div', attrs={'class' : 'credit'})
                if credits:
                    pcred = credits.find("p").text
                    poem_dop = pcred[(pcred.find("Copyright")+12):(pcred.find("Copyright")+16)]
                    print "Published:",poem_dop.encode('utf-8')


               # NOTE: features are stored here
               # in this dict that holds lists of labels
               # QUESTION how-to make it persistent
                categories = {}
                # labels are all within 'about' div
                about = soup.find('div', attrs={'class' : 'about'})
                # nested within their own section
                ps_about = about.find_all('p', attrs={'class' : 'section'})

                for slug in ps_about:
                    labels = slug.find('span', attrs={'class' : 'slug'})

                    if labels.text  != 'Poet':
                        
                        category = labels.text    
                        #print category.encode('utf-8'), ": "

                        # create a list within dict for this category
                        categories[category] = []

                        lbs = labels.find_next_siblings()

                        for lb in lbs:
                            categories[category].append(lb.text)

                        # for cat_label in categories[category]:
                        #     print cat_label.encode('utf-8')

                """
                for key in categories.keys():
                    print("\n"+key.encode('utf-8'))
                    for listt in categories[key]:
                            print(listt)
                """


                # JSON write to json folder

                c_key_valList={}
                cvalues=""

                for k,v in categories.items():
                    print("key: ", k)
                    for cv in v:
                        #print("labels:",cv)
                        cvalues=cvalues+","+cv

                    c_key_valList[k] = cvalues


                #print("labels as list:"+ cvalues)
                print ("c_key_valList:", c_key_valList)

                for key, value in c_key_valList.items():
                    print(k,value)
        """     
                f_json=open(json_fn_path,'a')
            
                print categories
                type(categories)

                json.dump([html_num.encode('utf-8'), { 'Author': poem_author.encode('utf-8').lstrip() } , { 'Title' : poem_title.encode('utf-8') }  , { 'poet_DOB' : poet_DOB.encode('utf-8') } , {'poem_dop' : poem_dop.encode('utf-8')} , {'category':key,"label":value} for key, value in c_key_valList.items() ] , f_json)
              
                f_json.close();
            """
            # # WRITE Poems to txt folder
            # txt_fn = html_num+".txt"
            # #print "TXT Filename: ", txt_fn.encode('utf-8')

            # dir = DIR+'txt'
            # txt_fn_path = dir+"/"+txt_fn
            # # print "TXT Path/Filename: ",txt_fn_path.encode('utf-8')
            # f=open(txt_fn_path,'w+')
            # f.write(poem.text.encode('utf-8').strip())
            # f.close();

            
     
