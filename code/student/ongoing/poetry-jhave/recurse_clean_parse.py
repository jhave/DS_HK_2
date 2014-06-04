#! /usr/bin/env python

import os
import sys

from bs4 import BeautifulSoup

DIR = "../../../../data/poetryFoundation/"

for root, subFolders, files in os.walk(DIR):

        for filename in files:
            
            filePath = os.path.join(root, filename)
            print "\n",filename.split(".")[0]
            
            soup = BeautifulSoup(open(filePath))
            
            poem = soup.find_all(id="poem")
            
            pa = soup.select('span.author a')
            
            if pa:
                poem_author = soup.select('span.author a')[0].text
                print 'Author:',poem_author.encode('utf-8')
                title_id = soup.find(id="poem-top")
                poet_DOB = soup.select('span.author span.birthyear')[0].text
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
                categories = {}
                # labels are all within 'about' div
                about = soup.find('div', attrs={'class' : 'about'})
                # nested within their own section
                ps_about = about.find_all('p', attrs={'class' : 'section'})

                for slug in ps_about:
                    labels = slug.find('span', attrs={'class' : 'slug'})

                    if labels.text  != 'Poet':
                        
                        category = labels.text    
                        print category.encode('utf-8'), ": "

                        # create a list within dict for this category
                        categories[category] = []

                        lbs = labels.find_next_siblings()

                        for lb in lbs:
                            categories[category].append(lb.text)

                        for cat_label in categories[category]:
                            print cat_label.encode('utf-8')