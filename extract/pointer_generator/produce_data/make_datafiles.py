# -*-coding:utf-8-*-  
import os  
import struct  
import collections  
from tensorflow.core.example import example_pb2  
  
  
# We use these to separate the summary sentences in the .bin datafiles  
SENTENCE_START = '<s>'  
SENTENCE_END = '</s>'  
  
train_file = "./train/train.txt"  
val_file = "./val/val.txt"  
test_file = "./test/test.txt"  
finished_files_dir = "./finished_files"  
chunks_dir = os.path.join(finished_files_dir, "chunked")
  
VOCAB_SIZE = 200000
CHUNK_SIZE = 1000

def chunk_file(set_name):
  in_file = 'finished_files/%s.bin' % set_name
  reader = open(in_file, "rb")
  chunk = 0
  finished = False
  while not finished:
    chunk_fname = os.path.join(chunks_dir, '%s_%03d.bin' % (set_name, chunk)) # new chunk
    with open(chunk_fname, 'wb') as writer:
      for _ in range(CHUNK_SIZE):
        len_bytes = reader.read(8)
        if not len_bytes:
          finished = True
          break
        str_len = struct.unpack('q', len_bytes)[0]
        example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
        writer.write(struct.pack('q', str_len))
        writer.write(struct.pack('%ds' % str_len, example_str))
      chunk += 1


def chunk_all():
  # Make a dir to hold the chunks
  if not os.path.isdir(chunks_dir):
    os.mkdir(chunks_dir)
  # Chunk the data
  for set_name in ['train', 'val', 'test']:
    print ("Splitting %s data into chunks..." % set_name)
    chunk_file(set_name)
  print ("Saved chunked data in %s" % chunks_dir)
  
def read_text_file(text_file):  
  lines = []  
  with open(text_file, "r") as f:  
    for line in f:  
      lines.append(line.strip())  
  return lines  
  
  
def write_to_bin(input_file,out_file, makevocab=False):  
  if makevocab:  
    vocab_counter = collections.Counter()  

  with open(out_file, 'wb') as writer:  
    # read the  input text file , make even line become article and odd line to be abstract（line number begin with 0）  
    lines = read_text_file(input_file)  
    for i, new_line in enumerate(lines):  
      if i % 2 == 0:  
        article = lines[i].encode('utf-8') 
      if i % 2 != 0:  
        abstract = "%s %s %s" % (SENTENCE_START, lines[i], SENTENCE_END)  
        abstract = abstract.encode('utf-8')
  
        print('abstract: ')
        print(abstract.decode('utf-8'))
        #print('article: ')
        #print(article.decode('utf-8'))
        print('---------------------')
        # Write to tf.Example  
        tf_example = example_pb2.Example()  
        tf_example.features.feature['article'].bytes_list.value.extend([article])  
        tf_example.features.feature['abstract'].bytes_list.value.extend([abstract])  
        tf_example_str = tf_example.SerializeToString()  
        str_len = len(tf_example_str)  
        writer.write(struct.pack('q', str_len))  
        writer.write(struct.pack('%ds' % str_len, tf_example_str))  
  
        # Write the vocab to file, if applicable  
        if makevocab:  
          art_tokens = article.decode('utf-8').split(' ') 
          abs_tokens = abstract.decode('utf-8').split(' ')
          abs_tokens = [t for t in abs_tokens if t not in [SENTENCE_START, SENTENCE_END]] # remove these tags from vocab  
          tokens = art_tokens + abs_tokens  
          tokens = [t.strip() for t in tokens] # strip  
          tokens = [t for t in tokens if t!=""] # remove empty  
          vocab_counter.update(tokens)  
  
  print("Finished writing file %s\n" % out_file)
  
  # write vocab to file  
  if makevocab:  
    print("Writing vocab file...")
    with open(os.path.join(finished_files_dir, "vocab"), 'w') as writer:  
      for word, count in vocab_counter.most_common(VOCAB_SIZE):  
        writer.write(word + ' ' + str(count) + '\n')  
    print("Finished writing vocab file")
  
  
if __name__ == '__main__':  
  
  if not os.path.exists(finished_files_dir): os.makedirs(finished_files_dir)  
  
  # Read the text file, do a little postprocessing then write to bin files  
  write_to_bin(test_file, os.path.join(finished_files_dir, "test.bin"))  
  #write_to_bin(val_file, os.path.join(finished_files_dir, "val.bin"))  
  #write_to_bin(train_file, os.path.join(finished_files_dir, "train.bin"), makevocab=True)   
