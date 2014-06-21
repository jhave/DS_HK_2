#! /usr/bin/env python

"""

Based on: 
http://www.nltk.org/howto/collocations.html
http://nltk.googlecode.com/svn/trunk/doc/howto/collocations.html

GOALS: 

1.
make collocation table for corpus in DS_HK_2\data\poetryFoundation\generated\ALL_poems.txt

2.
use that to generate poems on a spectrum from rare to cliched

3. [FUTURE GOAL]
combine with tangent1_synsetGenerator.py 

NOTE: i deleted 171644.txt : stupid christmas carol that warps the data

"""


from __future__ import division

from random import randint
from random import shuffle

from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.corpus import cmudict,wordnet as wn
from nltk.corpus import stopwords
import nltk, re, pprint
from nltk import Text

from nltk.collocations import *
from nltk import word_tokenize

import re
import os
import sys
import random



# use SOME_poems.txt for testing... ALL_poems.txt
CORPUS_TXT_FILE  =  "../../../../data/poetryFoundation/generated/ALL_poems.txt"
PROJECT_DIR  =  "../../../../data/poetryFoundation/generated/tangent_nltk_Collocation/"


#
#    READ CORPUS   ...  NOTE: .decode('utf-8')
#

pf=open(CORPUS_TXT_FILE,'r')

ALL_poems_string= pf.read().decode('utf-8')

pf.close();

#
#  define by negation (get rid of cruft)  ... TODO get rid of code cruft: \u2019
#

ignored_words =nltk.corpus.stopwords.words('english')

#
#   COLLOCATE    BIgrams
#

# bigram_measures = nltk.collocations.BigramAssocMeasures()
# bi_finder = BigramCollocationFinder.from_words(word_tokenize(ALL_poems_string))

# bi_finder.apply_freq_filter(30)
# bi_finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)

# #print bi_finder.nbest(bigram_measures.pmi, 100)  
# bfn = bi_finder.nbest(bigram_measures.pmi, 100)
# bfn_str=""

# for item in bfn:
#     bfn_str+=item[0]+" "+item[1]+"\n"

# print bfn_str.encode('ascii', 'ignore')




#
#   COLLOCATE    TRIgrams
#

trigram_measures = nltk.collocations.TrigramAssocMeasures()
tri_finder = TrigramCollocationFinder.from_words(word_tokenize(ALL_poems_string))

tri_finder.apply_freq_filter(10)
tri_finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)

#print tri_finder.nbest(trigram_measures.pmi, 100)  
tfn = tri_finder.nbest(trigram_measures.pmi, 100)
tfn_str=""

for item in tfn:
    tfn_str+=item[0]+" "+item[1]+" "+item[2]+"\n"

print tfn_str.encode('ascii', 'ignore')


"""
FORMATED ON TEST SOME_poems.txt DATA.....
BIgrams RETURNS:

orchid juice.
six inches
Uncle Paul
worry beads
Spanish lawyer
killing stick
autumn winter
good tunes
Devil get
become food
says Mister
drink till
beast within
alone knows
Duke Cosimo
stars rain
Something something
knows you.
sun moon
thousand years
one coin
eye first
dont know
first time
one side
n't know
one day
could n't
one night
body like


#########################################
FORMATED ON ALL_poems.txt DATA.....
with apply_freq_filter(3)
BIgrams RETURNS a list of cliches and 'brand' name objects and people, myth detritus with an emphasis on contemporary americana:

BASS DRUM
BRITISH INDIA
Des Moines
Jeanne dArc
dge ysses
low-definition attorneys.
wintres wedres
negro poet
FIFTEEN MINUTES.
Haines Eason
Phenomenally. Phenomenal
Plunge. Push.
Push. Lift.
Chatty Cathy.
Nova Scotia
Pall Mall
Ron Padgett
Weatherbeaten Bones.
Britian __________
GOLDEN TRACK.
Hot-cross buns
Quitte Pas
Doris Holbrook
Pangur Bn
Pease porridge
SHORT HISTORY
Myrna Loy
sonne softe
Hong Kong
ms. merongrongrong
Grosse Pointe
Wang Wei
samod tgdere
Eddie Bauer
Knickerbocker Theater
Tha vahnahnah
conturbabimus illa
Frederick Olmsted
Withered Chestnuts
terra cotta
Kay Jewelers
posthumous chomp
Billie Holiday
Mme. Sperides
Coral Gables
Lift. Toss
Silvry Tay
rigor mortis
schooner Flight.
Cherry Ames
Giordano Bruno
Kenneth Koch
Las Vegas
Lisbon Packet.
Mickey Mouse
mun doy
Norman Morrison
Buenos Aires
Csar Vallejo
lucy one-eye
Puerto Rican
D.G. Castleman
Kegon sect
Comrade Stalin
Sylvia Plath
Haroun Alraschid.
Cleanup crews
con brio
roller coaster
Van Gogh
sele am
Hank Williams
lapis lazuli
Cape Cod
Jackson Pollock
Natal Command
Linda Deemer
boom. Boomlay
obliterating strangeness
Baltimore Maryland
Hart Crane
evenly spaced
Pitti Palace
Zennor Hill.
Carneys Point
Robin Hood
les btes
West Point
Los Angeles
Barbara Allen.
ghoul-haunted woodland
drummers drumming
Madeleine Reierbacher
T.S. Eliot
Giovanni Bapini
Giovanni Franchi
gold-wove banner
instruction manual
Rudolph Reed
Richard Blanco

#########################
FORMATED ON ALL_poems.txt DATA.....
with apply_freq_filter(10)
BIgrams RETURNS more cliches and 'brand' name objects and people,  but with a bit more obscure myth detritus:
-- is apply_freq_filter working? does "pear tree" really occur in corpus more than 10 times?

Haroun Alraschid.
Los Angeles
Madeleine Reierbacher
eccho ring.
San Francisco
Visual Poetry
Stink Eye
Poetry magazine.
Miss Scarlett
Sister Ann
Mr. Fanelli
greatly expressing
Originally appeared
turtle doves
Sir Leoline
St. Agnes
barbed wire
Sir Bedivere
French hens
united nations
clearly expressing
expressing something.
Stick City
harken ere
Sweet Thames
New Orleans
New York
post office
parking lot
pear tree.
t hie
Two turtle
someone elses
lie. Tell
John Henry
ice cream
York City
bold Sir
King Arthur
New England
good Haroun
Three French
human beings
Ten thousand
mother Ida
Rhea think
thus began.
St. John
six months
ten thousand
Wilt thou
golden prime
Thou shalt
Thank you.
thou knowst
thou seest
expressing something
Dont take
Thou hast
run softly
years ago
thirty years
thou may'st
thou wert
Hast thou
Moloch whose
empty space
Thou canst
five hundred
thou mayst
thou shouldst
thousand miles
thou knowest
years ago.
kitchen table
either side
Dost thou
thou canst
screen door
forty years
thou hast
Im sorry
wilt thou
thou wast
Thou art
twenty years
thou wouldst
youve got
thou hadst
happy idea
high school
fifty years
thou shalt
bridal day
united way
someone else
Last night
lie awake
pine trees
Id rather

###########################
FORMATED ON ALL_poems.txt DATA.....
with apply_freq_filter(30)
BIgrams RETURNS less cliches and more 18th century formalisms: thou will long know one, etc...
-- is apply_freq_filter working? Sir Bedivere occurs more than 30 times!!??


Sir Bedivere
New York
ten thousand
Thou hast
years ago
empty space
either side
thou canst
thou hast
wilt thou
Thou art
high school
thou shalt
someone else
Last night
thou dost
thou wilt
hundred years
gives way
Ive seen
years later
long ago
thou art
thousand years
hast thou
many times
dont know
dont want
thy self
far away
didnt know
thine eyes
nothing else
long since
right hand
left behind
young men
never seen
young man
art thou
long enough
come back
mine eyes
every day
old man
n't know
many years
One day
old woman
first time
looks like
even though
last night
could n't
dead man
came back
could hear
could see
long time
one knows
one thing
looked like
one another
one side
last time
one day
could say
could never
would never
never know
never see
would come
every one
look like
something like
one hand
one night
one could
one man
one would
would like


##########
RAW OUTPUT
BIgrams RETURNS:

[(u'BASS', u'DRUM'), (u'BRITISH', u'INDIA'), (u'Des', u'Moines'), (u'Jeanne', u'd\u2019Arc'), (u'd\xe6ge', u'\xfeysses'), (u'low-definition', u'attorneys.'), (u'wintres', u'wedres'), (u'\u201cnegro', u'poet\u201d'), (u'FIFTEEN', u'MINUTES.'), (u'Haines', u'Eason'), (u'Phenomenally.', u'Phenomenal'), (u'Plunge.', u'Push.'), (u'Push.', u'Lift.'), (u'Chatty', u'Cathy.'), (u'Nova', u'Scotia'), (u'Pall', u'Mall'), (u'Ron', u'Padgett'), (u'Weatherbeaten', u'Bones.'), (u'Britian', u'__________'), (u'GOLDEN', u'TRACK.'), (u'Hot-cross', u'buns'), (u'Quitte', u'Pas'), (u'Doris', u'Holbrook'), (u'Pangur', u'B\xe1n'), (u'Pease', u'porridge'), (u'SHORT', u'HISTORY'), (u'Myrna', u'Loy'), (u'sonne', u'softe'), (u'Hong', u'Kong'), (u'ms.', u'merongrongrong'), (u'Grosse', u'Pointe'), (u'Wang', u'Wei'), (u'samod', u'\xe6tg\xe6dere'), (u'Eddie', u'Bauer'), (u'Knickerbocker', u'Theater'), (u'Tha\u2019', u'vahnahnah'), (u'conturbabimus', u'illa'), (u'Frederick', u'Olmsted'), (u'Withered', u'Chestnuts'), (u'terra', u'cotta'), (u'Kay', u'Jewelers'), (u'posthumous', u'chomp'), (u'Billie', u'Holiday'), (u'Mme.', u'Sperides'), (u'Coral', u'Gables'), (u'Lift.', u'Toss'), (u'Silv\u2019ry', u'Tay'), (u'rigor', u'mortis'), (u'schooner', u'Flight.'), (u'Cherry', u'Ames'), (u'Giordano', u'Bruno'), (u'Kenneth', u'Koch'), (u'Las', u'Vegas'), (u'Lisbon', u'Packet.'), (u'Mickey', u'Mouse'), (u'mun', u'doy'), (u'Norman', u'Morrison'), (u'Buenos', u'Aires'), (u'C\xe9sar', u'Vallejo'), (u'lucy', u'one-eye'), (u'Puerto', u'Rican'), (u'D.G.', u'Castleman'), (u'Kegon', u'sect'), (u'Comrade', u'Stalin'), (u'Sylvia', u'Plath'), (u'Haroun', u'Alraschid.'), (u'Cleanup', u'crews'), (u'con', u'brio'), (u'roller', u'coaster'), (u'Van', u'Gogh'), (u'sele', u'\xfeam'), (u'Hank', u'Williams'), (u'lapis', u'lazuli'), (u'Cape', u'Cod'), (u'Jackson', u'Pollock'), (u'Natal', u'Command'), (u'Linda', u'Deemer'), (u'boom.', u'Boomlay'), (u'obliterating', u'strangeness'), (u'Baltimore', u'Maryland'), (u'Hart', u'Crane'), (u'evenly', u'spaced'), (u'Pitti', u'Palace'), (u'Zennor', u'Hill.'), (u'Carney\u2019s', u'Point'), (u'Robin', u'Hood'), (u'les', u'b\xeates'), (u'\u201cWest', u'Point'), (u'Los', u'Angeles'), (u'Barbara', u'Allen.\u201d'), (u'ghoul-haunted', u'woodland'), (u'drummers', u'drumming'), (u'Madeleine', u'Reierbacher'), (u'T.S.', u'Eliot'), (u'Giovanni', u'Bapini'), (u'Giovanni', u'Franchi'), (u'gold-wove', u'banner'), (u'instruction', u'manual'), (u'Rudolph', u'Reed'), (u'Richard', u'Blanco')]
[Finished in 73.9s]

"""


"""

TRIgrams RETURNS 

withOUT apply_freq_filter and apply_word_filter
NOTE: many results all come from: http://www.poetryfoundation.org/poem/183587

[(u"'beyond", u"her'.", u'Bertold'), (u"'ow", u'quoloty', u'smoiles'), (u'//////////////////OOOOOOOOoooooooooooooooo/////////////////////', u'24242424242424242424242424242424242424242424242424242', u'februaryfebruaryfebruaryfebruaryfebruaryfebruaryfebruraryfebr'), (u'//potrero', u'traptraptraptraptraptraptraptraptraptraptraptraptraptraptraptraptr', u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'), (u'/burnt', u'sienna', u'/turquoise'), (u'1/25', u'Cobalt', u'linoleate'), (u'10th.', u'1666.', u'Copied'), (u'13-year-old', u'mercy\u2014', u'\u2018Take'), (u'1849', u'EN', u'ROUTE'), (u'1889', u'Somno', u'mollior'), (u'19.6.32\u2014deported', u'24.9.42', u'Undesirable'), (u'1968.', u'Neal\u2026\u2026Neal', u'Cassady\u2026\u2026died'), (u'24242424242424242424242424242424242424242424242424242', u'februaryfebruaryfebruaryfebruaryfebruaryfebruaryfebruraryfebr', u'Circacircacircacircacircacircacircacircacircacircacircacircacircacirca'), (u'27.50', u'guilders.', u'Burgundy-colored'), (u'5,000', u'Somali', u'Kenyans'), (u'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', u'1515151515151515151515151515151515151515151515151515151', u'brennenbrennenbrennenbrennenbrennenbrennenbrennenbrennen'), (u'ARMENIAN', u'TILE', u'SHOP'), (u'Abdel', u'Aziz', u'al-Sa\xfad'), (u'Aer', u'Lingus', u'check-in'), (u'Alber-', u'tino', u'Mussato'), (u'Aliphatic', u'C14', u'Hydrocarbon'), (u'All-State\u2026\u2026car', u'crash\u2026.1959.', u'Cisco'), (u'Alvord', u'desert\u2014pronghorn', u'ranges\u2014'), (u'An-', u'dromache', u'Nibbles'), (u'Antoine', u'Gaget.', u'1530.'), (u'Aurean', u'coronam', u'habentem'), (u'BUGS', u'BUNNY', u'DRESSED'), (u'Bacchei', u'ululatus', u'Obstrepuere'), (u'Back-to-Front', u'Inside-Out', u'Upside-Down'), (u'Beanstanes', u'so\xf0e/', u'gel\xe6ste.'), (u'Berecyntia', u'tibia', u'cornu'), (u'Berrigan\u2026\u2026..my', u'dad\u2026\u2026..heart', u'attack\u2026\u2026..1958.'), (u'Bis', u'pueri', u'senes'), (u'Bo', u'Peep.', u'\u201cBow-wow'), (u'Braeburn.', u'Jonagold.', u'Cameo.'), (u'Brandy-brown.', u'Leaf-brown.', u'Russet.'), (u'Bretagne\u2019s', u'off-kilter', u'menhirs'), (u'Bruc', u'\xf0isses', u'beages'), (u'CORNER.', u'Giulietta', u'Masina'), (u'Campo', u'dei', u'Fiori'), (u'Cantabit', u'vacuus', u'coran'), (u'Carolyn', u'Kizer\u2019s', u'knife-blade'), (u'Charactersrobot', u'leaderrobot', u'tworobot'), (u'Chauvet.', u'Alsace.', u'Lorraine.'), (u'Cheerfull', u'Winter.', u'Oceanus'), (u'Circacircacircacircacircacircacircacircacircacircacircacircacircacirca', u'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', u'1515151515151515151515151515151515151515151515151515151'), (u'Cokes\u2014or', u'staring\u2014Louis', u'humiliated\u2014Naomi'), (u"Cretan's", u'Hymni', u'Deorum'), (u'Curio', u'Fabricioque', u'licet'), (u'Dame\x97', u'Motley', u'accoutrement'), (u'Datta.', u'Dayadhvam.', u'Damyata.'), (u'Dayadhvam.', u'Damyata.', u'Shantih'), (u'Desiray', u'Kierra', u'Chee'), (u'Despot.', u'Fortnight.', u'Bilge.\u201d'), (u'Detective', u'Gregg', u'Messing'), (u'Dieser', u'Flucht', u'folgt'), (u'Dieu.', u'Ores', u"m'en"), (u'Dugan\u2026\u2026..my', u'grandfather\u2026\u2026..throat', u'cancer\u2026\u2026..1947.'), (u'EZRA', u'POUND', u'IL'), (u'Ecg\xfeeow', u'haten.', u'Gebad'), (u'Eighth.', u'Ninth.', u'Twelfth.'), (u'Elanor\u2019s', u'Rheumatic', u'Heart\u2014'), (u'Engineer', u'Sr.', u'\xc1lvaro'), (u'Engraved.', u'Incorrectly.', u'Discarded.'), (u'Epictetus', u'APPROACH', u'LIFE'), (u'Eu-', u'phu-', u'es.'), (u'Euro-', u'p\xe4ische', u'Literatur'), (u'Exogamous', u"Bride'.", u'Anyhow'), (u'FALSE', u'CARCASS', u'ECONOMY'), (u'FEWER', u'WIVES', u'WOULD'), (u'FISH', u'SHOULD', u'SWALLOW'), (u'FLIGHT', u'INTO', u'EGYPT'), (u'Fahd', u'ibn', u'Abdel'), (u'Far-swooping', u'elbow\u2019d', u'earth\u2014rich'), (u'Father.\u2019', u'\u2018Fair', u'Enough.\u2019'), (u'Finne', u'eal/', u'unhlitme.'), (u'First-person', u'dwindle.', u'Tweet-tweet.'), (u'Fletcher.', u'Glover.', u'Miller.'), (u'Forsythe', u'Irwin', u'Bourgois'), (u'Freezy', u'Freakies\u2019', u'once-invisible'), (u'Frostbite.', u'Grenades.', u'Stretchers.'), (u'Fruit-trees', u'overwoodie', u'reachd'), (u'GREAT', u'FISH', u'SHOULD'), (u'Giganta', u'facis.', u'iv.49'), (u'Gingko-balboa', u'azatine', u'melamine'), (u'Glacier.', u'Despot.', u'Fortnight.'), (u'Gloucester\u2014old', u'Gorton\u2019s', u'Wharf'), (u'Glover.', u'Miller.', u'Glazer.'), (u'Grenades.', u'Stretchers.', u'Coffins.'), (u'Groped', u'massaged', u'turgescent'), (u'Gu\xf0rinc', u'astah.', u'Wand'), (u'HERO', u'FOUNDS', u'REPUBLIC'), (u'HOUSE.', u'OTTO', u'VON'), (u'Heorute', u'ateah.', u'Dryhtsele'), (u'Herz', u'ist', u'm\xfcde.'), (u'HistoryAll', u'motivations', u'intermingle'), (u'Hockey', u'All-State\u2026\u2026car', u'crash\u2026.1959.'), (u'Hon', u'Kee', u'Grocery'), (u'Horrific.', u'Grisly.', u'\u201cRumplestiltskin'), (u'Hro\xf0gare', u'heresped', u'gyfen')]
[Finished in 96.3s]

############################################
with apply_freq_filter(3) and apply_word_filter
Still almost worthless.
NOTE (u'Seven', u'swans', u'a-swimming') etc... christmas carol only occurs once in corpus

[(u'Plunge.', u'Push.', u'Lift.'), (u'Push.', u'Lift.', u'Toss'), (u'Ejido', u'San', u'Quintin'), (u'Eight', u'maids', u'a-milking'), (u'whack', u'whack', u'whack'), (u'lady', u'\u201cnegro', u'poet\u201d'), (u'Nine', u'drummers', u'drumming'), (u'Great', u'Britian', u'__________'), (u'Seven', u'swans', u'a-swimming'), (u'Evening', u'falls.', u'Someone\u2019s'), (u'Bash\u014d\u2019s', u'traveling', u'companion'), (u'Ten', u'pipers', u'piping'), (u'Six', u'geese', u'a-laying'), (u'Red', u'Riding', u'Hood'), (u'Goddess', u'excellently', u'bright.'), (u'Quitte', u'Pas', u'beneath'), (u'Pas', u'beneath', u'mesquite.'), (u'theyr', u'eccho', u'ring.'), (u'Queen', u'Anne\u2019s', u'lace.'), (u'Phenomenally.', u'Phenomenal', u'woman'), (u'woman', u'Phenomenally.', u'Phenomenal'), (u'I\u2019m', u'Chatty', u'Cathy.'), (u'\u2019cause', u'Stink', u'Eye'), (u'Color', u'appears', u'Falls'), (u'Pointed', u'out.', u'And.'), (u'jug', u'jug', u'jug'), (u'falls.', u'Someone\u2019s', u'playing'), (u'Lower', u'East', u'Side'), (u'Lift.', u'Toss', u'it.'), (u'easily.', u'Pointed', u'out.'), (u'hello', u'hello', u'hello'), (u'thy', u'sonne', u'softe'), (u'good', u'Haroun', u'Alraschid.'), (u'girl', u'sells', u'purses'), (u'beautiful', u'Annabel', u'Lee'), (u'Three', u'French', u'hens'), (u'Two', u'turtle', u'doves'), (u'clearly', u'expressing', u'something.'), (u'Four', u'colly', u'birds'), (u'Beside', u'remote', u'Shalott.'), (u'crowded', u'hill', u'bordering'), (u'Fifteen', u'responsible', u'children'), (u'done', u'moy', u'duty'), (u'Clozapine.', u'\u201cDon\u2019t', u'take'), (u'bold', u'Sir', u'Bedivere'), (u'poem', u'originally', u'appeared'), (u'sheer', u'luminous', u'gown'), (u'moy', u'duty', u'boy'), (u'Google', u'anybody', u'else'), (u'Old', u'court.', u'Old'), (u'hath', u'xxxi', u'days.'), (u'woodchuck', u'could', u'chuck'), (u'hath', u'xxx', u'days.'), (u'79th', u'street', u'station'), (u'bullets', u'hushed', u'her.'), (u'don\u2019t', u'Google', u'anybody'), (u'portrait', u'done', u'instead.'), (u'sells', u'purses', u'made'), (u'filed', u'new', u'charges'), (u'Easily', u'pointed', u'out.'), (u'greatly', u'expressing', u'something'), (u'Ain\u2019t', u'got', u'nobody'), (u'New', u'York', u'Times'), (u'conversations', u'great', u'piles'), (u'woods', u'shal', u'answer'), (u'Mocks', u'married', u'men'), (u'Since', u'Persia', u'fell'), (u'I\u2019ve', u'felt', u'undeserving.'), (u'ones', u'clearly', u'expressing'), (u'caged', u'bird', u'sings'), (u'replied', u'King', u'Arthur'), (u'felt', u'undeserving.', u'I\u2019ve'), (u'Five', u'gold', u'rings'), (u'forsaken', u'city', u'starts'), (u'New', u'York', u'City'), (u'narrow', u'girl', u'sells'), (u'Dear', u'mother', u'Ida'), (u'raineth', u'every', u'day.'), (u'small', u'San', u'Francisco'), (u'one', u'eyed', u'shrew'), (u'hello', u'hello', u'...'), (u'clearly', u'expressing', u'something'), (u'spake', u'King', u'Arthur'), (u'easily', u'pointed', u'out.'), (u'Wilt', u'thou', u'forgive'), (u'wont', u'cure', u'it.'), (u'say', u'ray', u'comb'), (u'undeserving.', u'I\u2019ve', u'made'), (u'spoke', u'King', u'Arthur'), (u'great', u'god', u'Pan'), (u'rubber', u'band', u'around'), (u'Peace', u'say', u'ray'), (u'thirty', u'years', u'ago.'), (u'four', u'foot', u'bench'), (u'kill', u'kill', u'kill'), (u'glad', u'mad', u'brother'), (u'losing', u'isn\u2019t', u'hard'), (u'bad', u'glad', u'mad'), (u'five', u'foot', u'bench'), (u'three', u'little', u'kittens')]
[Finished in 106.3s]


##################
TRIgrams RETURNS 

with apply_freq_filter(10)
after deleting christmas carol

Another worthless run: two phrases reoccur...
and there are only 7 results returned.
Note NYC occurs in both lists....
Does "good Haroun Alraschid." really occur 10 times?
I begin to suspect my implementation or understanding is wrong.

good Haroun Alraschid.
clearly expressing something.
bold Sir Bedivere
greatly expressing something
New York City
Dear mother Ida
clearly expressing something
... ... ...

[Finished in 106.2s]

"""
