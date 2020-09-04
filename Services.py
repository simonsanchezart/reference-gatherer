import os
import re
import requests
import bs4
from selenium import webdriver
from time import sleep
from source import Source
from random import randint


class Artstation(Source):
    def __init__(self):
        super().__init__(ident='a', name='Artstation',
                         url='https://www.artstation.com/', query='https://www.artstation.com/search?q={searchTerm}&sort_by=relevance')

    def Download(self, searchTerm, folder):
        print(f'Downloading {searchTerm} from {self.name}')

        subFolder = os.path.join(folder, self.name)
        os.makedirs(subFolder, exist_ok=True)

        browser = webdriver.Firefox()
        browser.get(self.query.replace('{searchTerm}', searchTerm))

        linkElems = browser.find_elements_by_class_name('gallery-grid-link')
        artworks = []

        for link in linkElems:
            artworks.append(link.get_attribute('href'))

        for artwork in artworks:
            browser.get(artwork)
            imageElems = browser.find_elements_by_tag_name('img')

            for image in imageElems:
                src = image.get_attribute('src')

                # if there's no src, we skip this iteration to avoid exceptions
                if src is None:
                    continue

                # large is found on .jpgs or .pngs
                # original is found for .gifs
                if 'large' or 'original' in src:
                    # in the url we get the name and the file format with regex
                    imageRegex = re.compile(
                        r'(/large/|/original/)([a-zA-Z0-9\-]*)(\.\D{3})')
                    mo = imageRegex.search(src)
                    if mo is None:
                        continue
                    req = requests.get(src)

                    # second group is the name, third group is the file format
                    imageName = f'{mo.group(2)}{mo.group(3)}'
                    imagePath = os.path.join(
                        searchTerm, self.name, imageName)
                    imageFile = open(imagePath, 'wb')
                    for chunk in req.iter_content(100000):
                        imageFile.write(chunk)
                    imageFile.close()
                else:
                    continue
        return


class Pinterest(Source):
    def __init__(self):
        super().__init__(ident='p', name='Pinterest',
                         url='https://www.pinterest.com/', query='https://www.pinterest.com/search/pins/?q={searchTerm}')

    def Download(self, searchTerm, folder):
        print(f'Downloading {searchTerm} from {self.name}')

        subFolder = os.path.join(folder, self.name)
        os.makedirs(subFolder, exist_ok=True)

        browser = webdriver.Firefox()
        browser.get(self.query.replace('{searchTerm}', searchTerm))
        sleep(2)

        linkElems = browser.find_elements_by_tag_name('a')
        pins = []
        for link in linkElems:
            pinLink = link.get_attribute('href')
            if pinLink is None:
                continue
            if pinLink.startswith('https://www.pinterest.com/pin/'):
                pins.append(pinLink)
            else:
                continue

        for pin in pins:
            browser.get(pin)
            imageElems = browser.find_elements_by_tag_name('img')
            for image in imageElems:
                try:
                    src = image.get_attribute('src')

                    if src is None:
                        continue

                    if src.startswith('https://i.pinimg.com/originals/'):
                        # we get the file format by looking at the last 4 digits from src
                        fileFormat = src[-4:]
                        req = requests.get(src)

                        idImage = randint(0, 99999999)
                        imageName = f'{idImage}{fileFormat}'
                        imagePath = os.path.join(
                            searchTerm, self.name, imageName)
                        imageFile = open(imagePath, 'wb')
                        for chunk in req.iter_content(100000):
                            imageFile.write(chunk)
                        imageFile.close()
                    else:
                        continue
                except:
                    continue
        return

class DeviantArt(Source):
    def __init__(self):
        super().__init__(ident='d', name='DeviantArt',
                         url='https://www.deviantart.com/', query='https://www.deviantart.com/search/deviations?q={searchTerm}')

    def Download(self, searchTerm, folder):
        print(f'Downloading {searchTerm} from {self.name}')

        subFolder = os.path.join(folder, self.name)
        os.makedirs(subFolder, exist_ok=True)

        browser = webdriver.Firefox()
        browser.get(self.query.replace('{searchTerm}', searchTerm))

        linkElems = browser.find_elements_by_tag_name('a')
        deviants = []
        for link in linkElems:
            dataHook = link.get_attribute('data-hook')
            deviantHref = link.get_attribute('href')
            if dataHook == 'deviation_link':
                if deviantHref is None:
                    continue
                deviants.append(deviantHref)

        for deviant in deviants:
            req = requests.get(deviant)
            html = req.text
            soup = bs4.BeautifulSoup(html, 'html.parser')

            imageDiv = soup.find('div', attrs={'data-hook': 'art_stage'})
            image = imageDiv.find('img').get('src')

            if '.jpg' in image:
                fileFormat = '.jpg'
            elif '.png' in image:
                fileFormat = '.png'
            elif '.gif' in image:
                fileFormat = '.gif'

            req = requests.get(image)
            idImage = randint(0, 99999999)
            imageName = f'{idImage}{fileFormat}'
            imagePath = os.path.join(
                searchTerm, self.name, imageName)
            imageFile = open(imagePath, 'wb')
            for chunk in req.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        return