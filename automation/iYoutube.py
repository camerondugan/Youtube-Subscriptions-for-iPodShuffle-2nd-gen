import os, scrapetube
from yt_dlp import YoutubeDL

ipodName = 'IPOD'
ipodLocation = os.path.join("/run/media",os.getlogin(),ipodName) #Change on windows/mac system
# If it doesn't work then open the ipod folder itself in terminal and uncomment the line below and try again
#ipodLocation = '.'
videoDownloadlocation = os.path.join(ipodLocation,'Videos')

channelNames = ['Joe Rogan Experience','exampleChannelName2'] #remove example to work. Joe Rogan's channel is a working example.
channelIDs =  ['UCzQUP1qoWDoEbmsQxvdjxgQ','gibberish'] #not full url, just the id
videoLists = []
for channelID in channelIDs:
    videoLists.append(scrapetube.get_channel(channelID))
downloadQueue = []
seen = []

def clearStorage():
    os.chdir(os.path.join(ipodLocation,'Videos'))
    os.system("rm -rf *") #deletes everything downloaded
    os.chdir(os.path.join(ipodLocation,'.Trash-1000'))
    os.system("rm -rf *") #deletes everything in trash
    os.chdir(ipodLocation) #move back to ipod folder

def storageAvailable():
    disk = os.statvfs(ipodLocation)
    totalGBytes = float(disk.f_bsize*disk.f_bfree)/1024/1024/1024
    print("Your iPod has: %.2f GB left"% totalGBytes)
    return totalGBytes 

def loadSeen():
    open('automation/seen.txt','a').close() #create blank file if not there
    seenFile = open('automation/seen.txt')
    for line in seenFile:
        seen.append(line.split('\n')[0])
    seenFile.close()

#Queues one video per channel into downloadQueue
def queueDownloads():
    for i,v in enumerate(videoLists):
        for a in v:
            vidID = str(a['videoId'])
            if (seen.__contains__(vidID)):
                continue
            print(channelNames[i],'-',a['title']['runs'][0]['text'])
            downloadQueue.append(vidID)
            break

#Dowloads everything from download queue and marks down successfull downloads into seen.txt
def download():
    print()
    os.system("mkdir {}".format(videoDownloadlocation))
    os.chdir(videoDownloadlocation)
    ydl_opts = {
        'format': 'mp3/wav/bestaudio/best',
        'maxBuffer': 'Infinity',
        ''
        'postprocessors': [
        {
            'key': 'SponsorBlock', 
        },
        {
            'key': 'ModifyChapters', 
            'remove_sponsor_segments': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview', 'filler', 'interaction']
        },{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    for vid in downloadQueue:
        vidID = vid
        vid = "https://www.youtube.com/watch?v="+vid
        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([vid])
            except:
                print("Couldn't download: " + vid)
        seen.append(vid)
        seenFile = open(os.path.join(ipodLocation,"automation/seen.txt"),'a')
        seenFile.write(vidID+'\n')
        seenFile.close()
        storageAvailable()
    downloadQueue.clear()
    os.system("find {} -type f ! -name '*.mp3' -delete".format(videoDownloadlocation))# deletes all non-audio files
    os.chdir(ipodLocation)

def main():
    if (storageAvailable()<0.4): #Reset if full
        clearStorage()
    loadSeen()
    while storageAvailable()>0.4:
        queueDownloads()
        download()
    os.chdir(ipodLocation)
    os.system("python2 rebuild_db.py")

if __name__ == '__main__':
    main()
