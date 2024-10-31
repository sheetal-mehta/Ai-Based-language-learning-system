import allosaurus
from allosaurus.app import read_recognizer

model = read_recognizer("allo_try2")
output = model.recognize("Q1200901.wav",'deu')
print(output)