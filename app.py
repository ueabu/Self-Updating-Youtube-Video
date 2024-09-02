# Author - Uma Abu
# Description - This file contains the main application code for the Flask app

import flask
import json
from flask import send_file, Response
import requests
import config
from PIL import Image, ImageFont, ImageDraw 
import logging

app = flask.Flask(__name__)
app.config.from_object(config.Config)
logging.basicConfig(level=logging.DEBUG)

YOUTUBE_VIDEO_ID = app.config['YOUTUBE_VIDEO_ID']
GENERATED_THUMBNAIL_FILE_NAME = "generated_thumbnail.png"

@app.route('/up')
def hello():
    """An endpoint to test if the service is up and running"""

    return Response("All systems go! Up and running", status=200, mimetype='text/plain')

@app.route('/currentimage')
def sendCurrentImage():
    """Returns the current image with the most up to date thumbnail. Should ideally be called after /no_of_views"""

    return send_file(GENERATED_THUMBNAIL_FILE_NAME, mimetype='image/gif')

@app.route('/no_of_views')
def no_of_views():
    """Fetches the number of views from the youtube API and creates the thumbnail picture. Returns only the no_of_views"""

    formated_view_count = get_video_view_count()
    generate_new_thumbnail(formated_view_count)
    data = {
       'no_of_views': formated_view_count,
    }
    return Response(json.dumps(data), status=200, mimetype='application/json')

# Returns the formatted number of views
def get_video_view_count():
    """Wrapper function for querying the youtube API"""

    youtube_video_view_count = query_for_raw_number_of_views()
    formated_youtube_video_view_count = format(int(youtube_video_view_count), ',d')
    logging.info(formated_youtube_video_view_count)
    return formated_youtube_video_view_count

# Gets the raw number of views from youtube
def query_for_raw_number_of_views():
    """Queries the youtube API and returns the raw number of views"""

    views_query_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={YOUTUBE_VIDEO_ID}&key={app.config['API_KEY']}"
    response = requests.get(views_query_url)
    json_response = response.json()
    youtube_video_view_count = json_response['items'][0]['statistics']['viewCount']
    return youtube_video_view_count
   
#Generates a new thumbnail with the updated view count
def generate_new_thumbnail(formated_youtube_video_view_count):
    
    """Takes in the number of views the video has and generates a new thumbnail. New thumbnail is stored as a generated_thumbnail.png file and is overwritten anytime /no_of_views gets called. """

    logging.info('Generating new thumbnail ...')
    thumbnail_template = Image.open("thumbnail_template.png") # Open the template
    image_width, image_height = thumbnail_template.size # Get the size of the template
    title_font = ImageFont.truetype('font/peace-sans.regular.ttf', 180) # Load the font
    image_editable = ImageDraw.Draw(thumbnail_template) # Make the image editable
    _, _, textbox_width, textbox_height = image_editable.textbbox((0, 0), formated_youtube_video_view_count, font=title_font)
    image_editable.text(((image_width-textbox_width)/2, 75), formated_youtube_video_view_count, (255, 255, 255), font=title_font)# Draw the text
    thumbnail_template.save(GENERATED_THUMBNAIL_FILE_NAME) # Save the image
    logging.info('Thumbnail generated successfully!')

if __name__ == '__main__':
  app.run('localhost', 5000, debug=True, ssl_context='adhoc')
