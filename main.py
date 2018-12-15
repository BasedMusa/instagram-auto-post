from engine import uploadRandomNatureWallpaper, checkIfUserCredentialsInCache, promptUserForCredentials, getUserCredentialsCache
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

# Prompt user for credentials if not stored
# This also caches the credentials
if checkIfUserCredentialsInCache() == False:
    promptUserForCredentials()

uploadTime = getUserCredentialsCache()['upload_time']
hour = uploadTime.split(":")[0]
minute = uploadTime.split(":")[1]
print('Starting Script For Uploading To Instagram....' + uploadTime)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(uploadRandomNatureWallpaper,
                      'cron', hour=hour, minute=minute)
    scheduler.start()
    print('Press Ctrl+C to exit')

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
