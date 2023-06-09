from pdf2image import convert_from_path
import pytesseract
import backend.src.util as util

from parser_prescription import PrescriptionParser
from parser_patient_details import PatientDetailParser

POPPLER_PATH=r'C:\poppler-21.11.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract(file_path,file_format):
    pages=convert_from_path(file_path,poppler_path=POPPLER_PATH)
    document_text=''

    if file_format=='prescription':
        for page in pages:
            processed_image = util.preprocess_image(page)
            document_text = pytesseract.image_to_string(processed_image, lang='eng')
            document_text=document_text.replace('\n', ' ')
            data=PrescriptionParser(document_text).parse()
        return data
    elif file_format=='patient_details':
        proc_image = util.proc_photo(pages[0])
        document_text = pytesseract.image_to_string(proc_image, lang='eng')
        document_text=document_text.replace('\n', ' ')
        data=PatientDetailParser(document_text).parse()
        return data

if __name__=='__main__':
    data=extract('../resources/patient_details/pd_2.pdf','patient_details')
    print(data)
