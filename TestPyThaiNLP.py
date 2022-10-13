from pythainlp import correct
from pythainlp import spell
from pythainlp import word_tokenize

#text="ตามหาหนังเกาหลีที่กลุ่มตำรวจไปเปิดร้านไก่ทอดเพื่อซุ่มสืบเรื่องราวของพวกค้ายา แต่ไก่ทอดดันขายดีและมีชื่อเสียงจนกลุ่มตำรวต้องจริงจังกับเรื่องการเปิดร้าน"
#refineWord = word_tokenize(text);
#print(refineWord)
print(correct("ตำรว"))
#TFIDF