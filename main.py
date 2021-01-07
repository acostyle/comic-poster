import os
import requests

from dotenv import load_dotenv
from random import randint



def get_comic_information(comic_id):
    url = f'https://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def download_comic(url, comic_id):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    filename = f'comic{comic_id}.jpg'
    with open(filename, 'wb') as file:
        return file.write(response.content)


def get_user_groups(vk_token):
    url = 'https://api.vk.com/method/groups.get'
    payload={
        'extended': '1',
        'access_token': vk_token,
        'v': '5.126'
    }

    response = requests.get(url, params=payload, verify=False)
    response.raise_for_status()

    return response.json()


def get_upload_url(vk_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': group_id,
        'access_token': vk_token,
        'v': '5.126'
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()['response']['upload_url']


def upload_picture_on_server(vk_token, group_id, comic_id, upload_url):
    with open(f"comic{comic_id}.jpg", 'rb') as file:
        files = {
            'photo': file,
        }

        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    
    server = response.json()['server']
    photo = response.json()['photo']
    upload_hash = response.json()['hash']

    return server, photo, upload_hash


def save_wall_picture(group_id, vk_token, comic_id, upload_url):
    server, photo, upload_hash = upload_picture_on_server(vk_token, group_id, comic_id, upload_url)

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'server': server,
        'photo': photo,
        'hash': upload_hash,
        'group_id': group_id,
        'access_token': vk_token,
        'v': '5.126'
    }

    response = requests.post(url, params=payload)

    return response.json()


def post_wall(picture_id, owner_id, comic_name, vk_token, group_id):
    url = 'https://api.vk.com/method/wall.post'
    payload={
        "attachments": f"photo{owner_id}_{picture_id}",
        'owner_id': f'-{group_id}',
        "message": comic_name,
        "access_token": vk_token,
        'v': '5.122'
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()

    return response.json()


def main():
    load_dotenv()

    vk_token = os.getenv('ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')

    try:
        last_comic_id = get_comic_information('')['num']
        random_comic_id = randint(1, last_comic_id)

        comic_info = get_comic_information(random_comic_id)
        comic_name = comic_info['safe_title']
        comic_url = comic_info['img']

        download_comic(comic_url, random_comic_id)

        upload_url = get_upload_url(vk_token, group_id)
        
        decoded_json = save_wall_picture(group_id, vk_token, random_comic_id, upload_url)
        picture_id = decoded_json['response'][0]['id']
        owner_id = decoded_json['response'][0]['owner_id']

        post_wall(picture_id, owner_id, comic_name, vk_token, group_id)
    except requests.exceptions.HTTPError:
        print('HTTP Error')
    finally:
        if os.path.exists(f'comic{random_comic_id}.jpg'):
            path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), f'comic{random_comic_id}.jpg')
            os.remove(path)




if __name__=='__main__':
    main()
