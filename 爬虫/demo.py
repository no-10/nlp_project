import time
import re
import requests
from bs4 import BeautifulSoup

web1 = "https://global-factiva-com.libproxy1.nus.edu.sg/"
web2 = "https://global-factiva-com.libproxy1.nus.edu.sg/factivalogin/login.asp?productname=global"
web3 = "https://global-factiva-com.libproxy1.nus.edu.sg/sb/default.aspx?fcpil=zhcn&lnep=hp"

r = requests.get(web3)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.title)
