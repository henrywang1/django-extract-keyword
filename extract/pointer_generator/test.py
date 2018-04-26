import os


f = 'produce_data/finished_files/vocab'

dirpath = os.path.dirname(os.path.abspath(__file__))
f = os.path.dirname(os.path.join(dirpath,f))
print(f)

