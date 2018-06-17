# URL-CHECKER
This little script help you discover what is behind a specific url (shortened or simply weird...)

## Install
```bash
git clone https://github.com/x42en/url_checker.git
cd url_checker/
python setup.py install
```

## Usage
Simply put the url to follow as unique argument
```bash
./url_check.py http://my_url.io
```

## Options
Once the crawler has made his part, you are allowed to download a specific page.
Note: Be careful printing this page in a browser can be dangerous or have side-effects!

# TODO
- Allow download in a file
- Unit Tests
- Display only JS libs for pentesting