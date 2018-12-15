import requests
import random
import fileinput
import subprocess
import json


def line_prepender(filename, line):
    # Copied from StackOverflow ;)
    # Inserts text to first line of a file

    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(line).rstrip('\r\n') + '\n' + content)


def removeOldestPostFromCache():
    # This checks if more than 50 posts in already
    # posted cache (should be 51) and then removes last line
    with open('last_50_posted.txt', 'r') as alreadyPostedCacheFileReadMode:
        alreadyPostedCacheFileReadMode.seek(0, 0)
        lines = alreadyPostedCacheFileReadMode.readlines()
        numberOfLinesInCacheFile = len(lines)
        if numberOfLinesInCacheFile > 50:
            with open('last_50_posted.txt', 'w') as alreadyPostedCacheFileWriteMode:
                alreadyPostedCacheFileWriteMode.writelines(
                    [item for item in lines[:-1]])
                alreadyPostedCacheFileWriteMode.close()


def alreadyPosted(wallpaperID):
    # Checks if wallpaper was used in last 50 posts by comparing IDs

    with open("last_50_posted.txt", 'a+') as postCacheFile:
        # For comparing with posted IDs
        x = str(wallpaperID) + '\n'

        # Cursor is at end of file bydefault, so we need to move it top
        postCacheFile.seek(0, 0)
        alreadyPostedWallpaperIDs = postCacheFile.readlines()

        if x in alreadyPostedWallpaperIDs:
            return True
        else:
            return False


def getRandomSearchKeyword():
    randomNatureSearchKeywords = [
        'flower', 'mountains', 'nature', 'desert', 'forest', 'jungles'
    ]
    return randomNatureSearchKeywords[random.randrange(0, 5)]


def getWallpaperURLFromPexelsAPI(pexelAPIKey):
    # Uses Pexels API to get a random wallpaper
    # while also checking that the image has not been used in the last 50 posts
    # to avoid duplication

    # Send request
    jsonResponse = requests.get('https://api.pexels.com/v1/search?query='+getRandomSearchKeyword()+'&per_page=50&page=1',
                                headers={'Authorization': pexelAPIKey}).json()['photos']

    # Loop through the wallpaper elements
    pictureURL = ""
    for i in range(15):
        currentWallpaperJSON = jsonResponse[i]
        if alreadyPosted(currentWallpaperJSON['id']) == True:
            continue
        else:
            line_prepender('last_50_posted.txt',
                           currentWallpaperJSON['id'])
            pictureURL = currentWallpaperJSON['src']['large2x']
            removeOldestPostFromCache()
            break
    if pictureURL == "":
        return jsonResponse[i]['src']['large2x']
    else:
        return pictureURL


def checkIfUserCredentialsInCache():
    with open("credentials_cache.json", 'a+') as credentialCacheFile:
        # Cursor is at end of file by default in a+, so we need to move it top
        credentialCacheFile.seek(0, 0)

        if credentialCacheFile.read() != "":
            return True
        else:
            return False


def getUserCredentialsCache():
    with open('credentials_cache.json', 'r') as jsonFile:
        return json.load(jsonFile)


def promptUserForCredentials():
    # Prompt user for Insta credientials
    print('\nWe need your credentials for uploading content the photos Instagram')
    pexelAPIKey = input('Pexels Api key? ')
    username = input('Username? ')
    password = input('Password? ')
    caption = input('Caption(Optional)? ')
    uploadTime = input(
        'What time to upload to Instagram (24-Hour Format e.g 14:28)? ')
    # Create a dictionary ising the variables
    credentialDictionary = {
        "username": username, "password": password, "caption": caption, "pexel_api_key": pexelAPIKey, "upload_time": uploadTime
    }
    # Save credientials in cache
    with open('credentials_cache.json', 'w') as credientialsJSONFile:
        json.dump(credentialDictionary, credientialsJSONFile)
        return


def uploadRandomNatureWallpaper():
    # Get user credentials
    userCredentialsJSON = getUserCredentialsCache()
    username = userCredentialsJSON['username']
    password = userCredentialsJSON['password']
    caption = userCredentialsJSON['caption']
    pexelAPIKey = userCredentialsJSON['pexel_api_key']

    # Prepare command
    url = getWallpaperURLFromPexelsAPI(pexelAPIKey)
    cmd = "instapy -u " + username + " -p " + password + \
        " -f " + url + " -t \'" + caption + "\'"

    # print('\n'+cmd+'\n')

    # Execute command for uploading to Instagram
    subprocess.call(cmd, shell=True)

    return
