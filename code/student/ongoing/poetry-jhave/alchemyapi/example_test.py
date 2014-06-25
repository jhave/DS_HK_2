#!/usr/bin/env python

# modified to feed text file...


from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

DATA_DIR  =  "../../../../../data/poetryFoundation/"

txt_fn= DATA_DIR+"txt/1888.txt"
pf = open(txt_fn, 'r')
#print pf.read()
demo_text = pf.read()
pf.close()

demo_url = 'http://www.poetryfoundation.org/poem/1888'

txt_fn= DATA_DIR+"html/1888.html"
pf = open(txt_fn, 'r')
#print pf.read()
demo_html = pf.read()
pf.close()

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

print('Processing text: ', demo_text)


print('')
print('')
print('############################################')
print('#   Entity Extraction Example              #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.entities('text', demo_text, {'sentiment': 1})

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Entities ##')
    for entity in response['entities']:
        print('text: ', entity['text'].encode('utf-8'))
        print('type: ', entity['type'])
        print('relevance: ', entity['relevance'])
        print('sentiment: ', entity['sentiment']['type'])
        if 'score' in entity['sentiment']:
            print('sentiment score: ' + entity['sentiment']['score'])
        print('')
else:
    print('Error in entity extraction call: ', response['statusInfo'])


print('')
print('')
print('')
print('############################################')
print('#   Keyword Extraction Example             #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Keywords ##')
    for keyword in response['keywords']:
        print('text: ', keyword['text'].encode('utf-8'))
        print('relevance: ', keyword['relevance'])
        print('sentiment: ', keyword['sentiment']['type'])
        if 'score' in keyword['sentiment']:
            print('sentiment score: ' + keyword['sentiment']['score'])
        print('')
else:
    print('Error in keyword extaction call: ', response['statusInfo'])


print('')
print('')
print('')
print('############################################')
print('#   Concept Tagging Example                #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.concepts('text', demo_text)

if response['status'] == 'OK':
    print('## Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Concepts ##')
    for concept in response['concepts']:
        print('text: ', concept['text'])
        print('relevance: ', concept['relevance'])
        print('')
else:
    print('Error in concept tagging call: ', response['statusInfo'])


print('')
print('')
print('')
print('############################################')
print('#   Sentiment Analysis Example             #')
print('############################################')
print('')
print('')

#print('Processing html: ', demo_html)
print('')

response = alchemyapi.sentiment('html', demo_html)

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Document Sentiment ##')
    print('type: ', response['docSentiment']['type'])

    if 'score' in response['docSentiment']:
        print('score: ', response['docSentiment']['score'])
else:
    print('Error in sentiment analysis call: ', response['statusInfo'])


print('')
print('')
print('')
print('############################################')
print('#   Targeted Sentiment Analysis Example    #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

targeting='sky'
response = alchemyapi.sentiment_targeted('text', demo_text, targeting)

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Targeted Sentiment ## of',targeting)
    print('type: ', response['docSentiment']['type'])

    if 'score' in response['docSentiment']:
        print('score: ', response['docSentiment']['score'])
else:
    print('Error in targeted sentiment analysis call: ',
          response['statusInfo'])


print('')
print('')
print('')
print('############################################')
print('#   Text Extraction Example                #')
print('############################################')
print('')
print('')

print('Processing url: ', demo_url)
print('')

response = alchemyapi.text('url', demo_url)

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Text ##')
    print('text: ', response['text'].encode('utf-8'))
    print('')
else:
    print('Error in text extraction call: ', response['statusInfo'])


print('')
print('')
print('')
print('############################################')
print('#   Author Extraction Example              #')
print('############################################')
print('')
print('')

print('Processing url: ', demo_url)
print('')

response = alchemyapi.author('url', demo_url)

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Author ##')
    print('author: ', response['author'].encode('utf-8'))
    print('')
else:
    print('Error in author extraction call: ', response['statusInfo'])


print('')
print('')
print('')
print('############################################')
print('#   Relation Extraction Example            #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.relations('text', demo_text)

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


print('')
print('')
print('')
print('############################################')
print('#   Text Categorization Example            #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.category('text', demo_text)

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Category ##')
    print('text: ', response['category'])
    print('score: ', response['score'])
    print('')
else:
    print('Error in text categorization call: ', response['statusInfo'])

print('')
print('')
print('')
print('############################################')
print('#   Taxonomy  Example                      #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.taxonomy('text', demo_text)

if response['status'] == 'OK':
    print('## Response Object ##')
    #print(json.dumps(response, indent=4))

    print('')
    print('## Categories ##')
    for category in response['taxonomy']:
        print(category['label'], ' : ', category['score'])
    print('')

else:
    print('Error in taxonomy call: ', response['statusInfo'])

print('')
print('')


print('')
print('')
print('')
print('############################################')
print('#   Combined  Example                      #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.combined('text', demo_text)

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

print('')
print('')


'''

Processing text:  
                    
                                                        I 
          Over the green and yellow rice fields sweep the shadows of the autumn clouds, followed by the swift-chasing sun.
         The bees forget to sip their honey; drunken with the light they foolishly hum and hover; and the ducks in the sandy riverbank clamour in joy for mere nothing.
         None shall go back home, brothers, this morning, none shall go to work.
         We will take the blue sky by storm and plunder the space as we run.
         Laughters fly floating in the air like foams in the flood.
         Brothers, we shall squander our morning in futile songs.



############################################
#   Entity Extraction Example              #
############################################



## Response Object ##

## Entities ##



############################################
#   Keyword Extraction Example             #
############################################



## Response Object ##

## Keywords ##
text:  sandy riverbank clamour
relevance:  0.974501
sentiment:  negative
sentiment score: -0.458531

text:  yellow rice fields
relevance:  0.91222
sentiment:  negative
sentiment score: -0.427408

text:  autumn clouds
relevance:  0.680668
sentiment:  negative
sentiment score: -0.427408

text:  futile songs
relevance:  0.623196
sentiment:  negative
sentiment score: -0.552214

text:  swift-chasing sun
relevance:  0.613043
sentiment:  positive
sentiment score: 0.288541

text:  blue sky
relevance:  0.569742
sentiment:  negative
sentiment score: -0.51931

text:  morning
relevance:  0.449628
sentiment:  negative
sentiment score: -0.223052

text:  hover
relevance:  0.398894
sentiment:  negative
sentiment score: -0.458531

text:  brothers
relevance:  0.391409
sentiment:  positive
sentiment score: 0.270577

text:  foams
relevance:  0.381341
sentiment:  neutral

text:  bees
relevance:  0.377381
sentiment:  negative
sentiment score: -0.458531

text:  shadows
relevance:  0.377335
sentiment:  negative
sentiment score: -0.427408

text:  ducks
relevance:  0.376652
sentiment:  negative
sentiment score: -0.458531

text:  honey
relevance:  0.36963
sentiment:  negative
sentiment score: -0.458531

text:  joy
relevance:  0.367569
sentiment:  negative
sentiment score: -0.458531

text:  flood
relevance:  0.3644
sentiment:  neutral

text:  storm
relevance:  0.358775
sentiment:  negative
sentiment score: -0.51931

text:  light
relevance:  0.35002
sentiment:  negative
sentiment score: -0.458531

text:  home
relevance:  0.348454
sentiment:  negative
sentiment score: -0.719674

text:  work
relevance:  0.347906
sentiment:  negative
sentiment score: -0.789874

text:  space
relevance:  0.346443
sentiment:  negative
sentiment score: -0.51931




############################################
#   Concept Tagging Example                #
############################################



## Object ##

## Concepts ##
text:  Blue
relevance:  0.94493

text:  Light
relevance:  0.780683

text:  Green
relevance:  0.756043

text:  Insect
relevance:  0.727649

text:  Color
relevance:  0.71024

text:  Cliff Richard
relevance:  0.69485

text:  Francis Monkman
relevance:  0.682016

text:  Alan Tarney
relevance:  0.678243




############################################
#   Sentiment Analysis Example             #
############################################



## Response Object ##

## Document Sentiment ##
type:  positive
score:  0.148886



############################################
#   Targeted Sentiment Analysis Example    #
############################################



## Response Object ##

## Targeted Sentiment ## of sky
type:  negative
score:  -0.51931



############################################
#   Text Extraction Example                #
############################################


Processing url:  http://www.poetryfoundation.org/poem/1888

## Response Object ##

## Text ##
text:  I  / Over the green and yellow rice fields sweep the shadows of the autumn clouds, followed by the swift-chasing sun. / The bees forget to sip their honey; drunken with the light they foolishly hum and hover; and the ducks in the sandy riverbank clamour in joy for mere nothing.




############################################
#   Author Extraction Example              #
############################################


Processing url:  http://www.poetryfoundation.org/poem/1888

Error in author extraction call:  author-not-found:cannot-locate



############################################
#   Relation Extraction Example            #
############################################



## Object ##

## Relations ##
Subject:  I          Over the green and yellow rice fields
Action:  sweep
Object:  the shadows of the autumn clouds

Subject:  The bees
Action:  forget
Object:  to sip their honey

Subject:  The bees
Action:  forget to sip
Object:  their honey

Subject:  they
Action:  drunken
Object:  with the light

Subject:  None
Action:  shall go
Object:  back home, brothers, this morning, none

Subject:  We
Action:  will take
Object:  the blue sky by storm

Subject:  we
Action:  shall squander
Object:  our morning




############################################
#   Text Categorization Example            #
############################################



## Response Object ##

## Category ##
text:  science_technology
score:  0.835516




############################################
#   Taxonomy  Example                      #
############################################



## Response Object ##

## Categories ##
/science/weather/meteorological disaster/flood  :  0.435439
/business and industrial/chemicals industry/adhesives  :  0.408974
/sports/fishing/fly fishing  :  0.283618






############################################
#   Combined  Example                      #
############################################



## Response Object ##

## Keywords ##
sandy riverbank clamour  :  0.974501
yellow rice fields  :  0.91222
autumn clouds  :  0.680668
futile songs  :  0.623196
swift-chasing sun  :  0.613043
blue sky  :  0.569742
morning  :  0.449628
hover  :  0.398894
brothers  :  0.391409
foams  :  0.381341
bees  :  0.377381
shadows  :  0.377335
ducks  :  0.376652
honey  :  0.36963
joy  :  0.367569
flood  :  0.3644
storm  :  0.358775
light  :  0.35002
home  :  0.348454
work  :  0.347906
space  :  0.346443

## Concepts ##
Blue  :  0.94493
Light  :  0.780683
Green  :  0.756043
Insect  :  0.727649
Color  :  0.71024
Cliff Richard  :  0.69485
Francis Monkman  :  0.682016
Alan Tarney  :  0.678243

## Entities ##
 


[Finished in 7.7s]

'''
