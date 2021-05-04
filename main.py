import os
import gtts
import requests
import selenium
from selenium import webdriver
import time
import PIL
from PIL import ImageOps, ImageEnhance, ImageFilter
import pytesseract
from moviepy.editor import *
import numpy as np
import enchant
import collections
import string

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
d = enchant.Dict('en_US')
gotten_images = []

def filter_image(img):
    image = PIL.Image.fromarray(np.where(np.array(img) >= 250, 0, 250).astype('uint8'))
    image = ImageOps.grayscale(image)
    image = image.resize((int(image.size[0]/2), int(image.size[1]/2)), PIL.Image.ANTIALIAS)
    image = ImageEnhance.Sharpness(image).enhance(1)
    image = ImageEnhance.Contrast(image).enhance(2)
    image = image.resize((int(image.size[0]*2), int(image.size[1]*2)), PIL.Image.ANTIALIAS)
    return image

def image_string(image):
    words = []
    for c in range(14):
        try:
            txt = pytesseract.image_to_string(image, config=r'--psm {}'.format(c)).replace('|', 'I')
            txts = [s if d.check(s) else d.suggest(s)[0] for s in txt.split()]
            txts = [w for w in txts if w in 'aiAI' or len(w)>1]
            if len(txts)>0: words.append(txts)
        except:
            pass
    lists = list(set(map(tuple, words)))
    listScores = {k:0 for k in range(len(lists))}
    for i, lis in enumerate(lists):
        rest = lists[:]
        del rest[i]
        for n, word in enumerate(lis):
            for list2 in rest:
                try:
                    if word == list2[n]:
                        listScores[i] += 2
                    elif word in list2[n:]:
                        listScores[i] += 1
                    elif word not in list2:
                        listScores[i] -= 1
                except:
                    pass
    adj = {k:score/len(lists[k]) for k, score in listScores.items()}
    n = max(adj, key=lambda k: adj[k])
    if adj[n] < 0: return ' '
    return ' '.join(lists[n])

def image_to_movie():
    clip = ImageClip(f'imagee.jpg').set_duration(0.5)
    try:
        img = PIL.Image.open(f'imagee.jpg')
        txt = image_string(img)
        if txt == ' ':
            txt = image_string(filter_image(img))
        if not txt == ' ':
            gtts.gTTS(txt).save(f'audioo.mp3')
            audio = AudioFileClip(f'audioo.mp3')
            clip = clip.set_duration(audio.duration).set_audio(audio)
            os.remove(f'audioo.mp3')
    except:
        pass
    os.remove(f'imagee.jpg')
    return clip

def get_images():
    n = 0
    subreddits = ['dankmeme', 'meme']
    for sub in subreddits:
        driver = webdriver.Edge(executable_path=r'C:\Users\everc\OneDrive\Desktop\youtube\msedgedriver.exe')
        driver.get('https://reddit.com/r/'+sub)
        time.sleep(10)
        for img in driver.find_elements_by_tag_name('img')[1:-2]:
            src = img.get_attribute('src')
            if 'https://www.redditstatic.com' not in src and '/award_images/' not in src and 'external-preview' not in src:
                gotten_images.append(src)
                res = requests.get(img.get_attribute('src'))
                file = open(f'imagee.jpg', 'wb')
                file.write(res.content)
                file.close()
                n+=1
                image_to_movie().write_videofile(f'videos/{n}.mp4', fps=1)
                time.sleep(10)
        driver.quit()

get_images()
