# Self-Updating-Youtube-Video
A script that updates the title of a youtube video and the thumbnail with the number of views the video has.

Youtube Video: 

## Table of Contents
1. Files and Folders
2. Logic
3. Setting Up

## Files and Folders
1. app.py contains the code and logic that runs the entire application. 
2. config.py contains the config for the app pulled from enviornment variables in a .env file.
2. thumbnailgenerator.py is a stand alone python script that takes generates the thumbnail from the template photo. 
3. thumbnail_template.png is the template photo that the generated thumbnail is built from. 
4. requirements.txt contains a list of requirements needed for the application to run.
6. videodescription.txt contains the video description. It is updated along with the title and thumbnail.

## Logic
The application runs as a flask app with a scheduler setup to call the update method every hour!

The number of views the video has has fetched from the Youtube API using an API Key. The code also authenticates with the youtube API and recieves authorization from the user. After that happens, a thumbnail is generated using the number of views video has using the PIL (Pillow Library). That thumbnail is then uploaded along with the title back to youtube!

When the user initially authenticates and grants permission, a .pickle with the access and referesh tokens are generated and stored and are in future calls.

## Setting Up.

To Setup, you will need a google console account to get the API Key and create a desktop application for OAuth.

1. Create a .env file and add your API_KEY from the google console.  For more information, see : https://developers.google.com/youtube/v3/getting-started

`API_KEY = ""`

2. Download the credential file gotten after creating and registering a desktop application on the google console. Make sure the credential file is called `credentials.json`.

3. Update `YOUTUBE_VIDEO_ID` with the video you want to update

3. Change the schedule delay to 10 seconds and run the flask application, you should be prompted to login after 10 seconds. After logging in, the function should run and a thumbnail should be generated. 

Happy Coding!