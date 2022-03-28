
# YandeDownloader-An_OOP_Reconstruct
unified downloader of yande, konachan, minitokyo, based on selenium

Currently things to work on:
1. add a selenium core for id retrieval (12/11/2021, done);
2. unify the date (year and month-date), id list to a single json-style file (3/21/2022, done, constants are stored in `config.json`)
3. add hash check (hmmm...js script handles this, so no need anymore)
4. store file info to a database (3/27/2022, file info to json done)

## Init Python Virtual Environment
Check [here](https://code.visualstudio.com/docs/python/python-tutorial), A code editor is not necessary though. Python version should be 3.6 or higher.
Open `cmd` or other shell in the project directory, run
```
python -m venv .venv
```
then (for windowns).
```
.venv\scripts\activate
```
run
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
before the second command if activation raises error (This probably won't happen if command is executed in vs code's terminal).
## Dependency
```
python -m pip install requests pyautogui termcolor tqdm colorama lxml selenium
```
## Usage
```
python main.py
```
- ### Notes: 
- 1. `requests` is not needed if use only selenium,  (since yande.re has a strict anti-crawler policy, selenium would be one of the  few choices if don't use ip Pool),  you can safely comment out`download, multi_dates, remove_deleted` under `class Download`in `crawler.py` since using them will soon get blocked by the website;
 - 2. Download now is mainly handled by javascript [here](https://github.com/Kazy-jew/VMonkeyScript/blob/main/yandePost.js), you need to install  [Vilolentmonkey](https://chrome.google.com/webstore/detail/violentmonkey/jinjaccalgkegednnccohejagnlnfdag?hl=en) and drag the js script into it. Set "javascript" to false in `config.json` to avoid using javascript (the entrance is not added now though), but this is not recommended  since control a browser' s download process with pure python is clumsy and the relevant code may no longer get tested; 
 - 3. Selenium use Default chrome profile in that can use chrome extension directly. In case to change to a different profile, replace the two lines
         > `root = os.path.expanduser('~')  `
         > `chrome_data = r'AppData\Local\Google\Chrome\User Data'`
         
       in  `sln_chrome` under `Downloader` in `crawler.py`.
You can check your Profile  Path by entering `chrome://version` in  address bar.

