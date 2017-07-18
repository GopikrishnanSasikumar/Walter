import pandas as pd 
import scipy as sp
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
def fitandpredict(newpost,num=5):
    pkl_file=open('first.pkl','rb')
    df=pickle.load(pkl_file)
    pkl_file.close()
    #df=df1['Title of Book'].values.tolist()
    vectorizer=CountVectorizer(min_df=1,stop_words='english')
    vectorized=vectorizer.fit_transform(df)
    num_cluster=10
    km=KMeans(n_clusters=num_cluster,init='random',n_init=1,verbose=1)
    km.fit(vectorized)
    labels=km.labels_
    new_post=newpost
    new_post_vec = vectorizer.transform([new_post])
    new_post_label = km.predict(new_post_vec)[0]
    similar_indices = (labels==new_post_label).nonzero()[0]
    similar=[]
    for i in similar_indices:
        dist = sp.linalg.norm((new_post_vec - vectorized[i]).toarray())
        similar.append((dist, df[i]))
    similar = sorted(similar)
    sim=[]
    for i,j in similar:
        sim.append(j)
        similar=sim
    return similar[:num]
