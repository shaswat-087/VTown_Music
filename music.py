import numpy as np
import pandas as pd

df=pd.read_csv('Vtown.csv')
info=df[['track_id','title','artist','actor']]
actor_counts = df['actor'].value_counts()
artist_counts = df['artist'].value_counts()


df['actor_weight'] = df['actor'].map(actor_counts).fillna(0) / 100
df['artist_weight'] = df['artist'].map(artist_counts).fillna(0) / 100
feature=df[['actor_weight','artist_weight','energy','danceability','valence']]
x=df['energy'].median()
y=df['valence'].median()
arr=feature.to_numpy()
conditions=[
      (df['energy']>=x) & (df['valence']>=y),
      (df['energy']<=x) & (df['valence']>=y),
      (df['energy']>=x) & (df['valence']<=y),
      (df['energy']<=x) & (df['valence']<=y)
]

quadrant_labels=[
      'Party',
      'Chill',
      'Gym & Workout',
      'Sad Songs'
]

df['playlist']=np.select(conditions,quadrant_labels,default="Mix")
gym=df[df['playlist']=='Gym & Workout']
gym_sorted=gym.sort_values(by='energy',ascending=False)
print("Your gym & workout mix \n",gym_sorted['title'])

party=df[df['playlist']=='Party']
print("Your party mix \n",party['title'])
 

content=df['title'].str.strip().str.lower()
while True:
     choice=input("Search a song you want to listen . Press 5 to exit \n").strip().lower()
     if choice=='5':
        print("Successful Exit")
        break
     found=False
     for i,song in enumerate(content):
          if song==choice:
                 print(f"\nFound {choice} on row {i}")
                 found=True
                 index=i
                 
     if found:
            target=arr[index]   
     if not found:
            print(" Not found. Try Searching Again ")



     distance=np.linalg.norm(arr-target,axis=1)
     sorted=np.argsort(distance)
     top_10=sorted[1:11]
     print("Here are top 10 songs you would like next")
     print(df.iloc[top_10]['title'])

