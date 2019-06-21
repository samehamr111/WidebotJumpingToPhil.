import time
import urllib

import bs4
import requests
class Crawler(object):
    
    #issue the http request to wikipedia and return the html



    start_url = "https://en.wikipedia.org/wiki/Special:Random"
    target_url = "https://en.wikipedia.org/wiki/Philosophy"

    def __find_first(url):
        response = requests.get(url)
        html = response.text
        soup = bs4.BeautifulSoup(html, "lxml")
        all_paragraphs=soup.find("div",{"id":"bodyContent"}).findAll("p")
        
        for element in all_paragraphs :
           
            if element.find("a"):
                article_link = element.find("a").get('href')
                break

        if not article_link:
            return

        first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

        return first_link

    def __continue_crawl(search_history, target_url, max_steps):
        #in case we reach the philosophy page
        if search_history[-1] == target_url:
            print("We've found the target article!")
            return False
        #in case we will be stuck in a loop
        elif search_history[-1] in search_history[:-1]:
            print("We've arrived at an article we've already seen, aborting search!")
            return False
        else:
            return True

        
    def crawlPages():  
        article_chain = [Crawler.start_url]

        while Crawler.__continue_crawl(article_chain, Crawler.target_url,25):
            print(article_chain[-1])

            first_link = Crawler.__find_first(article_chain[-1])
            if not first_link:
                print("We've arrived at an article with no links, aborting search!")
                break

            article_chain.append(first_link)

            time.sleep(0.5) # slow down otherwise wiki server will block you
