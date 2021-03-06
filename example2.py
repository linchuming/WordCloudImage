from wordcloud_cn import WordCloud_CN
from grabcut import grabCut
import matplotlib.pyplot as plt

if __name__ == '__main__':
    gc = grabCut('image/2.jpg')
    gc.set_rect()
    mask = gc.simple_mask()
    wc = WordCloud_CN('text/jjlin.txt', mask=mask)
    wc.generate()
    plt.imshow(wc.recolor())
    plt.axis("off")
    plt.show()