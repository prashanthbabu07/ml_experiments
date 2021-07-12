# %%
from urllib import request
from bs4 import BeautifulSoup
import re
import os
import urllib

# %%

# connect to website and get list of all pdfs
url = "http://cs229.stanford.edu/syllabus.html"
response = request.urlopen(url).read()
soup = BeautifulSoup(response, "html.parser")
links = soup.find_all('a', href=re.compile(r'(.pdf)'))

# %%


# clean the pdf link names
url_list = []
for el in links:
    if el['href'].startswith('http'):
        url_list.append(el['href'])
    else:
        url_list.append(
            "http://cs229.stanford.edu/" + el['href'])

print(url_list)

# %%
for url in url_list:
    print(url.split("/")[-1])


# %%


# download the pdfs to a specified location
for url in url_list:
    try:
        print(url)
        filename = url.split("/")[-1]
        fullfilename = os.path.join(
            '/Volumes/Sandisk/Documents/Programming/ml-analytics/Stanform Andrew Ng/', filename)
        print(fullfilename)
        request.urlretrieve(url, fullfilename)
    except:
        pass

# %%
