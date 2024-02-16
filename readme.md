## Linkedin Scrapper using Selenium
This repository contains a LinkedIn scraper built with Selenium, allowing users to extract information from LinkedIn profiles and posts. The scraper utilizes cookies for login to handle bot detection effectively.

### How to use

#### Clone the repo

```bash
git clone https://github.com/Adiii1436/scrapper_linkedin.git
```

#### Using cookies
- We are using cookies to login to handle bot detection.
- Open the browser and login to your linkedin account.
- Now copy your cookies from: **inspect->application->cookies** into the excel sheet.
- You only need three columns: name,value and domain
- It will look something like this<br>
![cookies](https://github.com/Adiii1436/scrapper_linkedin/assets/73269919/9ebb8378-c290-4c25-aeda-f8508bad0669)
- Now place the cookies.csv file into the same folder.

#### Search for posts
- Open main.py
- Replace **search_term** with anything you want to search.
  ```python
  search_term = "google"
  ```
- Now all the results will be stored in **search_results.json** file.
- All the items are symantically classified according to searched term.