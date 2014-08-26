import matplotlib.pyplot as plt
import os, datetime
import re

import import_utilities

from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE

from sklearn.feature_extraction.text import TfidfVectorizer

type_of_run="ALL"
READ_PATH = "../../../../../data/poetry/lyrics/txt_poems_"+type_of_run+"/"

cnt =0
poems = []
authors =[]
titles = []
ids=[]

for subdir, dirs, files in os.walk(READ_PATH):
    for file in files:
        if ".txt" in file  and 'readme' not in file:
            if os.path.isfile(subdir+file):
                #print subdir+file
                txt_data=open(subdir+file).read()
                txt_data_split = txt_data.split("****!****")

                ids.append(file.split(".txt")[0])
                authors.append(txt_data_split[0].strip("\n"))
                titles.append(txt_data_split[1].strip("\n"))
                # pt =  re.sub('.*~~~~!~~~', '',txt_data_split[2])
                # poems.append(pt.strip("\n"))
                poems.append(txt_data_split[2])

# print authors
# print titles
# print poems

vectors = TfidfVectorizer().fit_transform(poems)
print("Tfid fit transform complete.")
print(repr(vectors))

# '''
# For high-dimensional sparse data it is helpful to first reduce the dimensions to 50 dimensions with TruncatedSVD and then perform t-SNE. This will usually improve the visualization.
# '''

def tsne(comp,perp,lr,init):

    print "N_components (fed to SVD) :",comp
    print "Perplexity (fed to TSNE) :",perp
    print "learning_rate (fed to TSNE) :",lr
    print "init(fed to TSNE) :",init

    X_reduced = TruncatedSVD(n_components=50, random_state=0).fit_transform(vectors)
    X_embedded = TSNE(n_components=comp, perplexity=perp, verbose=2,learning_rate=lr,init=init).fit_transform(X_reduced)

    # width and height of image
    iw=16
    ih=9

    fig = plt.figure(figsize=(iw, ih))
    fig.patch.set_facecolor('white')
    ax = plt.axes(frameon=False)
    plt.setp(ax, xticks=(), yticks=())
    plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,
                    wspace=0.0, hspace=0.0)
    plt.scatter(X_embedded[:, 0], X_embedded[:, 1],
            c='black', marker=".")
    fig.savefig("img/"+datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')+"_TSNE_LYRICS_NO_ANNOTATION"+type_of_run+"_perp"+str(perp)+"_comp"+str(comp)+"_lr"+str(lr)+"_"+str(init)+"_300dpi_1wh.png", transparent=False,dpi=300)


    fig = plt.figure(figsize=(iw*2,ih*2))
    fig.patch.set_facecolor('white')
    ax = plt.axes(frameon=False)
    plt.setp(ax, xticks=(), yticks=())
    plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,
                    wspace=0.0, hspace=0.0)
    plt.scatter(X_embedded[:, 0], X_embedded[:, 1],
            c='black', marker=".")
    fig.savefig("img/"+datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')+"_TSNE_LYRICS_NO_ANNOTATION"+type_of_run+"_perp"+str(perp)+"_comp"+str(comp)+"_lr"+str(lr)+"_"+str(init)+"_300dpi_2wh.png", transparent=False,dpi=300)

    fig = plt.figure(figsize=(iw*3,ih*3))
    fig.patch.set_facecolor('white')
    ax = plt.axes(frameon=False)
    plt.setp(ax, xticks=(), yticks=())
    plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,
                    wspace=0.0, hspace=0.0)
    plt.scatter(X_embedded[:, 0], X_embedded[:, 1],
            c='black', marker=".")
    fig.savefig("img/"+datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')+"_TSNE_LYRICS_NO_ANNOTATION"+type_of_run+"_perp"+str(perp)+"_comp"+str(comp)+"_lr"+str(lr)+"_"+str(init)+"_300dpi_3wh.png", transparent=False,dpi=300)


    X = X_embedded.tolist()
    for idx,x in enumerate(X):
        x.extend([authors[idx], titles[idx], ids[idx]])

    #print X
    # SAVE to txt file as csv for later import to d3
    txt_fn = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')+"_LYRICS_TSNE_"+type_of_run+"_perp"+str(perp)+"_comp"+str(comp)+"_lr"+str(lr)+"_"+str(init)+".txt"

    txt_fn_path = "txt/"+txt_fn
    f_txt=open(txt_fn_path,'w')
    f_txt.write("x,y,author,title,id")
    for x in X:
        f_txt.write("\n")
        for idx,item in enumerate(x):
          if idx == 4:
            f_txt.write("\"%s\"" % item)
          elif type(item) is str:
            f_txt.write("\"%s\"," % item)
          else:
            f_txt.write("%s," % item)

    f_txt.close();   
    "\nTXT file created at:",txt_fn_path



''' |  init : string, optional (default: "random")
 |      Initialization of embedding. Possible options are 'random' and 'pca'.
 |      PCA initialization cannot be used with precomputed distances and is
 |      usually more globally stable than random initialization.
 '''
# tsne(2,30,100,'pca')
# tsne(2,40,100,'pca')
# tsne(2,50,100,'pca')
# tsne(2,60,100,'pca')
# tsne(2,70,100,'pca')
# tsne(2,80,100,'pca')
# tsne(2,90,100,'pca')
# tsne(2,100,100,'pca')


#tsne(2,50,100,'pca')  # LOWEST [t-SNE] Error after 280 iterations: 0.992306
# tsne(2,50,100,'random')
# tsne(2,50,500,'pca')
# # tsne(2,50,500,'random')



tsne(2,40,1000,'pca')
tsne(2,40,1000,'random')
tsne(2,50,1000,'pca')
tsne(2,50,1000,'random')
tsne(2,60,1000,'pca')
tsne(2,60,1000,'random')

# raising perplexity
# tsne(2,30,100)
# tsne(2,40,100)
# tsne(2,50,100)
# tsne(2,60,100)
# tsne(2,70,100)
# tsne(2,80,100)
# tsne(2,90,100)
# tsne(2,100,100)


# raising learning rate seem
# tsne(2,40,100)
# tsne(2,40,200)
# tsne(2,40,300)
# tsne(2,40,400)
# tsne(2,40,500)
# tsne(2,40,600)
# tsne(2,40,700)
# tsne(2,40,800)
# tsne(2,40,900)
# tsne(2,40,1000)

# raising components decreases quality
# tsne(3,40,100)
# tsne(4,40,200)
# tsne(5,40,300)
# tsne(6,40,400)
# tsne(7,40,500)
# tsne(8,40,600)
# tsne(9,40,700)
# tsne(10,40,800)
# tsne(11,40,900)
# tsne(12,40,1000)

# tsne(2,5)
# tsne(2,10)
# tsne(2,20)
# tsne(2,30)
# tsne(2,40)
# tsne(2,50)

# tsne(3,40)
# tsne(5,40)
# tsne(6,40)
# tsne(7,40)
# tsne(8,40)

# tsne(9,90)

# tsne(3,50)
# tsne(3,60)
# tsne(3,70)

'''

learning_rate : float, optional (default: 1000)
 |      The learning rate can be a critical parameter. It should be
 |      between 100 and 1000. If the cost function increases during initial
 |      optimization, the early exaggeration factor or the learning rate
 |      might be too high. If the cost function gets stuck in a bad local
 |      minimum increasing the learning rate helps sometimes.

'''

