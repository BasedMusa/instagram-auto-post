# instagram-auto-post
This script can automatically upload images related to nature to an Instagram page


## Requirements
You need the following:
* Instagram ID Username
* Instagram ID Password
* An API Key for [Pexels](https://www.pexels.com/) (Pexels API is used to get images for uploading to Instagram. Get an API Key for free from [here](https://www.pexels.com/api/new/))

## Usage
Run ``main.py`` from root directory using `python main.py`. The first time, it will prompt you for the credentials mentioned above and then it will store the data in a ``JSON`` file  in the same folder. Just run this every time you start your computer.

To edit these credentials, delete the JSON file and restart the script, it will prompt you again for the credentials. Or you can manually edit the JSON file.

## Disclaimer
The script does not upload to Instagram by itself, it uses version 0.0.6 of another Python library called ``instapy``. My script does not collect any informaion or share any private account info. You can manually verify that in the script as it only has a 100 lines of code.  
