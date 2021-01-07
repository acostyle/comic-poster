# Comic poster
This project allows you to upload comics from `xkcd.com` to the wall of your VK group.

## How to install
Python3 should be already installed. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
`pip install -r requirements.txt`

## How to use
Create `.env` with `access_token` and `group_id`

Get your application ID. You need to create an application on [VK Dev](https://vk.com/dev). Then replace `client_id` with your ID here:
```
https://oauth.vk.com/authorize?client_id=&scope=stories,photos,docs,manage,wall&response_type=token&v=5.
```
Allow the application to access the page, copy the `access_token` from the address bar and paste it into the `ACCESS_TOKEN` variable. In the `GROUP_ID` variable write the ID of your group.

Example of `.env`:
```
ACCESS_TOKEN=your_access_token
GROUP_ID=your_group_id
```
## How to run
`python main.py`
