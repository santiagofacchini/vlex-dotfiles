"""Corrects HTML files and uploads compressed zip files to ftp multiarchivo.

After text is extracted from PDF files, images of the same vid are grouped,
compressed and uploaded to multiarchivo FTP, and HTML files are corrected.
"""

import re
import os
import shutil
import ftplib


# Set local variables
directory = '/Users/santiagofacchini/Downloads/ocr'

# Change working directory
os.chdir(directory)
print(f'Current working directory is: {directory}')
print(f'Found {str(len(os.listdir(directory)))} elements:')

# FTP connection
ftp = ftplib.FTP(
    os.environ['MULTIARCHIVO_HOST'],
    os.environ['MULTIARCHIVO_USER'],
    os.environ['MULTIARCHIVO_PASS'],
)

# Print FTP welcome message
print(ftp.getwelcome())

# Loop through files in directory
for element in os.listdir(directory):
    
    # Work with images: create one folder for each set of images
    # If element is not an image, do nothing
    if element.endswith('.htm') or element == '.DS_Store':
        pass

    # If element is an image
    else:
        # Create image folder
        folder_name = re.sub(r'-\d+\..{3}', '', element)
        if os.path.isdir(f'{directory}/{folder_name}') is False:
            os.mkdir(f'{directory}/{folder_name}')

        # Copy image to its corresponding folder
        if os.path.isfile(f'{directory}/{folder_name}/{element}') is False:
            src = f'{directory}/{element}'
            dst = f'{directory}/{folder_name}/{element}'
            shutil.move(src, dst)

# Compress image folders, upload to FTP, delete uncompressed folders
for folder in os.listdir(directory):
    if os.path.isdir(folder):
        print(f'Compressing {folder} and uploading it to FTP...')
        file_name = f'{folder}.zip'
        zip_folder = shutil.make_archive(folder, 'zip', directory, folder)
        upload_file = open(zip_folder, 'rb')
        ftp.storbinary('STOR ' + file_name, upload_file)
        shutil.rmtree(folder)
        print('DONE!')

    # Convert file content to string, make replacements
    if os.path.isfile(element) and element != '.DS_Store':
        print(f'Correcting OCR in {element}...')
        with open(element, 'r').read() as file_content:
            file_content = re.sub(r'\r', '', file_content)
            file_content = re.sub(r'<!DOCTYPE.*<body>\n?', '', file_content, 0, re.DOTALL)
            file_content = re.sub(r'</body>\n?', '', file_content)
            file_content = re.sub(r'</html>\n?', r'', file_content)
            file_content = re.sub(r'</?p>', r'', file_content)
            file_content = re.sub(r'\t', r' ', file_content)
            file_content = re.sub(r'&nbsp;+', r' ', file_content)
            file_content = re.sub(r'<img src="[^/]+/([^\s]+) ([^>]+)/>', r'\n<center><img vlex:fn_original="\1 \2 /></center>', file_content)
            file_content = re.sub(r' ?[\'*^•] ?', r' ', file_content)
            file_content = re.sub(r' +', r' ', file_content)
            file_content = re.sub(r'\.\W+$', '.', file_content)
            file_content = re.sub(r' ?°', r'º', file_content)
            file_content = re.sub(r'Nos?\.', r'Nº', file_content)
            file_content = re.sub(r'CAP.TUL. ([^ ]+) ', r'CAPÍTULO \1\n', file_content)
            file_content = re.sub(r'T.TUL. ([^ ]+) ', r'TÍTULO \1\n', file_content)
            file_content = re.sub(r'iqú', r'íqu', file_content)
            file_content = re.sub(r'<sup> ?[QSsoa0] ?</sup>', r'º', file_content)
            file_content = re.sub(r' i([oa]) ', r' l\1 ', file_content)
            file_content = re.sub(r' í([oa]) ', r' l\1 ', file_content)
            file_content = re.sub(r' i([oa])s ', r' l\1s ', file_content)
            file_content = re.sub(r' asi(\W)', r' así\1', file_content)
            file_content = re.sub(r' él ', r' el ', file_content)
            file_content = re.sub(r' él\n', r' el ', file_content)
            file_content = re.sub(r' dél ', r' del ', file_content)
            file_content = re.sub(r' la\n', r' la ', file_content)
            file_content = re.sub(r' del\n', r' del ', file_content)
            file_content = re.sub(r'rt.culo', r'rtículo', file_content)
            file_content = re.sub(r'^SECCI.N ([^ ]+) ', r'SECCIÓN \1\n', file_content)
            file_content = re.sub('Iº', '1º', file_content)
            output_file = open(element, 'w')
            output_file.write(file_content)
            print('OK!')

# Close ftp connection
ftp.quit()
print('FTP connection closed!')