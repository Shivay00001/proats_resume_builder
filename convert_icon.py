
from PIL import Image
import os

source = r"C:/Users/shiva/.gemini/antigravity/brain/207f1ace-a693-4e61-91cd-09b370f349db/app_icon_1770102253139.png"
dest = "app_icon.ico"

img = Image.open(source)
img.save(dest, format='ICO', sizes=[(256, 256)])
print(f"Icon converted: {dest}")
