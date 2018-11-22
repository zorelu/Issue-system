import os
import time

print(os.getcwd())
print(os.path.abspath('./static/images'))
print(os.path.dirname(__file__))

print(len('__01中医馆.png'.split('.')))
print(['1', '2'][0])
t = time.time()
print(str(int(t)))