import time

import requests
from bs4 import BeautifulSoup

#

# import requests
import urllib.request
from bs4 import BeautifulSoup
# from urllib import urlopen
import re
from urllib.request import Request, urlopen
import uvicorn

import requests
from fastapi import FastAPI

from fastapi.responses import HTMLResponse
import html
from deep_translator import GoogleTranslator
import traceback

app = FastAPI()
cache = []


@app.get("/", response_class=HTMLResponse)
def read_root():
    try:

        if len(cache) != 0:
            return cache[0]
        print("inside conversion")
        my_session = requests.session()
        for_cookies = my_session.get("https://www.classcentral.com/")
        cookies = for_cookies.cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'}
        my_url = 'https://www.classcentral.com/'

        response = requests.get(my_url, headers=headers, cookies=cookies)
        print("got the response")
        soup = BeautifulSoup(response.content, 'html.parser')
        print("parsed the response")

        text_to_translate = soup.get_text(separator=' ')

        translated_text = ''
        print(len(text_to_translate.split('\n')))

        for element in soup.find_all(text=True):
            if element.parent.name in ['script', 'style', 'iframe']:
                # ignore script, style, and iframe elements
                continue
            else:
                # translate the text content of the element
                translation = GoogleTranslator(source='en', target="hi").translate(element.strip())
                element.replace_with(translation)

        count = 0
        # for string in text_to_translate.split('\n'):
        #     # time.sleep(2)
        #     if string.strip() != '':
        #         print(count)
        #         print("the string to translate ", string)
        #         # translated_string = translator.translate(string, dest='hi').text
        #         translated_string = GoogleTranslator(source='auto', target='hi').translate(string)
        #         translated_text += translated_string + '\n'
        #         count = count + 1
        #soup.body.replace_with(translated_text)
        html = str(soup)

        cache.append(html)
        return html

    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, host="0.0.0.0", reload=True)
