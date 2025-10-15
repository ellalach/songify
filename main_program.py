import requests
import base64
import json
import random

#client id and secret created from spotify's api
CLIENT_ID= #given id
CLIENT_SECRET= #given secret 

#declare a command to get spotify's access token
def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes),"utf-8")
    
    url="https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data={"grant_type": "client_credentials"}
    result=requests.post(url, headers=headers, data=data)
    
    json_result=json.loads(result.content)

    token=json_result["access_token"]
    return token
 
 
#declare a command to easily access the correct format for token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
    
    
#create command for id search for artists
def search_for_artist(token, artist_name):
    url='https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    
    query=(f'?q={artist_name}&type=artist&limit=1')
    query_url=url+query
    
    result=requests.get(query_url, headers=headers)
    json_result=json.loads(result.content)
    json_result=json.loads(result.content)['artists']['items']
    
    if len(json_result)==0:
        print("Sorry, no artist with this name exists.")
        return None
    else:
        return json_result[0]
        
        
#declare a command to get an artists top 10 songs
def get_songs(token, artist_id):
    url=(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US")
    headers=get_auth_header(token)
    
    result=requests.get(url,headers=headers)
    json_result=json.loads(result.content)["tracks"]
    return json_result


#declare command to get an artist latest 1-20 albums
def get_albums(token, artist_id):
        url=(f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album&market=US")
        headers=get_auth_header(token)
        
        result=requests.get(url,headers=headers)
        json_result=json.loads(result.content)["items"]
        return json_result
       
 
#main code

print("\nWelcome to the song reccomendation program!")
print("Based on the artist of your choice, this program will find an artist in the same genre and reccomend their top 10 songs to you!")

#create flag variable and while look
is_running=True
while is_running:
    
    artist=input("\nPlease enter the artist of your choice: ")

    #gather artist id and genre based on inputed artist
    token=get_token()
    result=search_for_artist(token, artist)
    artist_id=result['id']
    artist_genres=result['genres']

    print("Okay! Loading...")
    input("Press enter to see your artist stats.")

    print(f"\nShowing results for {artist}")
    print(f"\n{artist}'s top ten song:")
    songs=get_songs(token, artist_id)
    for idx, song in enumerate(songs):
        print(f"\t{idx+1}. {song['name']}")
    print(f"\n{artist}'s lastest albums:")
    albums=get_albums(token,artist_id)
    for idx, album in enumerate(albums):
        print(f"\t{idx+1}. {album['name']}")
    
    
    data_file="C:\\Users\\lache\\code\\songify\\ella_genre.json"
    #load ella_recommendations
    with open(data_file,"r") as file:
        contents=json.load(file)

    #check for avaliable genre
    genre_found=False
    if not artist_genres:
        chosen_genre = "pop"
        genre_found = True
    for genre in artist_genres:
        if genre in contents:
            genre_found=True
            chosen_genre=genre
            break
        else:
            pass
    if genre_found==False:
        print("Sorry I don't have similar artists for you")
    else:
        pass

    #choose random artist based on genre 
    if genre_found==True:
        input("\nPress enter to see your recommended artist.")
    
        artist=random.choice(contents[chosen_genre])
        print(f"\nMy reccomended artist for you is {artist}")
    
        print("Here are their top ten songs:")
    
        artist_result=search_for_artist(token, artist)
        artist_id=artist_result['id']
        rec_artist=artist_id

        #print reccomended songs
        rec_songs=get_songs(token,rec_artist)
        for idx, song in enumerate(rec_songs):
            print(f"\t{idx+1}. {song['name']}")
    else:
        pass
    #ask user if they'd like to continue entering artists
    user_choice=input("\nWould you like to enter another artist (y/n): ")
    
    if user_choice.startswith('n'):
        print("Okay exiting...")
        is_running=False
        
    else:
        pass
    
