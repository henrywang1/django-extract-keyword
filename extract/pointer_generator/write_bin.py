import re
import struct
from tensorflow.core.example import example_pb2
import string
import gc
import os
import jieba
dirpath = os.path.dirname(os.path.abspath(__file__))
outfile = 'produce_data/finished_files/test*'
outfile = os.path.join(dirpath,outfile)

SENTENCE_START = '<s>'
SENTENCE_END = '</s>'

def get_space_content(data,mode='jieba'):
    if mode == 'jieba':
        wds = jieba.cut(data)
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
        #del wds_list
        #gc.collect()
        wds = (' ').join(wds)
    else:
        wds = (d for d in data)
        wds = map(lambda x:x.strip(),wds)
        wds = list(filter(lambda x:len(x)>0,wds))
    return wds

def read_text_file(text_file):
  lines = []
  with open(text_file, "r") as f:
    for line in f:
      lines.append(line.strip())
  return lines

def write_to_bin(article,out_file=outfile):
  #article = read_text_file('test.txt')
  #article = ' '.join(article)
  #print(article)
  with open(out_file, 'wb') as writer:
    # read the  input text file , make even line become article and odd line to be abstract（line number begin with 0）
    article = re.sub('\r\n','',article) 
    article = article.strip()
    article = re.sub('\u3000','',article)
    article = re.sub('[\u3100-\u312F]','',article)
    article = re.sub('[%s]'%string.punctuation,'',article)
    article = re.sub('[\uff00-\uffef]','', article)
    article = get_space_content(article) 
    article = article.encode('utf-8')
    
    abstract = "%s%s" % (SENTENCE_START, SENTENCE_END)
    abstract = abstract.encode('utf-8')

    tf_example = example_pb2.Example()
    tf_example.features.feature['article'].bytes_list.value.extend([article])
    tf_example.features.feature['abstract'].bytes_list.value.extend([abstract])
    tf_example_str = tf_example.SerializeToString()
    str_len = len(tf_example_str)
    writer.write(struct.pack('q', str_len))
    writer.write(struct.pack('%ds' % str_len, tf_example_str))
