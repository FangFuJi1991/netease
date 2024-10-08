import os
import re
import requests
#导入库

def download(ids : int, path : str = "", name : str = ""):
    if path == "":
        path = f"./song/"
    if name == "":
        name = ids
    #默认参数

    if os.path.exists(f"{ path }/{ name }.mp3"):
        print("Exists\n")
        return 1
    #文件是否存在

    url = f"https://music.163.com/song/media/outer/url?id={ ids }"
    song = requests.get(url)
    #请求音乐

    with open(f"{ path }/{ name }.mp3", "wb") as file:
        file.write(song.content)
    print("Succeed\n")
    return 0
    #写入文件

def download_album(ids : int, path = "./album/", cookie : str = ""):
    url = f"https://music.163.com/api/album/{ ids }"
    album = requests.get(url, headers = {"Cookie" : f"{ cookie }"}).json()
    #请求专辑

    code = album["code"]
    #状态码
    if code == 200: #OK
        album_name = album["album"]["name"]
        songs = album["album"]["songs"]
        songs_count = len(songs)
        #赋值专辑数据

        print(f"{ album_name }\n{ len(songs) } Songs")

        album_name = re.sub(r'[\\/:*?"<>|]', "", album_name)
        if not os.path.exists(f"{ path }/{ album_name }"):
            os.makedirs(f"{ path }/{ album_name }")
        #文件夹是否存在

        for song in songs:
            song_name = song["name"]
            song_index = songs.index(song) + 1
            song_fix = "0" * ( len(str(songs_count)) - len(str(song_index)) ) + str(song_index)
            #赋值歌曲数据

            print(f"{ song_index }/{ songs_count } { song_name } ...")

            song_name = f"{ song_fix } - { re.sub(r'[\\/:*?"<>|]', "", song_name) }"
            download(song["id"], f"{ path }/{ album_name }/", song_name)
            #处理名称下载歌曲
        print("Over")
        return 0

    elif code == 404: #未找到
        print("Not Found")
        return 404

    elif code == -447: #服务器繁忙
        print("Busy")
        return 447

    elif code == -462: #请输入Cookie
        print("Restart And Enter Cookie")
        return 462

    else: #未知
        print("Error")
        return 1

def download_playlist(ids : int, path = "./playlist/", cookie : str = ""):
    url = f"https://music.163.com/api/playlist/detail?id={ ids }"
    playlist = requests.get(url, headers = {"Cookie" : f"{ cookie }"}).json()
    #请求歌单

    code = playlist["code"]
    #状态码
    if code == 200: #OK
        playlist_name = playlist["result"]["name"]
        songs = playlist["result"]["tracks"]
        songs_count = len(songs)
        #赋值歌单数据

        print(f"{ playlist_name }\n{ len(songs) } Songs")

        playlist_name = re.sub(r'[\\/:*?"<>|]', "", playlist_name)
        if not os.path.exists(f"{ path }/{ playlist_name }"):
            os.makedirs(f"{ path }/{ playlist_name }")
        #文件夹是否存在

        for song in songs:
            song_name = song["name"]
            song_index = songs.index(song) + 1
            #赋值歌曲数据

            print(f"{ song_index }/{ songs_count } { song_name } ...")

            song_name = re.sub(r'[\\/:*?"<>|]', "", song_name)
            download(song["id"], f"{ path }/{ playlist_name }/", song_name)
            #处理名称下载歌曲
        print("Over")
        return 0

    elif code == 404: #未找到
        print("Not Found")
        return 404

    elif code == -447: #服务器繁忙
        print("Busy")
        return 447

    elif code == -462: #请输入Cookie
        print("Restart And Enter Cookie")
        return 462

    else: #未知
        print("Error")
        return 1

if __name__ == "__main__":
    try:
        mode = input("album / playlist\n")
        #模式选择

        if mode == "album": #专辑
            enter_id = int(input("ID\n"))
            enter_path = input("Path ( Default : ./album/ )\n") or "./album/"
            enter_cookie = input("Cookie ( Default : None )\n")
            download_album(enter_id, enter_path, enter_cookie)

        elif mode == "playlist": #歌单
            enter_id = int(input("ID\n"))
            enter_path = input("Path ( Default : ./playlist/ )\n") or "./playlist/"
            enter_cookie = input("Cookie ( Default : None )\n")
            download_playlist(enter_id, enter_path, enter_cookie)

    except ValueError: #输入类型错误
        print("Input Wrong")
