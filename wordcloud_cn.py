# coding: utf-8
from os import path
import codecs
import jieba

from wordcloud import WordCloud, ImageColorGenerator

FONT_PATH = path.join(path.dirname(__file__), 'font', 'yahei.ttf')
STOPWORDS_PATH = path.join(path.dirname(__file__), 'stopwords', 'stopwords.txt')

class WordCloud_CN:
    def __init__(self, file_path, font_path=None, max_word=2000,
                 max_font_size=40, random_state=42, stopwords_path=None,
                 mask=None, background_color="white"):
        if font_path is None:
            self.font_path = FONT_PATH
        else:
            self.font_path = font_path

        if stopwords_path is None:
            self.stopwords_path = STOPWORDS_PATH
        else:
            self.stopwords_path = stopwords_path

        self.file_path = file_path
        self.max_word = max_word
        self.max_font_size = max_font_size
        self.random_state = random_state
        self.mask = mask
        self.backgroud_color = background_color
        self.wc = None

    def generate(self):
        self.wc = WordCloud(font_path=self.font_path, max_words=self.max_word,
                       max_font_size=self.max_font_size, random_state=self.random_state,
                       mask=self.mask, background_color=self.backgroud_color)
        return self.wc.generate(self.get_text)

    def recolor(self):
        image_colors = ImageColorGenerator(self.mask)
        return self.wc.recolor(color_func=image_colors)

    def save(self, file_path):
        self.wc.to_file(file_path)

    @property
    def get_text(self):
        text = open(self.file_path).read()
        stopwords = self.get_stopwords
        # print stopwords
        words = [w for w in jieba.cut(text) if w not in stopwords]
        # print words
        return ' '.join(words)

    @property
    def get_stopwords(self):
        text = codecs.open(self.stopwords_path, encoding='utf-8').readlines()
        words = [w.rstrip() for w in text]
        return set(words)
