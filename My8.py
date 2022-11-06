#1
import requests 
import os
#from datetime import datetime


base_url = 'https://akabab.github.io/superhero-api/api'
heroes = {'name' : ['Hulk', 'Captain America', 'Thanos']}

def take_all_id(url, heads):
    resp = requests.get(f'{url}/all.json')
    answer_id = {}
    if resp.status_code == 200:
        for name in resp.json():
            if name['name'] in heads['name']:
                answer_id[name['name']] = name['id']
    else:
        print(f'error {resp.status_code}')
    return answer_id
  
def take_stats(url, heroes, stats = "intelligence"):
    heroes_id = take_all_id(url, heroes)
    heroes_intelligence = []
    for hero in heroes_id:
        resp = requests.get(f'{url}/powerstats/{heroes_id[hero]}.json')
        if resp.status_code == 200:
            heroes_intelligence.append(resp.json()[stats])
        else:
            return print(f'error {resp.status_code}') 
    heroes_stats = dict(zip(heroes_intelligence, heroes_id.keys()))
    heroes_intelligence.sort(reverse = True)
    return [heroes_stats.get(int) for int in heroes_intelligence]

print(f'Самый умник: {str(take_stats(base_url, heroes)[0])}')

#2

class YaUploader:
  
    def __init__(self, token: str):
        self.token = token
        self.header = {"content-type": "application/json", 'Authorization': f'OAuth {token}'}

    def is_load(self, file_path: str, file_list):
        '''Проверяем размеры файлов и место на диске'''      
        size = 0
        resp = requests.get('https://cloud-api.yandex.net/v1/disk', headers = self.header)   
        for file in file_list:
            size += os.path.getsize(f'{file_path}{file}')
        return int(size) < int(resp.json()["total_space"])

    def make_folder(self, file_list, path_folder = 'New'):
        '''Будем сохранять в папку "New" но можем и создать, так же проверяем файлы'''     
        resp = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers = self.header, params ={'path' : f'/{path_folder}'})
        if resp.status_code == 409:
            print(f'Папка {path_folder} уже существует')
            new_list = []
            for file in file_list:
                resp = requests.get('https://cloud-api.yandex.net/v1/disk/resources', headers = self.header, params ={'path' : f'/{path_folder}/{file}'})
                if resp.status_code == 200:
                    print(f'Файл {file} уже существует, удаляем из списка загрузки')
                else:
                    new_list.append(file)
            return new_list
        else:
            print(f'Папка {path_folder} создана')  
        return file_list
  
    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        folder = 'SomeNew'
        file_list = ['file1.txt', 'file2.txt', 'file3.txt']
#        self.make_folder(file_list, folder)
        file_list = self.make_folder(file_list, folder)
        if self.is_load(file_list, file_path) and file_list != []:
            for file in file_list:
                response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers = self.header, params ={'path' : f'/{folder}/{file}'})
                upload_way = response.json().get('href')
                with open(f'{file_path}{file}', 'rb') as f:
                    print(f'Отправляем {file_path}{file}')
                    resp = requests.put(upload_way, files = {'file': f}, headers = self.header)
                    if resp.status_code == 201:
                        print('Сделано')
                    else:
                        print(f'error {resp.status_code}')
        else:
            if file_list == []:
                print('Нечего загружать')

if __name__ == '__main__':
 
    path_to_file = ''
    token = 'Тут могла быть ваша реклама'
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)