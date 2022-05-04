import os
import sys
import ghostscript


def pdf_to_pdfa(dir: str):
    '''Converts PDF files to PDF/A.
    '''
    pdf_files = sorted(os.listdir(dir))
    os.mkdir(f'{dir}pdfa-files')
    for pdf_file in pdf_files:
        if pdf_file.endswith('.pdf'):
            print(pdf_file)
            args = [
                '-dPDFA=1',
                '-dBATCH',
                '-dNOPAUSE',
                '-sColorConversionStrategy=RGB',
                '-sDEVICE=pdfwrite',
                f'-sOutputFile={dir}pdfa-files/{pdf_file}',
                f'{dir}{pdf_file}',
            ]
            ghostscript.Ghostscript(*args)
            os.remove(f'{dir}{pdf_file}')

pdf_directory = sys.argv[1]
pdf_to_pdfa(pdf_directory)
