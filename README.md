# Self-Updating-Youtube-Video
A script that updates the title of a youtube video and the thumbnail with the number of views the video has.

This script has been modified to only fetch the number of views the video has and create a thumbnail with the views it has fetched. 
The script is a flask API that exposes endpoints a make.com scenerio to do the updating. 

Youtube Video: https://youtu.be/G9uatzCRh8U

## Table of Contents
1. Files and Folders
2. Logic
3. Setting Up
4. Deployment
5. History of Major Changes

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

The service is deployed to [fly.io](https://fly.io) as a Flask app, managed via the `flyctl` CLI. See https://fly.io/docs/python/frameworks/flask/ for more.

Deploys are run with:

```bash
flyctl deploy
```

The `fly.toml` file in the project root holds the app configuration (region, ports, VM size, etc.), and the `Dockerfile` defines the runtime image used by Fly Machines.

## History of Major Changes

A running log of the meaningful decisions and refactors made to this project, newest first.

- **Switched deployment to `flyctl` / fly.io** _(latest)_ — Moved the hosting of the Flask app to fly.io, deployed via the `flyctl` CLI. A `fly.toml` and `Dockerfile` were added so the app runs on Fly Machines instead of the previous host. This is the current source of truth for how the service is deployed.
- **Scheduler tuned to hourly updates** — The update cadence was changed so the view count / thumbnail refresh runs hourly, instead of the earlier (less frequent) schedule.
- **Refactored to a thin API; updating handled by make.com** — The script was simplified to expose only the endpoints needed to (a) fetch the current YouTube view count and (b) generate a thumbnail with that view count baked into it. The actual updating of the YouTube video (title, thumbnail, description) is now orchestrated by a [make.com](https://www.make.com) scenario that calls these endpoints on a schedule.
- **Initial implementation** — A Flask app that pulled view counts from the YouTube Data API and updated the video's title and thumbnail directly. See the companion video walkthrough: https://youtu.be/G9uatzCRh8U.

Happy Coding!