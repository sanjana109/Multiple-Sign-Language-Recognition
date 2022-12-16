import PIL
import os
import os.path
from PIL import Image

f = 'C://Users//shree//Desktop//data//train//A'
for file in os.listdir(f):
    f_img = f+"/"+file
    img = Image.open(f_img)
    img = img.resize((128,128))
    img.save(f_img)