import os
import sys
import PyPDF2

def pdf_merger(dir: str):
    '''Merges PDF files into a single file.
    '''
    # List downloaded PDF files
    directory_content = os.listdir(dir)

    # Call the merger
    merged_object = PyPDF2.PdfFileMerger()

    for file in sorted(directory_content):
        if file.endswith('.pdf'):
            print(file)
            merged_object.append(PyPDF2.PdfFileReader(f'{dir}{file}'))

    # Write merged data to a single PDF file and close
    merged_object.write(f'{dir}merged.pdf')
    merged_object.close()

# Directory where PDF files are located
pdf_directory = sys.argv[1]

pdf_merger(pdf_directory)
