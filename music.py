import numpy as np
import pandas as pd

df=pd.read_csv('Vtown_Final.csv')
info=df[['track_id','title','artist','actor']]
actor_counts = df['actor'].value_counts()
artist_counts = df['artist'].value_counts()
play_counts={}

df['actor_weight'] = df['actor'].map(actor_counts).fillna(0) / 100
df['artist_weight'] = df['artist'].map(artist_counts).fillna(0) / 100
feature=df[['actor_weight','artist_weight','energy','danceability','valence']]
x=df['energy'].median()
y=df['valence'].median()
z=df['danceability'].median()
arr=feature.to_numpy()
conditions=[
      (df['energy']>=x) & (df['valence']>=y) & (df['danceability']>=z),
      (df['energy']>=x) & (df['valence']>=y) & (df['danceability']<=z),

      (df['energy']<=x) & (df['valence']>=y) &(df['danceability']>=z),
      (df['energy']<=x) & (df['valence']>=y) &(df['danceability']<=z),

      (df['energy']>=x) & (df['valence']<=y) &(df['danceability']>=z),
      (df['energy']>=x) & (df['valence']<=y) &(df['danceability']<=z),
  
      (df['energy']<=x) & (df['valence']<=y) & (df['danceability']>=z),
      (df['energy']<=x) & (df['valence']<=y) & (df['danceability']<=z)
]

quadrant_labels=[
      'Party',
      'Feel Good',
      'Romance',
      'Relax',
      'Work Out',
      'Energize',
      'Focus',
      'Sad'
  
      
]
 
df['playlist']=np.select(conditions,quadrant_labels,default="Mix")

content=df['title'].str.strip().str.lower()
user=np.array([0.2,0.2,0.5,0.5,0.5])
N=0
df['distance'] = np.linalg.norm(arr - user, axis=1)
top_10 = np.argsort(df['distance'].to_numpy())[:10]
while True:
       menu_choice=int(input("Press 1 to Search \n 2 to View Feed \n 3 to View Playlist \n 4 to View Repeat Tracks \n 5 to exit"))

       if menu_choice==5:
        print("Successful Exit")
        break
       if menu_choice==1:
         choice=input("Search a song you want to listen . \n").strip().lower()
         found=False
         for i,song in enumerate(content):
            if song==choice:
                 print(f"\nFound {choice} on row {i}")
                 found=True
                 index=i
                 N=N+1
                 a=1/N
                 track_id=df.iloc[i]['track_id']
                 user=((1-a)*user)+(a*arr[i])
                 play_counts[track_id]=play_counts.get(track_id,0)+1
                 break
                 
         if found:
            target=user
            distance=np.linalg.norm(arr-target,axis=1)
            df['distance'] = distance
            sorted=np.argsort(distance)
            top_10=sorted[1:11]
         else:
           print("Song Not Found. Try Searching Again .")

       if menu_choice==2:
            print("Here are top 10 songs you would like next")
            print(df.iloc[top_10]['title'])
       if menu_choice==3: 
            for label in quadrant_labels:
                 sorted_playlist=df[df['playlist']==label].sort_values(by='distance')

                 if not sorted_playlist.empty:
                    print(f"\nYour {label} Mix:")
                    print(sorted_playlist['title'].to_string(index=True))
       if menu_choice==4:
            for track_id,count in play_counts.items():
                if  count>5:
                       print("Listen Again ")
                       print(df[df['track_id']==track_id]['title'])
       
       
    
