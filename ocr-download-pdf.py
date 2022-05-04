"""Downloads PDF documents needed for OCR processing.

Vids must be first copied to clipboard, then run script. No authentication is
required: uses cookies text file, which is generated using "Get cookies.txt"
extension for Chrome. This file is then parsed into a dictionary of key value
pairs compatible with requests.

Random vid for testing and debugging: 842508601
"""

import requests
import pyperclip


# Set local variables
download_directory = '/Users/santiagofacchini/Downloads'
cookies_file = '/Users/santiagofacchini/Downloads/cookies.txt'

# Create a list of vids from clipboard
vids = pyperclip.paste().split('\n')
print(f'Files in queue: {len(vids)}')

def cookie_file_parser(cookie_file):
    """Parse cookies text file and return a dictionary of key value pairs
    compatible with requests. Prior to this, manually remove blank lines from
    file, otherwise, returns list out of range error.
    """

    cookies = {}
    with open(cookie_file, 'r') as cookie_file_content:
        for line in cookie_file_content:
            line_fields = line.strip().split('\t')
            cookies[line_fields[5]] = line_fields[6]
    return cookies

# Parse cookies text file
parsed_cookies = cookie_file_parser(cookies_file)

# Download PDF files
for vid in vids:
    print(f'Downloading {vid}.pdf...', end=' ')
    
    # First request returns a redirect to AWS
    aws_redirect = requests.get(
        url=f'https://admin.vlex.com/vid/{vid}/download',
        cookies=parsed_cookies,
    )
    
    # Actual response in bytes
    pdf_response = requests.get(aws_redirect.url)

    # Save response content to PDF file
    with open(f'{download_directory}/{vid}.pdf', 'wb') as pdf_file:    
        pdf_file.write(pdf_response.content)    
        print('DONE!')
