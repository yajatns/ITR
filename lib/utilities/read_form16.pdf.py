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
    print "==================================="
    print "Start to convert from PDF to images"
    print "==================================="
    pages = convert_from_path(pdf_path='/Users/yajat/PycharmProjects/BankStatement/asset/akhilesh_J36964.pdf', dpi=500,
                              userpw='BAAPG0280R')
    print "========================================="
    print "Successfully converted from PDF to images"
    print "========================================="
    i = 1
    print "==========="
    print "Save images"
    print "==========="
    for page in pages:
        page.save('out%s.jpg' % i, 'JPEG')
        i += 1
    all_text = []
    form_16_a = []
    form_16_b = []
    form16_a_page1 = 0
    form16_b_page1 = 0
    form16_b_last_page = 0
    print "===================================="
    print "Start to convert from Images to text"
    print "===================================="
    for x in range(1, i):
        page_text = pytesseract.image_to_string(Image.open('out%s.jpg' % x))
        all_text.append(page_text)
        if "TDS" in page_text and "Centralized Processing Cell" in page_text and "FORM NO. 16" in page_text and "PART A" in page_text:
            form16_a_page1 = x

        if "TDS" in page_text and "Centralized Processing Cell" in page_text and "FORM NO. 16" in page_text and "PART B" in page_text:
            form16_b_page1 = x
            form_16_b.append(page_text)
        if "Signature of person" in page_text and "responsible for deduction of" in page_text:
            form16_b_last_page = x
    print "================================"
    print "Seperate Form 16 A and form 16 B"
    print "================================"
    for index, page_content in enumerate(all_text):
        page_number = index + 1
        if page_number >= form16_a_page1 and page_number < form16_b_page1:
            form_16_a.append(page_content)
        elif page_number >= form16_b_page1 and page_number <= form16_b_last_page:
            form_16_b.append(page_content)

    print "========="
    print "Form 16 A"
    print "========="
    print form_16_a
    print "========="
    print "Form 16 B"
    print "========="
    print form_16_b
