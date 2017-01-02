from wordcloud_cn import WordCloud_CN
from grabcut import grabCut
import matplotlib.pyplot as plt

if __name__ == '__main__':
    gc = grabCut('image/0.jpg')
    mask = gc.simple_mask()
    wc = WordCloud_CN('text/jn.txt', mask=mask)
    wc.generate()
    plt.imshow(wc.recolor())
    plt.axis("off")
    plt.show()
    # wc.save('result.jpg')