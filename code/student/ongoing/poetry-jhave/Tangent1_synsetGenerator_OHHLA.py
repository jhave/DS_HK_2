#! /usr/bin/env python

"""

MOodified from
https://github.com/shanbady/NLTK-Boston-Python-Meetup

Tangent#1 : generate a poem use synsets from nltk wordnet to replace all but stopwords
Goal: generate a set of poems from entire corpus.

1. 
Read in a .txt file poem

2.
For each poem: 

    Tokenize
    Find synsets
    Select replacement word

3. 
Write new poem to txt file in "generated/tangent1_synset/"


"""


from __future__ import division

from random import randint
from random import shuffle

from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.corpus import cmudict,wordnet as wn
from nltk.corpus import stopwords
import nltk, re, pprint
from nltk import Text

WhitespaceTokenizer = nltk.WhitespaceTokenizer

import re
import os, datetime
import sys
import random
import string

import import_utilities

# HOW_TO put all utilities into subdirectory and call them in: sys.path.insert(0,'/utilities')
#import profanityFilter_ARR.py
curses = [
'2g1c',
'2 girls 1 cup',
'acrotomophilia',
'anal',
'anilingus',
'anus',
'arsehole',
'ass',
'asshole',
'assmunch',
'auto erotic',
'autoerotic',
'babeland',
'baby batter',
'ball gag',
'ball gravy',
'ball kicking',
'ball licking',
'ball sack',
'ball sucking',
'bangbros',
'bareback',
'barely legal',
'barenaked',
'bastardo',
'bastinado',
'bbw',
'bdsm',
'beaver cleaver',
'beaver lips',
'bestiality',
'bi curious',
'big black',
'big breasts',
'big knockers',
'big tits',
'bimbos',
'birdlock',
'bitch',
'black cock',
'blonde action',
'blonde on blonde action',
'blow j',
'blow your l',
'blue waffle',
'blumpkin',
'bollocks',
'bondage',
'boner',
'boob',
'boobs',
'booty call',
'brown showers',
'brunette action',
'bukkake',
'bulldyke',
'bullet vibe',
'bung hole',
'bunghole',
'busty',
'butt',
'buttcheeks',
'butthole',
'camel toe',
'camgirl',
'camslut',
'camwhore',
'carpet muncher',
'carpetmuncher',
'chocolate rosebuds',
'circlejerk',
'cleveland steamer',
'clit',
'clitoris',
'clover clamps',
'clusterfuck',
'cock',
'cocks',
'coprolagnia',
'coprophilia',
'cornhole',
'cum',
'cumming',
'cunnilingus',
'cunt',
'darkie',
'date rape',
'daterape',
'deep throat',
'deepthroat',
'dick',
'dildo',
'dirty pillows',
'dirty sanchez',
'dog style',
'doggie style',
'doggiestyle',
'doggy style',
'doggystyle',
'dolcett',
'domination',
'dominatrix',
'dommes',
'donkey punch',
'double dong',
'double penetration',
'dp action',
'eat my ass',
'ecchi',
'ejaculation',
'erotic',
'erotism',
'escort',
'ethical slut',
'eunuch',
'faggot',
'fecal',
'felch',
'fellatio',
'feltch',
'female squirting',
'femdom',
'figging',
'fingering',
'fisting',
'foot fetish',
'footjob',
'frotting',
'fuck',
'fucking',
'fuck buttons',
'fudge packer',
'fudgepacker',
'futanari',
'g-spot',
'gang bang',
'gay sex',
'genitals',
'giant cock',
'girl on',
'girl on top',
'girls gone wild',
'goatcx',
'goatse',
'gokkun',
'golden shower',
'goo girl',
'goodpoop',
'goregasm',
'grope',
'group sex',
'guro',
'hand job',
'handjob',
'hard core',
'hardcore',
'hentai',
'homoerotic',
'honkey',
'hooker',
'hot chick',
'how to kill',
'how to murder',
'huge fat',
'humping',
'incest',
'intercourse',
'jack off',
'jail bait',
'jailbait',
'jerk off',
'jigaboo',
'jiggaboo',
'jiggerboo',
'jizz',
'juggs',
'kike',
'kinbaku',
'kinkster',
'kinky',
'knobbing',
'leather restraint',
'leather straight jacket',
'lemon party',
'lolita',
'lovemaking',
'make me come',
'male squirting',
'masturbate',
'menage a trois',
'milf',
'missionary position',
'motherfucker',
'mound of venus',
'mr hands',
'muff diver',
'muffdiving',
'muthafucka',
'nambla',
'nawashi',
'negro',
'neonazi',
'nig nog',
'nigga',
'niggas',
'nigger',
'nimphomania',
'nipple',
'nipples',
'nsfw images',
'nude',
'nudity',
'nympho',
'nymphomania',
'octopussy',
'omorashi',
'one cup two girls',
'one guy one jar',
'orgasm',
'orgy',
'paedophile',
'panties',
'panty',
'pedobear',
'pedophile',
'pegging',
'penis',
'phone sex',
'piece of shit',
'piss pig',
'pissing',
'pisspig',
'playboy',
'pleasure chest',
'pole smoker',
'ponyplay',
'poof',
'poop chute',
'poopchute',
'porn',
'porno',
'pornography',
'prince albert piercing',
'pthc',
'pubes',
'pussy',
'queaf',
'raghead',
'raging boner',
'rape',
'raping',
'rapist',
'rectum',
'reverse cowgirl',
'rimjob',
'rimming',
'rosy palm',
'rosy palm and her 5 sisters',
'rusty trombone',
's&m',
'sadism',
'scat',
'schlong',
'scissoring',
'semen',
'sex',
'sexo',
'sexy',
'shaved beaver',
'shaved pussy',
'shemale',
'shibari',
'shit',
'shota',
'shrimping',
'slanteye',
'slut',
'smut',
'snatch',
'snowballing',
'sodomize',
'sodomy',
'spic',
'spooge',
'spread legs',
'strap on',
'strapon',
'strappado',
'strip club',
'style doggy',
'suck',
'sucks',
'suicide girls',
'sultry women',
'swastika',
'swinger',
'tainted love',
'taste my',
'tea bagging',
'threesome',
'throating',
'tied up',
'tight white',
'tit',
'tits',
'titties',
'titty',
'tongue in a',
'topless',
'tosser',
'towelhead',
'tranny',
'tribadism',
'tub girl',
'tubgirl',
'tushy',
'twat',
'twink',
'twinkie',
'two girls one cup',
'undressing',
'upskirt',
'urethra play',
'urophilia',
'vagina',
'venus mound',
'vibrator',
'violet blue',
'violet wand',
'vorarephilia',
'voyeur',
'vulva',
'wank',
'wet dream',
'wetback',
'white power',
'women rapping',
'wrapping men',
'wrinkled starfish',
'xx',
'xxx',
'yaoi',
'yellow showers',
'yiffy',
'zoophilia']



#
# pattern.en
# module to singularize and do verb tenses
# http://www.clips.ua.ac.be/pattern
#
from pattern.en import pluralize, singularize
from pattern.en import comparative, superlative
from pattern.en import conjugate, lemma, lexeme, PARTICIPLE
# # # print conjugate('googled', tense=PARTICIPLE, parse=True)  
# >>> googling
# NOTE: it also does sentiment, returns a tuple...
# from pattern.en import sentiment
# and can be used with weights using http://sentiwordnet.isti.cnr.it/ 

#
#  IMPORTANT : while testing change this dir
#
DATA_DIR  =  "../../../../data/poetry/ohhla/ohhla_txt_files_1/"#ohhla_txt_files_with_url/"
#  NOTE: "txt_6" directory contains only 6 files for testing
GENERATED_DIR  =  "../../../../data/poetry/ohhla/ohhla_generated/synsetGenerator_"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"/"

# add meronymns
# introduce a swearing shuffle
# brands array
# spice it up: porn & poetry terms (define a balancing term for that)


#
# HELPR FUNCTION: FIND A SIMILAR WORD OF SIMILAR SIZE
#

def find_synset_word(word):
    

    wordstring=word

    # get rid of punctuation
    #wordstring.translate(None, string.punctuation)
    word_punct = strip_punctuation(word)
    word = word_punct['word']
    punct = word_punct['punct']

    syllableSize=syllables_en.count(word)

    synsets = wn.synsets(word)
    shuffle(synsets)
    ## # print word,"synset:",synsets


    replacement_candidates = []

    for syns in synsets:

        lemmas =  syns.lemma_names
        ## # print "LEMMAS:",lemmas
        ## # print "hypernyms:",syns.hypernyms()
        ## # print "hyponyms:",syns.hyponyms()
        ## # print "holonyms:",syns.member_holonyms()
        ## # print syns,"antonyms:",syns.lemmas[0].antonyms()
        
        for w in lemmas:
            replacement_candidates.append(w)

        for w in syns.hyponyms():
            replacement_candidates.append(w.name.split(".")[0])

        for w in syns.hypernyms():
            replacement_candidates.append(w.name.split(".")[0])

        for w in syns.member_holonyms():
            replacement_candidates.append(w.name.split(".")[0])

        ## # print "replacement_candidates:",replacement_candidates

        for wordstring in replacement_candidates:
            #find an approximate matchb
            ## # print "wordstring in name:",wordstring
            if (approx_equal(wordstring,word) and wordstring.lower() != word.lower() and len(wordstring)>len(word)):
                ## # print "SYNSET approx_equal:",word,wordstring
                return wordstring+punct
            #len same, word not
            if(len(wordstring) == len(word) and wordstring.lower() != word.lower()):
                ## # print "SYNSET len same, word not:",word,wordstring
                return wordstring+punct

            if(syllables_en.count(wordstring) == syllableSize and wordstring.lower() != word.lower()):
                ## # print "SYNSET syllable same, word not:",word,wordstring
                return wordstring+punct
     

    ## # print "SYNSET escape case, return original:",word
    return    wordstring





#########################
# HELPER FUNCTIONs      #
#########################

# TEST FOR APPROX. EQUIVALENCE
def approx_equal(self, other, delta=4):
    count = abs(len(self) - len(other))
    for c,k in zip(self, other):
        count += c != k
    return count <= delta

# STRIP PUNCTUATION BUT KEEP IT TO BE ADDED LATER
def strip_punctuation(word):
    # define punctuations
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~_'''
    my_str = word

    # remove punctuations from the string
    no_punct = ""
    punct=""
    position=""
    punct_bool=False
    for char in my_str:
        if char not in punctuations:
            ### # print "CHAR:", char
            no_punct = no_punct + char
            
        else:
            punct_bool=True
            punct += char
            #no_punct = no_punct+' '

    ### # print "word:",no_punct,"punct:", punct
    return {'word':no_punct,'punct':punct, 'punct_bool':punct_bool}

#Check whether 'str' contains ANY punctuation
def containsAnyPunct(str):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~_'''
    return 1 in [c in str for c in punctuations]

def isAllPunct(s):
    return all(c in string.punctuation for c in s)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# replace digits with other digits...
def replaceNumbers(inputString):
    outputString =''
    for char in inputString:
        if char.isdigit():
            char = random.randrange(9)
            ## # print "DIGIT",char
        outputString +=str(char)
    return outputString

# STRIP _
def strip_underscore(word):
    # define punctuations
    punctuations = '''_'''
    my_str = word

    # remove _ from the string
    no_punct = ""
    for char in my_str:
        if char not in punctuations:
            ### # print "CHAR:", char
            no_punct = no_punct + char
        else:
            no_punct = no_punct+' '

    ### # print "word:",no_punct,"punct:", punct
    return no_punct


#
# take all UNIQUE terms, create reservoir, shuffle it when encountering next unique
#

RESERVOIR=["Jha"]

#
# LANGUAGE TEST using import_utilities.get_language(line)
#

#################################################

labels_to_keep = ['Artist','Album','Song','Typed', 'VERSE','CHORUS']

personal_pronouns = ["i","me","we","us","you","she","her","he","him","it","they","them"]

#################################################
#                                               #
#    READ FILES                                 #
#                                               #
#################################################
for subdir, dirs, files in os.walk(DATA_DIR):
    for file in files:
        #print subdir+file
        if ".txt" in file  and 'readme' not in file:
            html_file_number=file.split(".")[0]
            print "file",file#,"\nhtml_file_number",html_file_number
            # 
            # & PARSE POEM
            #
            cnt=0
            new_poem = ""
            quit_language=0
           
            pf = open(subdir+file, 'rU')
            for line in pf:
                
                wordmap = []
                new_line=""
                replacement_word=""
                

                if cnt>=6 and len(line) > 12 and "[" not in line and "english" not in import_utilities.get_language(line):
                    quit_language+=1
                    #print import_utilities.get_language(line), quit_language, "line:",line
                else:
                    if cnt>=6:
                        quit_language-=1
                    #print "quit_language:",quit_language,"line:", line

                '''

KEEP

<pre>
Artist: Spice 1
Album:  1990-Sick
Song:   1-800 (Str8 from the Pen)
Typed by : Timo.Scheffler@allgaeu.org

                '''
                if "<a href='http:" in line:
                    url = line
                    # print "url:",url

                elif '<pre>' not in line and '</pre >' not in line and '< /pre >' not in line:

                    # POS part-of-speech
                    line_pos_tags = nltk.pos_tag(line.strip(' \t\n\r').split(' '))
                    # # # print "\n",line
                    # # # print line_pos_tags



                    if len(line)>0:
                        new_line="\n"

                    cnt=cnt+1
                    #capitalize artist,album,song
                    label_idx=99
                    skip_line=False

                    # if line is not empty, push each word of line into array with syllable cnt
                    if len(line) > 1:

                        widx=0
                        # get each WORD
                        for word in line.strip(' \t\n\r').split(' '):

                            # scramble emails
                            if '@' in word:
                                word = ''.join(random.sample(word,len(word)))

                            # deal with end case
                            if '</pre>' in word:
                                word = word.split('</pre>')[0]

                            #####################################
                            # non-empty word, start replacement #
                            #####################################
                            if len(word)>0:

                                # # # print word,"widx:",widx," line_pos_tags[widx][0]:",line_pos_tags[widx][0]," line_pos_tags[widx][1]:",line_pos_tags[widx][1]

                                # booleans that allow us to leave the VERSE CHORUS format
                                labelling=False
                                VC = False
                                
                                # if it's ALL punctuation, don't change it
                                if isAllPunct(word):
                                    new_line += word+' '
                                    # print "isAllPunct new_line",new_line
                                # if it's numeric, shuffle it
                                elif hasNumbers(word):
                                    new_line += replaceNumbers(word)+' '
                                    # print "replaceNumbers new_line",new_line
                                else:
                                    # is it Artist, Album, Song
                                    for ltk in labels_to_keep:
                                        if ltk in word:
                                            ## # print 'found an ',ltk
                                            labelling = True
                                            label_idx=0

                                            if 'VERSE' in ltk or 'CHORUS' in ltk:
                                                ## # print "skip this line"
                                                new_line += ltk+" "
                                                # print "VERSE new_line",new_line
                                                skip_line=True
                                            else:
                                                replacement_word=ltk
                                                if 'Typed' not in ltk:
                                                    new_line += replacement_word+": "
                                                    # print "Typed new_line",new_line
                                                else:
                                                    new_line += replacement_word+" "
                                                    # print "else Typed new_line",new_line



                                    ###########################################################
                                    # REPLACEMENT of pronouns with compressed verb (as in I'd)#
                                    ###########################################################                
                                    if len(word.split("'"))>1:

                                        if word.split("'")[0] in personal_pronouns:
                                            replacement_word = random.choice(personal_pronouns)+"'"+word.split("'")[1]+' '
                                            # print "COMPOSITE pronoun'verb word:'"+word+"'    replacement:",replacement_word

                                            new_line += replacement_word
                                            # print "PRONOUNS new_line:",new_line

                                    ####################################################
                                    # Replacement of OTHERs                            #
                                    ####################################################

                                    elif not word.lower() in stopwords.words('english') and not labelling and not skip_line:

                                        # take off leading brackets, commas etc...
                                        word_punct_nopunct = strip_punctuation(word)
                                        word_nopunct = word_punct_nopunct['word']
                                        word_punct = word_punct_nopunct['punct']
                                        punct_bool = word_punct_nopunct['punct_bool']
                                        
                                        
                                        similarterm = find_synset_word(word_nopunct)
                                        if similarterm == "ilk":
                                            #print "LIKE it"
                                            similarterm = "like"

                                        # is it a TRUNCATED VERB slang as in singin or wishin
                                        if similarterm == word and len(word)>2 and 'in' in word[-2:]:
                                            similarterm = find_synset_word(word+'g')
                                            ## print "TRUNCATED SLANG word: '"+word+"'",similarterm
                                            interim = lemma(similarterm)
                                            ## print interim
                                            similarterm = conjugate(interim, tense=PARTICIPLE, parse=True)[:-1] 
                                            # # # print word,"widx:",widx," line_pos_tags[widx][0]:",line_pos_tags[widx][0]," line_pos_tags[widx][1]:",line_pos_tags[widx][1]
                                           

                                        #################      
                                        # SWEAR WORD    #
                                        #################
                                        #print "at the garden of if:", word
                                        if word in curses:
                                            similarterm = random.choice(curses)
                                            #print "SWEAR WORD word: '"+word+"'",similarterm


                                        ####################################################
                                        # put punctuation stripped off string back onto it 
                                        # testing: (\why ->i, not*)
                                        ####################################################
                                        # # print word, word_nopunct, similarterm
                                        #replacement_word = string.replace(word, word_nopunct, replacement_word)

                                        #if punct_bool:
                                        # print "BEFORE word.replace replacement_word:",replacement_word
                                        replacement_word = word.replace(word_nopunct, similarterm)
                                        # print "AFTER word.replace replacement_word:",replacement_word

                                        replacement_word = strip_underscore(replacement_word)
                                        replacement_word = replaceNumbers(replacement_word)

                                        if label_idx<2:
                                            replacement_word = ' '.join(word[0].upper() + word[1:] for word in replacement_word.split())
                                            ## # print "CAPITALIZE",replacement_word

                                        
                                        # RESERVOIR_OF_WEIRDNESS    
                                        if "like" not in word and word == replacement_word and "english" in import_utilities.get_language(line):
                                            if word not in RESERVOIR and quit_language<0 and import_utilities.countPunctuation(word)<1: 
                                                RESERVOIR.append(word)
                                                #print "add to RESERVOIR: ",import_utilities.countPunctuation(word),word
                                            replacement_word = random.choice(RESERVOIR)
                                            #print word,"  vs   replacement_word:",replacement_word #,"    new_line:",new_line
                                        if quit_language>0:
                                            #print "Probably foreign language: make a word salad in english"
                                            replacement_word = random.choice(RESERVOIR)


                                        new_line += replacement_word+" "
                                        # print "BIG BLOCK new_line",new_line
                                        ## print "word: '"+word+"' replacement: '"+replacement_word+"' new_line:",new_line



                                    elif not labelling and not skip_line:
                                        if word.isalpha():
                                            #print "SAME?:",word
                                            new_line += word+" "
                                            # if not word.lower() in personal_pronouns :
                                            #     new_line += word+" "
                                            #     # print "skip STOP word: *"+word+"*","new_line:",new_line
                                            # else:
                                            #     replacement_word = random.choice(personal_pronouns)
                                            #     ## print word+" random personal_pronouns: *"+replacement_word+"*"
                                            #     new_line += replacement_word+" "
                                            #     # print "else STOP new_line",new_line
                                        else:
                                              # # print "verse GAP"
                                              new_line += "\n"
                                              # print "GAP new_line",new_line
                            #else:
                                ## # print len(line),"line break"
                                #new_line += "\n"

                                widx+=1



                    

                    #
                    #  POEM line + line ...
                    #  
                    # # print new_line  +"\n\n*******"
                    new_poem += new_line

                    ## print "\nLINE:",line,"NEW LINE:",new_line,"\n"



            # 
            # WRITE new POEM TO FILE
            #
            txt_fn = html_file_number+".txt"
            # # print "TXT Filename: ", txt_fn.encode('utf-8')

            txt_fn_path = GENERATED_DIR+txt_fn
            # # print "txt_fn_path: ",txt_fn_path.encode('utf-8')


            if not os.path.exists(GENERATED_DIR):
                os.makedirs(GENERATED_DIR)

            f=open(txt_fn_path,'w+')

            dp = url+new_poem
            f.write(dp)

            f.close();
            
            #print RESERVOIR

            txt_fn_path = GENERATED_DIR+"00AA_RESERVOIR.txt"
            if not os.path.exists(GENERATED_DIR):
                os.makedirs(GENERATED_DIR)

            f=open(txt_fn_path,'w+')

            dp = ' '.join(RESERVOIR)
            f.write(dp)

            f.close();


print "RESERVOIR:", ' '.join(RESERVOIR)






    

