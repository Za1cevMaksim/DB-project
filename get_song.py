import requests
from bs4 import BeautifulSoup
import json
import os
import db_insert
import other_func


def take_music(song_name):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                      "YaBrowser/22.11.3.838 Yowser/2.5 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9"
    }

    url = 'https://rur.hitmotop.com/'
    song_url=url+'search?q='+song_name

    rs=requests.get(song_url,headers=headers)
    soup = BeautifulSoup(rs.text, "lxml")
    result=soup.find_all("li", "tracks__item track mustoggler")
    ans=[]
    for i in range(0,len(result)):
        ans.append(json.loads(result[i].get('data-musmeta')))
    return ans


def download_song(url, save_path):
    try:
        # Отправляем GET-запрос по URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Проверяем, успешен ли запрос

        # Открываем файл для записи в бинарном режиме
        with open(save_path, 'wb') as file:
            # Итерируемся по блокам данных и записываем их в файл
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")

user='users'
password='123456'


with open('db_create.sql', 'r') as f:
    setup_sql = f.read()
def fin(setup_sql,user,password,song_name,author):
    #res=take_music(song_name)
    res=other_func.download_song(setup_sql,user,password,song_name,author)
    directory="DownloadedMusic"
    files=[]
    files+=os.listdir(directory)
    #print(files)
    if(res[0][0]+"-"+res[0][1]+'.mp3' not in files):
        download_song(res[0][2],'DownloadedMusic\\' + res[0][0]+"-"+res[0][1]+'.mp3')
    return 'DownloadedMusic\\' + res[0][0]+"-"+res[0][1]+'.mp3'
    #print(res)
def fin2(author):
    res=take_music(author)
    author_id=other_func.find_author_id(setup_sql,user,password,author)
    print(author_id)
    print(res)
    for i in range(0,len(res)):
        #download_song(res[i]['url'],'D:\download\\' + res[i]['title']+'.mp3')
        db_insert.insert_songs(setup_sql,user,password,res[i]['title'],author_id[0],res[i]['url'])


#fin2("eminem")


#fin(setup_sql,user,password,"Владимерский централ","eminem")