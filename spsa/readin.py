import PyPDF2
import re

reTag = re.compile("[0-9]{4}")

fi = open('data/SPSA-2017-Preliminary-Program-v4.pdf', 'rb')
obj = PyPDF2.PdfFileReader(fi)
print(obj.getDocumentInfo())
print(obj.getFields())
print(obj.getNumPages())
pages = []
chunks = []
for p in obj.pages:
    txt = p.extractText().replace("\n", "")
    txtLi = reTag.split(txt)
    for t in txtLi:
        chunks.append(t)
    pages.append(txt)
fi.close()
