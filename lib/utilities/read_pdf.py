from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
#PIL
import camelot
import pandas
import numpy


class Form16A:

    def __init__(self, location, file_name, password=""):
        self.file = None
        output = PdfFileWriter()
        temp_file = PdfFileReader(open(location+file_name, "rb"))
        if password:
            temp_file.decrypt(password=password)
        self.num_pages = temp_file.getNumPages()
        for i in range(temp_file.getNumPages()):
            page = temp_file.getPage(i)
            page_content = page.extractText()
            # print page_content.split('FORM NO. 16')
            print 'page %s' % i
            content = str(page_content.encode('utf-8'))
            if content.startswith('FORM NO. 16'):
                cur = content.split('FORM NO. 16')[1]
                if cur.startswith('[See rule 31(1)(a)]'):

                    print 'This is 16A beginning'
                    print cur.split('Certificate under Section 203 of the Income-tax Act, 1961 for '
                                    'tax deducted at source on salary')[1]
                elif cur.startswith('Certificate under Section 203'):
                    print 'This is 16B beginning'
                    print cur.split('Certificate under Section 203 of the Income-tax Act, 1961 for '
                                    'tax deducted at source on salary')[1]


if __name__ == '__main__':
    # ts = Form16A(location='/Users/yajat/PycharmProjects/BankStatement/asset/', file_name="akhilesh_J36964.pdf",
    #              password="BAAPG0280R")
    # print ts.file['content']
    # print ts.file.keys()
    # print ts.file.getPage(0).extractText().encode('utf-8')

    # raw = parser.from_file('/Users/yajat/PycharmProjects/BankStatement/asset/akhilesh_J36964.pdf')
    # print(raw['content'])
    # print raw.keys()
    pages = convert_from_path(pdf_path='/Users/yajat/PycharmProjects/BankStatement/asset/akhilesh_J36964.pdf', dpi=500,
                              userpw='BAAPG0280R')
    i = 0
    for page in pages:
        page.save('out%s.jpg' % i, 'JPEG')
        i += 1
    pytesseract.image_to_string(Image.open('out1.jpg'))
# sudo apt update
# sudo apt install tesseract-ocr
# sudo apt install libtesseract-dev
# brew install tesseract