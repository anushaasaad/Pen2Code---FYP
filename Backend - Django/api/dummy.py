import pathlib
import os

path = max(pathlib.Path('modia/covers/').glob('*/'), key=os.path.getmtime)
print(path)
name = str(path).split('\\')
p = os.listdir(path)
print(name[-1])
print(p)
p = os.listdir(path)
pic_path = str(path) + "\\" + str(p[0])