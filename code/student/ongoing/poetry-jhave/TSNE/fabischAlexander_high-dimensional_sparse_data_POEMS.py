import matplotlib.pyplot as plt
import os, datetime
import re

from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE

from sklearn.feature_extraction.text import TfidfVectorizer

type_of_run="ALL"
READ_PATH = "../../../../../data/poetryFoundation/txt_poems_"+type_of_run+"/"

cnt =0
poems = []
authors =[]
titles = []
ids=[]

for subdir, dirs, files in os.walk(READ_PATH):
    for file in files:
        if ".txt" in file  and 'readme' not in file:
            if os.path.isfile(subdir+file):
                print subdir+file
                txt_data=open(subdir+file).read()
                txt_data_split = txt_data.split("****!****")

                ids.append(file.split(".txt")[0])
                authors.append(txt_data_split[0].strip("\n"))
                titles.append(txt_data_split[1].strip("\n"))
                pt =  re.sub('.*~~~~!~~~', '',txt_data_split[2])
                poems.append(pt.strip("\n"))

# print authors
# print titles
# print poems

vectors = TfidfVectorizer().fit_transform(poems)
print(repr(vectors))

# '''
# For high-dimensional sparse data it is helpful to first reduce the dimensions to 50 dimensions with TruncatedSVD and then perform t-SN.head()E. This will usually improve the visualization.
# '''
X_reduced = TruncatedSVD(n_components=50, random_state=0).fit_transform(vectors)
X_embedded = TSNE(n_components=2, perplexity=40, verbose=2).fit_transform(X_reduced)



fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor('white')
ax = plt.axes(frameon=False)
plt.setp(ax, xticks=(), yticks=())
plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,
                wspace=0.0, hspace=0.0)

plt.scatter(X_embedded[:, 0], X_embedded[:, 1],
        c='black', marker=".")


fig.savefig("img/"+datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')+"_TSNE_poetryFoundation_NO_ANNOTATION"+type_of_run+".png", transparent=False)

for i, a in enumerate(authors):
    ax.annotate(a, (X_embedded[:, 0][i], X_embedded[:, 1][i]))
    #ax.annotate(a+"\n'"+titles[i]+"'", (X_embedded[:, 0][i], X_embedded[:, 1][i]))


#plt.show()
fig.savefig("img/"+datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')+"_TSNE_poetryFoundation_"+type_of_run+".png", transparent=False)


X = X_embedded.tolist()
for idx,x in enumerate(X):
    x.extend([authors[idx], titles[idx], ids[idx]])

print X
# SAVE to txt file as csv for later import to d3
txt_fn = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')+"_poetryFoundation_TSNE_"+type_of_run+".txt"

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



