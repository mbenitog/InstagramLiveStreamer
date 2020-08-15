# InstagramLiveStreamer
This script will get the stream keys from Instagram and auto-update them in Restream each hour to bypass the 1 hour IG limit.

Ther idea behind this is that Restream allows to change the keys without restarting your stream in OBS and having to change the key manually. This means that, once an hour has passed, the script will generate a new Instagram stream key and update it in Restream's page automatically so you can continue your stream with minimal downtime.

It makes use of Chrome Selenium and Restream.io for the automatic key updates. You could easily modify the script to bypass this module and just get the keys in text format for manual updates or maybe other use case.

## Setup
First download the correct ChromeDiver executable (according to your Chrome version) from here https://chromedriver.chromium.org/home and place it in the root folder of the project. You will need this if you want the automatic key updating.

Second, you will need to install some python dependencies which you may not have already installed. Mainly InstagramAPI. You can do so with ```pip install InstagramAPI```. Then, try running the main python file and then use the same method to install the missing dependencies.

## Important notes
When the script asks to save the credentials, it will save them in a JSON file in the root folder of the project. **YOUR USERNAME AND PASSWORD WILL BE STORED IN PLAIN TEXT**. Just take this into account and choose not to save your credentials if you don't like how they will be stored.

Your restream login will be stored in the chrome_data folder. The script will create a chrome_data dir which is separate from your own day-to-day Chrome profile. This means your Restream login will not be available in your normal Chrome instances and vice-versa. Both login.json and chrome_data are safe to delete, but you will reset the Instagram and Restream logins respectively if you do so.
