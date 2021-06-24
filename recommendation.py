import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import csv
import pyrebase
from firebase import Firebase

config = {
    "apiKey": "AIzaSyCl62bFlfmX6EFeM3YERrU5AyD2QMfhV-Y",
    "authDomain": "whattocook-cs63.firebaseapp.com",
    "databaseURL": "https://whattocook-cs63-default-rtdb.firebaseio.com",
    "projectId": "whattocook-cs63",
    "storageBucket": "whattocook-cs63.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
dataset = db.child("datasets").get()

with open('thai_menu.csv','w', encoding="utf-8" ,newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id','description'])

    for data in dataset.each():
        writer.writerows([[str(data.key()),str(data.val())]])

ds = pd.read_csv("thai_menu.csv")
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['description'].values.astype('U'))
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

    results[row['id']] = similar_items[1:]
        
print('done!')

def recommend(item_id, num):

    dataset = db.child("datasets").get()

    with open('thai_menu.csv','w', encoding="utf-8" ,newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id','description'])

        for data in dataset.each():
            writer.writerows([[str(data.key()),str(data.val())]])

    ds = pd.read_csv("thai_menu.csv")

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['description'].values.astype('U'))
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

        results[row['id']] = similar_items[1:]
            
    print('done!')
    print(item_id)
    print('in')
    print("-------")
    recs = results[item_id][:num]
    print(recs)

    return recs
