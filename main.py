import requests
from tqdm import tqdm
import datetime
import json

def run(save):
    userid = input('input user id: ')
    with open('p.ini', 'r') as file_object:
        vk_token = file_object.read().strip()
    photos = {}
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': userid,
        'album_id': 'profile',
        'access_token': vk_token,
        'v': '5.131',
        'extended': '1'}
    res = requests.get(URL, params=params)

    i = int(input('How many photos do you want to download? '))

    json_ = []
    for item in tqdm(res.json()['response']['items'][:i]):
        max_size = {'type': 'a'}
        for size in item['sizes']:
            if size['type'] > max_size['type']:
                max_size = size

        name = item['likes']['count']
        if name in photos:
            name += '_' + item['date']
        photos[name] = max_size['type']
        json_.append({'file_name': name, 'type': max_size['type']})
        rec_photo = requests.get(max_size['url'], stream=True)
        save(rec_photo.raw.read(), name)

    with open(f"{datetime.datetime.now()}.json", "w") as a:
        json.dump(json_, a, indent='\t')


def photo_to_pc(photo, name):
    with open(f"{name}.jpg", "wb") as f:
        f.write(photo)


class Photo_to_ya:

    def __init__(self):
        with open('ya.ini', 'r') as file_object:
            token = file_object.read().strip()

        self.headers = {
           'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(token)
        }

        self.folder = input('Input folder name: ')

        self.create_folder()


    def create_folder(self):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": f'/{self.folder}'}
        response = requests.put(url, params=params, headers=self.headers)
        return



    def get_upload_link(self, name):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": f'/{self.folder}/{name}.jpg', "overwrite": "true"}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()['href']


    def __call__(self, photo, name):
        url = self.get_upload_link(name)
        response = requests.put(url, data=photo)

where_to_save = input('1 to pc, 2 to yandex: ')

if where_to_save == '1':
    run(photo_to_pc)
elif where_to_save == '2':
    run(Photo_to_ya())
else: print('Invalid input')




