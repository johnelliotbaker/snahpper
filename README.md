# Snahpper - Snahp.it Harvester

Snahpper is an data retriever and organizer for materials on snahp.it

## Installation
The minimum installation for running snahpper

### Requirements
* Python3
* pip (python app manager)
* Beautifulsoup4 (python module)

#### 1. Git clone the repo to local drive

    git clone https://github.com/johnelliotbaker/snahpper

#### 2. Edit config.json to include valid credential

    "snahp": {
        "host": "https://forum.snahp.it",
        "credentials": {
            "username": "your_username",
            "password": "your_password"
        }
Replace your_username with a valid username.
Do the same for your_password.

#### 3. Edit jobs.json to register some jobs
    "jobs": [
            {
                "title": "TV",
                "queue": [64, 31, 32, 65, 33, 61, 62, 57],
                "days": 3,
                "enabled": 1
            },
            {
                "title": "Movie",
                "queue": [26, 56],
                "days": 3,
                "enabled": 1,
                "minYear": 1995
            }

A "Job" requires 4 fields
- title: A title to identify the job
- queue: A collection of forum id's to retrieve
- days:  Limit the number of days for data retrieval
- enabled: 1 to enable the job, 0 to disable

Optionally, following fields can adjust the data retrieval
- minYear: Will only retrieve data past this number


## Usage
Depending on the way python3 has been installed
snahpper can be launched simply by double clicking the 
Crawler.py

or issuing a command in terminal

    python3 Crawler.py

The Crawler.py will generate html files for viewing.

