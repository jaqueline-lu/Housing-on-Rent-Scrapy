import multiprocessing as mp 
import time
from urllib.request import urlopen,urljoin
from bs4 import BeautifulSoup
import re

base_url = "https://morvanzhou.github.io/"
def crawl(url):
    try:
        response = urlopen(url)
        #time.sleep(5.1)
        r= response.read().decode('utf-8')
        #print(url)
    except: return 0

    return r

def parse(html):
    soup = BeautifulSoup(html,'lxml')
    urls = soup.find_all('a',{'href':re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url,url['href']) for url in urls])
    url = soup.find('meta',{'property':"og:url"})['content']
    return title,page_urls,url

unvisited = set([base_url,])
visited = set()

if base_url != "https://morvanzhou.github.io/":
    restricted_crawl = True
else:
    restricted_crawl = False

#count,t1 =1,time.time()
pool = mp.Pool(4)
while len(unvisited)!=0:
    if restricted_crawl and len(visited) >20:
        break
    print("Distributed Crawling...")
    crawl_jobs = [pool.apply_async(crawl,args=(url,)) for url in unvisited]
    #htmls = [crawl(url) for url in unvisited]
    htmls = [j.get() for j in crawl_jobs]
    print("parsing...")
    #results = [parse(html) for html in htmls]
    parse_jobs = [pool.apply_async(parse,args=(html,))for html in htmls]
    results = [j.get() for j in parse_jobs]
    print("analysing...")
    visited.update(unvisited)
    unvisited.clear()

    for title,page_urls,url in results:
        print(count,title,url)
        count+=1
        unvisited.update(page_urls - visited)
print('Total time %.1f s' % (time.time()-t1, ))
