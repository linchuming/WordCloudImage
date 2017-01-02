"""
Image-colored wordcloud
========================
You can color a word-cloud by using an image-based coloring strategy implemented in
ImageColorGenerator. It uses the average color of the region occupied by the word
in a source image. You can combine this with masking - pure-white will be interpreted
as 'don't occupy' by the WordCloud object when passed as mask.
If you want white as a legal color, you can just pass a different image to "mask",
but make sure the image shapes line up.
"""

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'test2.txt')).read()
jb = jieba.cut(text)
zh_text = ' '.join([w for w in jb])

# read the mask / color image
# taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
alice_coloring = np.array(Image.open(path.join(d, "alice_color.png")))
stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(font_path='../font/yahei.ttf',
    background_color="white", max_words=2000, mask=alice_coloring,
    stopwords=stopwords, max_font_size=40, random_state=42)
# generate word cloud
wc.generate(zh_text)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

# show
plt.imshow(wc)
plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
plt.figure()
plt.imshow(alice_coloring)
plt.axis("off")
plt.show()