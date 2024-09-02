# Self-Updating-Youtube-Video
A script that updates the title of a youtube video and the thumbnail with the number of views the video has.

This script has been modified to only fetch the number of views the video has and create a thumbnail with the views it has fetched. 
The script is a flask API that exposes endpoints a make.com scenerio to do the updating. 

Youtube Video: https://youtu.be/G9uatzCRh8U

## Table of Contents
1. Files and Folders
2. Logic
3. Setting Up

## Files and Folders
1. app.py contains the code and logic that runs the entire application. It houses the endpoints, code for fetching the number of views and code for generating the thumbnail.
2. config.py contains the config for the app pulled from enviornment variables in a .env file.
3. tests/unit_tests.py are unit tests for the code.
4. thumbnail_template.png is the template photo that the generated thumbnail is built from. 
5. requirements.txt contains a list of requirements needed for the application to run.
6. videodescription.txt contains the video description. It is updated along with the title and thumbnail.

## Logic
The application runs as a web server (flask app). It exposes a few endpoints explained below

/up - An endpoint to test if the service is up and running
/no_of_views - Returns the number of views from the youtube API and generates a new thumbnail with the latest number of views
/currentimage - Returns the current image with the most up to date thumbnail. Should ideally be called after /no_of_views

The `/no_of_views` endpoint will be called 2 times a day from a make scenario. This call will query the youtube api for the number of views the video has, generate a new thumbnail with the new number and return the number of views the video has.
The `/currentimage` will be called immediately after and will return the new generated image. Make.com will then handle all the updating. 

## Setting Up.

To Setup, you will need a google console account to get the API Key.

1. Create a .env file and add your API_KEY from the google console.  Also add the Youtube video ID you want this to work for! For more information, see : https://developers.google.com/youtube/v3/getting-started

`API_KEY = ""`
`YOUTUBE_VIDEO_ID = ""`

2. Update `YOUTUBE_VIDEO_ID` with the video you want to update

## Deployment

The service is deployed to fly.io as a flask app. See https://fly.io/docs/python/frameworks/flask/ for more.

Happy Coding!