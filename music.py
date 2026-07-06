import numpy as np
import pandas as pd
from flask import Flask, render_template, url_for, request, redirect, jsonify

app=Flask(__name__)
@app.route("/")
def index():
    global user
    feed=recommend(user)
    repeat_list=[]
    for track_id,count in play_counts.items():
     row=df[df['track_id']==track_id]
     if  count>5:
        if not row.empty:
            repeat_list.append({
                    "title": row.iloc[0]['title'],
                    "artist": row.iloc[0]['artist'],
                    "cover": row.iloc[0]['image_url']

                })

    return render_template('index.html',feed=feed,repeat_tracks=repeat_list)

df=pd.read_csv('Vtown_Final.csv')
info=df[['track_id','title','artist','actor',"image_url"]]
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
history_order=[]
@app.route('/search',methods=['POST'])
def search():
         global N,user
         choice=request.form['choice'].strip().lower()
         found=False
         for i,song in enumerate(content):
            if song==choice:
                 found=True
                 index=i
                 N=N+1
                 a=1/N
                 track_id=df.iloc[i]['track_id']
                 user=((1-a)*user)+(a*arr[i])
                 play_counts[track_id]=play_counts.get(track_id,0)+1
                 if track_id in history_order:
                     history_order.remove(track_id)
                 history_order.insert(0,track_id)
                 break
                 
         if found:
            
            searched_song = {
            "title": df.iloc[index]['title'],
            "artist": df.iloc[index]['artist'],
            "cover": df.iloc[index]['image_url'] 
             }
            target=arr[index]
            search_feed=recommend(target)
            return render_template("index.html",msg=f"Found {choice}",song=searched_song,search_feed=search_feed)

         else:
           return render_template("index.html",msg="Song Not Found. Try Searching Again .")

def recommend(target):
      distance=np.linalg.norm(arr-target,axis=1)
      df['distance'] = distance
      sorted=np.argsort(distance)
      top_10=sorted[1:11]
      feed_list=[]
      for i,song in enumerate(top_10):
        feed={
           "title": df.iloc[song]['title'],
            "artist": df.iloc[song]['artist'],
            "cover": df.iloc[song]['image_url']    
        
           
          }
        feed_list.append(feed)
      return feed_list

@app.route('/playlists')
def playlist():
    global N,user
    if N==0:
        return render_template("index.html", msg="Try searching to get started", playlists={})
        
    playlist_data={}
    
    distance=np.linalg.norm(arr - user, axis=1)
    df['distance']=distance

    for label in quadrant_labels:
        sorted_playlist=df[df['playlist'] == label].sort_values(by='distance')
        
        if not sorted_playlist.empty:
            tracks_list=[]
            for i, row in sorted_playlist.iterrows():
                tracks_list.append({
                    "title": row['title'],
                    "artist": row['artist'],
                    "cover": row['image_url']
                })
            playlist_data[label]=tracks_list

    return render_template("index.html", playlists=playlist_data)

@app.route("/history")
def history():
    global history_order
    if not history_order:
        print("Try searching to get started ")
     
    history_list=[]
    
    for track_id in history_order:
        row=df[df['track_id']==track_id]
        if not row.empty:
          
                history_list.append({
                    "title": row.iloc[0]['title'],
                    "artist": row.iloc[0]['artist'],
                    "cover": row.iloc[0]['image_url']

                })
   
         


    return render_template("index.html", history_tracks=history_list)


if __name__== "__main__":
    app.run(debug=True)
