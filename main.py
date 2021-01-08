import os
import requests

from dotenv import load_dotenv
from random import randint


def get_comic_information(comic_id):
    url = f'https://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def check_error(decoded_response):
    if 'error' in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response['error'])


def download_comic(url, comic_id):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    filename = f'comic{comic_id}.jpg'
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_upload_url(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': '5.126'
    }

    response = requests.get(url, params=payload)
    decoded_response = response.json()
    check_error(decoded_response)

    return decoded_response['response']['upload_url']


def upload_picture_on_server(vk_access_token, vk_group_id, comic_id, upload_url):
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


def save_wall_picture(vk_group_id, vk_access_token, comic_id, upload_url):
    server, photo, upload_hash = upload_picture_on_server(vk_access_token, vk_group_id, comic_id, upload_url)

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'server': server,
        'photo': photo,
        'hash': upload_hash,
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': '5.126'
    }

    response = requests.post(url, params=payload)
    decoded_response = response.json()
    check_error(decoded_response)

    return decoded_response


def post_wall(picture_id, owner_id, comic_name, vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/wall.post'
    payload={
        "attachments": f"photo{owner_id}_{picture_id}",
        'owner_id': f'-{vk_group_id}',
        "message": comic_name,
        "access_token": vk_access_token,
        'v': '5.122'
    }
    response = requests.post(url, params=payload)
    decoded_response = response.json()
    check_error(decoded_response)

    return decoded_response


def delete_picture(random_comic_id):
    if os.path.exists(f'comic{random_comic_id}.jpg'):
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), f'comic{random_comic_id}.jpg')
        os.remove(path)


def main():
    load_dotenv()

    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')

    try:
        last_comic_id = get_comic_information('')['num']
        random_comic_id = randint(1, last_comic_id)

        comic_info = get_comic_information(random_comic_id)
        comic_name = comic_info['safe_title']
        comic_url = comic_info['img']

        download_comic(comic_url, random_comic_id)

        upload_url = get_upload_url(vk_access_token, vk_group_id)
        wall_picture = save_wall_picture(vk_group_id, vk_access_token, random_comic_id, upload_url)
        picture_id = wall_picture['response'][0]['id']
        owner_id = wall_picture['response'][0]['owner_id']

        post_wall(picture_id, owner_id, comic_name, vk_access_token, vk_group_id)
        delete_picture(random_comic_id)
    except requests.exceptions.HTTPError:
        print('HTTP Error')        


if __name__=='__main__':
    main()