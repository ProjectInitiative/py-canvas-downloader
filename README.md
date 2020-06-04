# Canvas Course Downloader

## Purpose

To download as much course data as possible before losing access to my university's Canvas site.

## Requirements

  - [Python 3.8](https://www.python.org/downloads/)
  - pip
  - pipenv: can be installed with `pip install pipenv`
  - A Canvas personal access token: new access tokens can be generated under account > settings > scroll to bottom > + New Access Token

## Setup

1. To use this script you will need to create a **.env** file in the root directory of the repository that has the following information:

```bash
ACCESS_TOKEN=<very-long-access-token>
CANVAS_LMS_SERVER=<base-url-of-your-canvas-site>
```

> NOTE: In my case, the University of Texas `CANVAS_LMS_SERVER` URL would be formatted as follows: `https://utexas.instructure.com`

2. Install all of the required Python dependencies by running the following commands:

```bash
cd <ROOT-DIRECTORY-OF-REPOSITORY>
pipenv install
```

## Usage

To run the program, run the following:

```bash
cd <ROOT-DIRECTORY-OF-REPOSITORY>
pipenv shell
python ./get-courses.py
```

## Additional Information

> NOTE: **I HAVE YET TO IMPLEMENT PROPER API RATE LIMITING! RUN AT YOUR OWN RISK!**
> Since the program does not make any parallel API calls, I have not experienced any API quota locks, **BUT** there is still a risk that you lock yourself out of your account and will need to contact IT!

This script is a quick and dirty implementation focusing on trying to get as much data as possible before losing access to the university Canvas site. Program has been tested on Windows 10 and Ubuntu 20.04.

Currently functionality:
  - Downloads all files uploaded by professors and TAs 
  - Retains original file structure and names

Future functionality (not guaranteed):
  - Download all modules files and content
  - Retains module structure
  - Download quiz content (HTML)
  - API rate limiting

If the program crashes or you stop it prematurely, the program should pick back up where it left off. 

## Special Thanks

Andrew Gu