from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

base_url="https://en.wikipedia.org"
his = ["/wiki/Scrapy"]

for i in range(20):
    try:
        url = base_url + his[-1]
        html = urlopen(url).read()
    except OSError:
        url = his[-1]
        print("different languages possibly: ")
        html = urlopen(url).read()
    except ValueError:
        break
    except urllib.error.HTTPError:
        print(" cannot urlopen,quit")
        url = base_url + his[-2]
        html = urlopen(url).read()

    soup = BeautifulSoup(html,features='lxml')
    print(i+1,soup.find('h1').get_text(),'  url:',his[-1])

    # find the compatible /item/ website
    sub_urls = soup.find_all("a",{"title":re.compile("[A-Za-z0-9-_]"),"href":re.compile("/wiki/[A-Za-z0-9-_]*$")})

    if len(sub_urls)!=0:
        his.append(random.sample(sub_urls,1)[0]['href'])
    else:
        his.pop()
        
# Thanks to: https://morvanzhou.github.io/tutorials/
