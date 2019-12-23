import os
import slack
from dotenv import load_dotenv
from imgurpython import ImgurClient

load_dotenv()

slack_token = os.environ['SLACK_API_TOKEN']
slack_client = slack.WebClient(
    token = slack_token
)

img_client_id = os.environ['IMGUR_CLIENT_ID']
img_client_secret = os.environ['IMGUR_CLIENT_SECRET']

img_client = ImgurClient(img_client_id, img_client_secret)


def upload_image_to_imgur(img_path: str):
    res = img_client.upload_from_path(img_path, config=None, anon=True)
    return res.get('link', 'https://docs.microsoft.com/en-us/windows/win32/uxguide/images/mess-error-image4.png')


def send_picture_to_space(img_path: str, confidence: str, label: str):
    link = upload_image_to_imgur(img_path)
    attachments = [{"title": label, "image_url": link}]
    response = slack_client.chat_postMessage(
        channel='#watchingbirds',
        text=f"Look at this {label} I found! I'm {int(confidence * 100)}% confident it's a {label}.",
        username='BirdWatcherBot',
        attachments=attachments
    )
    assert response["ok"]
    print(response)
