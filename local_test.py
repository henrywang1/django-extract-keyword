import sqlite3
import psycopg2
conn = sqlite3.connect('db.sqlite3')
# conn = psycopg2.connect(database="defs1sr50t8t4j",
#                         user="vchkjmihktadra",
#                         password="d42c52f0fd439d0d9423f9f47ff5f7b7fc79edf871fb896dabf76816884f43fa",
#                         host="ec2-54-221-192-231.compute-1.amazonaws.com",
#                         port="5432")

# conn = psycopg2.connect(database="extract_local",
#                         port="5432")

#postgres://vchkjmihktadra:d42c52f0fd439d0d9423f9f47ff5f7b7fc79edf871fb896dabf76816884f43fa@ec2-54-221-192-231.compute-1.amazonaws.com:5432/defs1sr50t8t4j
# cursor.execute(sql [, optional parameters])
c = conn.cursor()
c.execute('SELECT * FROM extract_keyword')
ret = c.fetchall()
# # print([item for item in ret[-100:]])
# c.execute('SELECT MAX(id) from extract_keyword')
# ret = c.fetchone()
# print(ret[0])

def get_user_dict(file_name):
    # lfreq = {}
    # ltotal = 0
    ret = []
    # f_name = resolve_filename(f)
    with open(file_name, 'r') as f:
        for lineno, line in enumerate(f, 1):
            try:
                line = line.strip()
                word, freq = line.split('@@')[:2]
                ret.append(word)

            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (file_name, lineno, line))
        # f.close()
        # return lfreq, ltotal
    return ret

#ret = import_txt('./dict_with_cnt.txt')
def get_stop_words(file_name):
    ret = []
    with open(file_name, 'r') as f:
        for lineno, line in enumerate(f, 1):
            try:
                line = line.strip()
                ret.append(line)

            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' % (file_name, lineno, line))
    return ret

stop_words = get_stop_words('extract/ntub_stop_words.txt')
key_words = get_user_dict('extract/dict_with_cnt.txt')
#print(len(stop_words))

# ntub_stop_words.txt
# print(ret[-100:])
print(len(key_words), len(ret))
# c.execute("TRUNCATE TABLE extract_keyword RESTART IDENTITY;")
c.execute("DELETE FROM extract_keyword")
c.execute("DELETE FROM extract_stopword")
# DELETE FROM extract_keyword;")
# c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='extract_keyword';")
key_words = [k for k in key_words if len(k)<=30]
from tqdm import tqdm
for item in tqdm(key_words):
    sql='INSERT OR IGNORE INTO extract_keyword (keyword) VALUES ("{0}");'.format(item) #ON CONFLICT (keyword) DO NOTHING
    # print(sql)
    c.execute(sql)

for item in tqdm(stop_words):
    if not item.strip():
        continue
    sql='INSERT OR IGNORE  INTO extract_stopword (stop_word) VALUES ("{0}");'.format(item) #ON CONFLICT (stop_word) DO NOTHING;
    c.execute(sql)

    #try:
    #    ("INSERT INTO extract_keyword (keyword) VALUES ({0});".format((item,)))
    #    break
        #c.execute("INSERT INTO extract_keyword (keyword)\
        #VALUES (%s)", (item,))
                   
    #except:
    #    print('error insert {0}'.format(item))
    #    continue

conn.commit()

# c.execute("DELETE FROM extract_stopword;")
# # c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='extract_stopword';")

# for item in stop_words:
#     c.execute("INSERT INTO extract_stopword (stop_word) VALUES (%s)", (item,))
# conn.commit()
