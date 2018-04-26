import pandas as pd
import glob
from sklearn.model_selection import train_test_split
import re
import gc
import jieba
#jieba.set_dictionary('../dictionary/dict@@.txt')
#jieba.load_userdict('../dictionary/dictionary@@.txt')
jieba.set_dictionary('./dict.big.txt')
jieba.load_userdict('./dict_with_cnt.txt')
import jieba.analyse
import re
import string
import numpy as np

def get_space_content(data,field='content'):
    wds = jieba.lcut(data[field])
    wds = map(lambda x:x.strip(),wds)
    wds = list(filter(lambda x:len(x)>0,wds))
    wds_list = []
    for wd in wds:
        if re.match('\d+',wd) is not None:
            continue
        elif re.match('©',wd) is not None:
            continue
        wds_list.append(wd)
    wds = wds_list
    del wds_list
    gc.collect()
    wds = (' ').join(wds)
    return wds

def clean_space(x):
    try:
        if np.isnan(x):
            return None
    except:
        x = re.sub('\u3000','',x)
        if len(x) == 0:
            return None
        return x

df = pd.read_csv('./article_contents_clean.csv',lineterminator="\n")
df = df.drop('Unnamed: 0',axis=1)
df = df.fillna(' ')
df_a = pd.read_csv('./abstracts.csv',lineterminator="\n")
df = pd.merge(df,df_a,on='pid',how='left')
df.columns = ['pid','title','content','abstract']
df.abstract = df.abstract.apply(clean_space)
df.title = df.title.apply(clean_space)
df = df.dropna()
df = df[df.abstract!=' ']
df = df[df.title!=' ']
df = df.iloc[:4000]
train,val = train_test_split(df,train_size=0.8)
val,test = train_test_split(val,train_size=0.5)

for t in ['train','val','test']:
    file_path = './{0}/{0}.txt'.format(t)
    print(file_path)
    if t == 'train':
        data = train
    elif t == 'val':
        data = val
    elif t == 'test':
        data = test
    with open(file_path,'w') as f:
        for k,v in data.iterrows():
            title = get_space_content(v,'title')
            content = get_space_content(v,'abstract')
            content = re.sub('\u3000','',content)
            content = re.sub('[\u3100-\u312F]','',content)
            content = re.sub('[%s]'%string.punctuation,'',content)
            content = re.sub('[\uff00-\uffef]','', content)
            content = re.sub('[\r\n]','',content)
            content = content.strip()
            content = '%s\n%s\n'%(content,title)
            f.write(content)
