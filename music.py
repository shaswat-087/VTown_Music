import numpy as np
import pandas as pd

df=pd.read_csv('Vtown.csv')
info=df[['track_id','title','artist','actor']]
actor_counts = df['actor'].value_counts()
artist_counts = df['artist'].value_counts()


df['actor_weight'] = df['actor'].map(actor_counts).fillna(0) / 100
df['artist_weight'] = df['artist'].map(artist_counts).fillna(0) / 100
feature=df[['actor_weight','artist_weight','energy','danceability','valence']]


arr=feature.to_numpy()
A=arr[1]
modA=np.linalg.norm(A)
all_dot=arr@A
all_mod=np.linalg.norm(arr,axis=1)
cosine=all_dot/(all_mod*modA)  # Using formula cos theta =A.B/|A||B|
sorted=np.argsort(-cosine)
top_10=sorted[1:11]
print(df.iloc[top_10]['title'])