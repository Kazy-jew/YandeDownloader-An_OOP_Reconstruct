# YandeDownloader-An_OOP_Reconstruct
unified downloader of yande, konachan, minitokyo, based on selenium

Currently things to work on:
1. add a selenium core for id retrieval (12/11/2021, done);
2. unify the date (year and month-date), id list to a single json-style file
3. add hash check (hmmm...js script handles this, so no need anymore)
4. store file info to a database

## Dependency
```
python -m pip install requests pyautogui termcolor tqdm colorama lxml selenium
```
- ### Notes: 
- 1. `pyautogui` is windows only, yet if using the js script here, it's not needed;
- 2. `requests ` is not needed if use only selenium,  (since yande.re has a strict anti-crawler policy, selenium would be the only choice if don't use ip Pool),  you can safely comment `download, multi_dates, remove_deleted`in `crawler.Download`;

