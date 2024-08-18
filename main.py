import os
import re
import requests

def get_playlist(playlist_id,cookie):
    playlist_url = f"https://music.163.com/api/playlist/detail?id={playlist_id}"
    playlist_list = requests.get(playlist_url,headers={"Cookie":cookie}).json()
    
    if not playlist_list["code"] == 200:
        return(1)
    
    songs_count = len(playlist_list["result"]["tracks"])
    print(f"Name:{playlist_list['result']['name']} ID:{playlist_list['result']['id']}")
    if songs_count >= 2:
        print(f"There are {songs_count} songs in this playlist.")
    else:
        print(f"There is {songs_count} song in this playlist.")
        rerrr
    return(playlist_list) #获取歌单然后返回一个列表

def download_playlist(playlist,mode="name",path=".//playlist//"):
     #文件名非法字符会被转换成这个
    if playlist["code"] != 200 or playlist == 1:
        return(1)
    playlist_path = f"{path}//{playlist['result'][mode]}"
    if not os.path.exists(playlist_path):
        os.makedirs(playlist_path) #没有文件夹就新建
    
    replace_character = ""
    for song in playlist["result"]["tracks"]: #遍历歌单
        song_url = f"https://music.163.com/song/media/outer/url?id={song['id']}"
        song_name = re.sub(r"[\/\\\:\*\?\"\<\>\|]",replace_character,song[mode])
        song_path = f"{playlist_path}//{song_name}.mp3" #替换非法字符
        
        if os.path.exists(song_path):
            print(f"{song_name} is exist")
            continue
        
        print(f"Downloading {song['name']}.")
        with open(song_path, "wb") as song_file:
            song_file.write(requests.get(song_url).content) #保存文件
        print("Succeed.")

    return(0)
if __name__ == "__main__":
    try:
        while True:
            enter_id = input("Please enter playlist ID.")
            if enter_id.isdigit():
                break
            print("This playlist ID is wrong.")
        enter_mode = input("You can choose the file naming rule ( name (default) / id ) or you can skip.")
        if enter_mode == "":
            enter_mode = "name"
        enter_path = input("You can set the path.( ./playlist/ )")
        if enter_path == "":
            enter_path = "./playlist/"
        enter_cookie = input("Please enter your cookie.If you didn't enter cookie,you can only download 10 songs.")
        if download_playlist(get_playlist(enter_id,enter_cookie),enter_mode,enter_path):
            print("Over.")  
    #except:
        #print("Error.")
    finally:
        pass
