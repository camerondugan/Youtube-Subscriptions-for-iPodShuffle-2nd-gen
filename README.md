# Youtube Subscriptions for iPodShuffle 2nd gen

## What this does:

1. Downloads youtube videos from your list of channels
2. Removes sponsors/ads from the videos with sponsorblock
3. Converts to mp3 and stores it on your ipod in a Videos folder
4. Rebuilds the ipod database to allow it to actually play (thank you rebuild\_db.py)

## Getting started

1. Plug in your iPod Shuffle 2nd gen
2. Remove all songs from your shuffle (if you just want to hear new youtube videos)
3. Download this repo and copy all the contents into your iPod's storage
4. Open your iPod's folder in the terminal
5. Setup Python to run the code: (only have to do once)
    1. Type 'python -m pip ensure pip'
    2. Type 'python -m pip install -r automation/requirements.txt'
6. Edit automation/iYoutube.py to have your desired youtube channels:
    1. Find the youtube channel's channel id: google it or use this: [commentpicker.com](https://commentpicker.com/youtube-channel-id.php)
    2. Open iYoutube.py in a text editor and edit: channelNames and channelIds somewhere around line 10

## Usage

Warning: Make a backup of your iPod's folders before use. This could break things, idk. You have been warned.

1. Open your iPod's folder in the terminal
2. Type 'python automation/iYoutube.py'

Note: each time you run the code, it will wipe all of the audio files it downloaded if storage available < 40%
