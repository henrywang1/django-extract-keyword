import pickle
import os
import sys
sys.path.insert(0, './jieba/')
import jieba
import jieba.analyse
import pandas as pd

# 從db讀自訂字典
import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute('SELECT * FROM extract_keyword')
keywords = c.fetchall()

c.execute('SELECT * FROM extract_stopword')
stopwords = c.fetchall()

for w in keywords:
    jieba.add_word(w[1])

for w in stopwords:
    jieba.analyse.add_stop_word(w[1])

# 從檔案讀自訂字典
# jieba.load_userdict(os.path.join("./extract/dict_with_cnt.txt"))
# jieba.analyse.set_stop_words(os.path.join("./extract/ntub_stop_words.txt"))

# 讀取範例文章
input_article = pd.read_csv('input.csv') #範例用文章
input_article['title_content'] = input_article['title'] + ' '+ input_article['content'] 
topK = 10


# 擷取關鍵字
def get_tags(article):
    tags = jieba.analyse.extract_tags(article, topK=topK, withWeight=False)
    predict_tag = ','.join(tags)
    return predict_tag

input_article['predict_tags'] = input_article["title_content"].apply(get_tags)
print(input_article['predict_tags'] )

# 輸出結果
input_article.to_csv('output.csv', index=False)