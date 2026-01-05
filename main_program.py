import tkinter as tk
import requests
import base64
import json
import random
import os

#color pallete
MAIN_COLOR = "#d2d2d2"
LIGHT_MAIN_COLOR="#e3e3e3"
SECONADRY_COLOR_1= "#41ae67"
ACCENT_COLOR_1= "#168c3f"
SECONADRY_COLOR_2= "#232323"
ACCENT_COLOR_2="#232323"
ACCENT_COLOR_3="#9c9898"

#font pallete
TITLE_FONT=("Metropolis-SemiBold", 18, "bold")
MAIN_FONT=("Metropolis-SemiBold", 12)
SECONDARY_FONT=("Metropolis-SemiBold", 12)

class apiCalls:
    def __init__(self):
        """initialize attributes for api class"""
        #client id and secret are created from spotify's api
        self.CLIENT_ID='ebb61d68f0e3462698fa145f46d2b154'
        self.CLIENT_SECRET='5606692bad1b487ba5d9c49b8d410900'

        self.get_token()

    def get_token(self):
        """get spotifyAPI's access token, this will be used to call functions from spotify's API"""
        auth_string = (f"{self.CLIENT_ID}:{self.CLIENT_SECRET}")
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

        self.token=json_result["access_token"]

        self.auth_token={"Authorization": "Bearer " + self.token}
    

    def search_for_artist(self, artist_name=None):
        """search for artist and gather their id and genre"""
        if artist_name==None:
            self.artist_name=self.artist_name
        else:
            self.artist_name=artist_name

        url='https://api.spotify.com/v1/search'
        headers=self.auth_token

        query=(f'?q={self.artist_name}&type=artist&limit=1')
        query_url=url+query
        
        result=requests.get(query_url, headers=headers)
        json_result=json.loads(result.content)
        artists = json_result["artists"]["items"]
        if len(artists) == 0:
            print("Sorry, no artist with this name exists.")
            return

        artist = artists[0]
        self.artist_id = artist["id"]
        self.artist_genre = artist["genres"]
    

    def get_songs(self):
        """use artist id and auth token to access artist top 10 tracks and print them"""
        url=(f"https://api.spotify.com/v1/artists/{self.artist_id}/top-tracks?country=US")
        headers=self.auth_token

        result=requests.get(url,headers=headers)
        artist_tracks=json.loads(result.content)["tracks"]

        return artist_tracks

    def get_albums(self):
        """use artist id and auth token to access artists 20 latest albums also print them"""
        url=(f"https://api.spotify.com/v1/artists/{self.artist_id}/albums?include_groups=album&market=US")
        headers=self.auth_token
        result=requests.get(url,headers=headers)
        artist_albums=json.loads(result.content)["items"]
        
        return artist_albums

    def rec_artist(self):
        """aks user if they want to be recommended an artist, then use that id to to print artists top 10 songs"""
        
        self.script_dir=os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(self.script_dir, "ella_genre.json"), 'r') as file:
            contents=json.load(file)

            #check for avaliable genre
            if not self.artist_genre:
                chosen_genre="pop" #spotify API does not recognize pop genre in contents, so this is fixing that bug
                genre_found=True
            for genre in self.artist_genre:
                if genre in contents:
                    genre_found=True
                    chosen_genre=genre
                    break
            
            if genre_found==False:
                suggested_artist="We have no reccomendations for you at this time."

            if genre_found==True:
                suggested_artist=random.choice(contents[chosen_genre])
 
        return suggested_artist
            
    
    def run_program(self):
        self.get_token()
        self.search_for_artist()
        self.get_songs()
        self.get_albums()
        self.rec_artist()

class songifyapp:
    def __init__(self, root):
        """initialize attributes"""
        self.root=root
        self.root.title("Songify")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.config(bg=MAIN_COLOR)

        #Get the apiCalls classs
        self.apiCalls = apiCalls()
        
        #values= songs, albums, reccomended artist
        self.mode_var=tk.StringVar(value="artist")

        #start building the ui
        self.build_ui()

        self.artist_entry.bind("<FocusIn>", self.remove_placeholder_text)
        self.mode_var.trace_add("write", self.update_label)


    def build_ui(self):
        """built the gui layout"""
        PADX=5
        PADY=5

        title_label=tk.Label(
            self.root, text="Songify", font=TITLE_FONT, bg=MAIN_COLOR, fg=ACCENT_COLOR_1
        )
        title_label.pack(padx=PADX, pady=PADY)

        tag_label=tk.Label(
            self.root, text="A Song Reccomendation App", font=MAIN_FONT, bg=MAIN_COLOR, fg=SECONADRY_COLOR_1
        )
        tag_label.pack(padx=PADX,pady=PADY)


        self.artist_entry=tk.Entry(
            self.root, width=36, font=MAIN_FONT, justify="center"
        )
        self.artist_entry.insert(0, "Input Artist Here")
        self.artist_entry.pack(padx=PADX,pady=PADY)
        
        run_btn=tk.Button(
            self.root, text="Enter", font=MAIN_FONT, bg=SECONADRY_COLOR_1, activebackground=ACCENT_COLOR_1,
            activeforeground="white", width=18, command=self.run
        )
        run_btn.pack(padx=PADX, pady=PADY)

        mode_frame=tk.Frame(self.root, bg=MAIN_COLOR)
        mode_frame.pack(padx=PADX,pady=PADY, fill="x")


        song_rb=tk.Radiobutton(
            mode_frame, text="Top Songs", variable=self.mode_var, value="songs", bg=MAIN_COLOR, activebackground=MAIN_COLOR, font=MAIN_FONT, fg=SECONADRY_COLOR_1, activeforeground=SECONADRY_COLOR_1
        )
        song_rb.grid(row=0,column=0,padx=PADX,pady=PADY)
        
        album_rb=tk.Radiobutton(
            mode_frame, text="Latest Albums", variable=self.mode_var, value="albums", bg=MAIN_COLOR, activebackground=MAIN_COLOR, font=MAIN_FONT, fg=SECONADRY_COLOR_1, activeforeground=SECONADRY_COLOR_1
        )
        album_rb.grid(row=0,column=1,padx=PADX,pady=PADY)

        artist_rb=tk.Radiobutton(
            mode_frame, text="Similar Artist", variable=self.mode_var, value="artist", bg=MAIN_COLOR, activebackground=MAIN_COLOR, font=MAIN_FONT, fg=SECONADRY_COLOR_1, activeforeground=SECONADRY_COLOR_1
        )
        artist_rb.grid(row=0,column=2,padx=PADX,pady=PADY)

        for i in range(3):
            mode_frame.columnconfigure(i, weight=1, uniform="cols")

        self.output_label=tk.Label(
            self.root, text="Similar Artist", font=TITLE_FONT, bg=MAIN_COLOR, fg=ACCENT_COLOR_1
        )
        self.output_label.pack(padx=PADX,pady=PADY)

        output_frame=tk.Frame(self.root)
        output_frame.pack(padx=PADX,pady=PADY)

        self.output_text=tk.Text(
            output_frame, wrap="word", height=20, width=70
        )
        self.output_text.pack(padx=PADX, pady=PADY, side="left")

        scroll_y=tk.Scrollbar(output_frame)
        scroll_y.pack(side="right", fill="y")

        scroll_y.config(command=self.output_text.yview)
        self.output_text.config(yscrollcommand=scroll_y.set)

        btn_frame=tk.Frame(
            self.root, bg=MAIN_COLOR
        )
        btn_frame.pack(padx=PADX, pady=PADY, fill="x")

        copy_btn=tk.Button(
            btn_frame, text="Copy Output", font=MAIN_FONT, bg=SECONADRY_COLOR_1, activebackground=ACCENT_COLOR_1,
            activeforeground="white", width=16, command=self.copy
        )
        copy_btn.grid(row=0, column=0, padx=PADX, pady=PADY)
        
        clear_btn=tk.Button(
            btn_frame, text="Clear", font=MAIN_FONT, bg=SECONADRY_COLOR_2, activebackground=ACCENT_COLOR_2, fg="white",
            activeforeground="white", width=16, command=self.clear
        )
        clear_btn.grid(row=0, column=1, padx=PADX, pady=PADY)

        quit_btn=tk.Button(
            btn_frame, text="Quit", font=MAIN_FONT, bg=SECONADRY_COLOR_2, activebackground=ACCENT_COLOR_2, fg="white",
            activeforeground="white", width=16, command=self.close
        )
        quit_btn.grid(row=0, column=2, padx=PADX, pady=PADY)

        for i in range(3):
            btn_frame.columnconfigure(i, weight=1, uniform="cols")

        props_label=tk.Label(
            self.root, text="legedary is a thug", font=SECONDARY_FONT, bg=MAIN_COLOR, fg=ACCENT_COLOR_3
        )
        props_label.pack(padx=PADX, pady=PADY)

    def remove_placeholder_text(self, event=None):
        """remove placeholder artist text"""
        self.artist_entry.delete(0,tk.END)

    def update_label(self, *args):
        """update the output label"""
        if self.mode_var.get()=="songs":
            self.output_label.config(text="Top Songs")
        elif self.mode_var.get()=="albums":
            self.output_label.config(text="Latest Albums")
        else:
            self.output_label.config(text="Similar Artist")
    
    def close(self, event=None):
        """close the application"""
        self.root.quit()

    def run(self):
        self.apiCalls.artist_name=self.artist_entry.get()
        self.apiCalls.search_for_artist()

        if self.mode_var.get()=="songs":
            self.get_top_songs()
        elif self.mode_var.get()=="albums":
            self.get_latest_albums()
        else:
            self.get_similar_artists()

    def get_top_songs(self):
        results=self.apiCalls.get_songs()
        self.output_text.delete("1.0", tk.END)
        for idx, song in enumerate(results):
            self.output_text.insert(tk.END, f"{idx+1}. {song['name']}\n")

    def get_latest_albums(self):
        results=self.apiCalls.get_albums()

        self.output_text.delete("1.0", tk.END)
        for idx, album in enumerate(results):
            self.output_text.insert(tk.END, f"{idx+1}. {album['name']}\n")

    def get_similar_artists(self):
        results=self.apiCalls.rec_artist()
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", results)

    def clear(self):
        self.artist_entry.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)

    def copy(self):
        root.clipboard_clear()
        root.clipboard_append(self.output_text.get("1.0", tk.END))
        root.update()

#main code
root=tk.Tk()
app=songifyapp(root)
root.mainloop()
