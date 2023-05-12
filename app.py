# Author - Uma Abu
# Description - This file contains the main application code for the Flask app

import flask
from flask import send_file
import requests
from googleapiclient.http import MediaFileUpload
import urllib.parse as p
import config
import os, pickle
from PIL import Image, ImageFont, ImageDraw 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apscheduler.schedulers.background import BackgroundScheduler

app = flask.Flask(__name__)
app.config.from_object(config.Config)

CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
YOUTUBE_VIDEO_ID = "fLlQ2w1gOEM"
GENERATED_THUMBNAIL_FILE_NAME = "generated_thumbnail.png"

@app.route('/up')
def hello():
    return "Hello World! Service is Up and Running!"

@app.route('/currentimage')
def sendCurrentImage():
    return send_file(GENERATED_THUMBNAIL_FILE_NAME, mimetype='image/gif')

@app.route('/authenticate')
def authenticate():
    youtube = youtube_authenticate()
    return "Authenticated"

@app.route('/adhoc')
def run_update_method():
    update_view_count_and_thumbnail()
    return "Updated"

# Gets the video view count from youtube
def get_video_view_count():
    print('Getting number of views')
    video_URL = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={YOUTUBE_VIDEO_ID}&key={app.config['API_KEY']}"
    response = requests.get(video_URL)
    json_response = response.json()
    youtube_video_view_count = json_response['items'][0]['statistics']['viewCount']
    print("Number of views: ", youtube_video_view_count)
    return youtube_video_view_count

#Generates a new thumbnail with the updated view count
def generate_new_thumbnail(no_of_views):
    print('Generating new thumbnail')
    view_count = no_of_views
    formated_view_count = format(int(view_count), ',d')
    views_count_string = str(formated_view_count) # Text to be written
    thumbnail_template = Image.open("thumbnail_template.png") # Open the template
    image_width, image_height = thumbnail_template.size # Get the size of the template
    title_font = ImageFont.truetype('font/peace-sans.regular.ttf', 180) # Load the font
    image_editable = ImageDraw.Draw(thumbnail_template) # Make the image editable
    _, _, textbox_width, textbox_height = image_editable.textbbox((0, 0), views_count_string, font=title_font)
    image_editable.text(((image_width-textbox_width)/2, 75), views_count_string, (255, 255, 255), font=title_font)# Draw the text
    thumbnail_template.save(GENERATED_THUMBNAIL_FILE_NAME) # Save the image
    print('Thumbnail generated successfully')

# Get Video Description from a text file
def get_video_description():
  with open('videodescription.txt', 'r') as f:
    videodescription = f.read()
    f.close()
  return videodescription

def update_view_count_and_thumbnail():
  print("==================================")
  view_count = get_video_view_count()
  generate_new_thumbnail(view_count)
  print("Updating Video Title and Thumbnail")
  youtube = youtube_authenticate()
  print(f"This Video Has {view_count} views",)
  
  title_update_request = youtube.videos().update(
      part="snippet",
      body={
        "id": YOUTUBE_VIDEO_ID,
        "snippet": {
          "categoryId": "27",
          "title": f"This Video Has {view_count} views",
          "description": get_video_description(),
        }
      })
  
  # title_update_response = title_update_request.execute()

  # thumbnail_update_request = youtube.thumbnails().set(
  #   videoId=YOUTUBE_VIDEO_ID,
  #   media_body=MediaFileUpload(GENERATED_THUMBNAIL_FILE_NAME)
  # )
    
  # thumbnail_update_response = thumbnail_update_request.execute()

 
  # Save credentials back to session in case access token was refreshed.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  # flask.session['credentials'] = credentials_to_dict(credentials)
  update_responses = {}
  update_responses['title_update_response'] = 'title_update_response'
  # update_responses['thumbnail_update_response'] = thumbnail_update_response
  print("Successfully Updated Video Title and Thumbnail")
  print("==================================")

  return update_responses


def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # raise Exception("Renew Credentials")
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)



scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(update_view_count_and_thumbnail,'interval',minutes=30)
# scheduler.add_job(update_view_count_and_thumbnail,'interval',seconds=10)
scheduler.start()

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  app.run('localhost', 8080, debug=True, ssl_context='adhoc')
  # app.run(ssl_context='adhoc')
