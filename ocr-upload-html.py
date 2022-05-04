"""Uploads textoNOT to its corresponding vid.

No authentication is required, as it uses existing cookies in text file. This
file must be first generated using "Get cookies.txt" extension for Chrome while
logged in to both Google and vLex accounts. Text file is then parsed into a
dictionary compatible with requests module.
"""

import os
import requests


# Set local variables
cookies_file = '/Users/santiagofacchini/Downloads/cookies.txt'
ocr_files = '/Users/santiagofacchini/Downloads/ocr'


def cookie_file_parser(cookies_file):
    """Parses cookies text file used for authentication into a dictionary.

    Args:
        Plain text file from "Get cookies.txt" extension for Chrome. Prior to
        exporting cookies to text file, make sure user is logged in to both
        Google and vLex, and open https://app.vlex.com. Then export cookies to
        file.

    Returns:
        A dictionary of name-value pairs resulting from parsing the text file.

    Raises:
        Manually remove blank and # lines from text file, lines 1-4. Otherwise,
        it raises list out of range error. For example:

        1 # Netscape HTTP Cookie File
        2 # http://curl.haxx.se/rfc/cookie_spec.html
        3 # This is a generated file!  Do not edit.
        4 
    """

    cookies = {}
    with open(cookies_file, 'r') as cookie_file_content:
        for line in cookie_file_content:        
            line_fields = line.strip().split('\t')
            cookies[line_fields[5]] = line_fields[6]
    return cookies

# Parse cookies text file
parsed_cookies = cookie_file_parser(cookies_file)

# Change working directory
os.chdir(ocr_files)

# Loop over ocr files
for ocr_file in os.listdir(ocr_files):

    # Skip hidden OS files
    if not ocr_file.startswith('.'):

        # Read file content
        with open(ocr_file, 'r').read() as plain_text:

            # Get vid
            vid = ocr_file.replace(r'.htm', '')
            print(f'Uploading textoNOT to https://admin.vlex.com/vid/{vid}')

            # vLex form payload
            payload = {
                'textoNOT': plain_text,
            }

            # POST requests are made to https://admin.vlex.com/vid/<vid>/update
            # Must include parsed cookies and payload
            post_request = requests.post(
                f'https://admin.vlex.com/vid/{vid}/update',
                cookies=parsed_cookies,
                data=payload,
            )

            print('OK!')
