# Marugo
## Instagram bot

This is a simple scrapper that login in instagram, search by hashtags, follow profiles and like posts automatically. 

## Setting up the environment:

 - Make sure you have python 3.9 or higher installed

 - Make sure you have the chromedriver installed and matching your chrome version

Create the environment
```
python3 -m venv venv
```
Activate the environment:
```
source venv/bin/activate
```
Install de dependencies:
```
pip install -r requirements.txt
```
## Defining the attributtes to run the scrapper
Create a .env file based on env.credentials, and set the search variables :
- USERNAME
- PASSWORD
- HASHTAGS (Split by comma. Ex: "#music,#mpb,#mpbbrasil)
- PERIOD (in hours)

## Start the scrapper
Run tasks.py

#### Obs:
This project is ready to deploy in Robocorp Cloud [https://cloud.robocorp.com/]