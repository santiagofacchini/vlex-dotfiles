import requests
import sys


# Path to cookies file
cookies_file = '/Users/santiagofacchini/Downloads/cookies.txt'

def cookie_file_parser(cookie_file):
    """Parses cookies text file and returns a dictionary of key value pairs
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

# vids
vids = sys.argv[1].split(',')

# Update fields in paylad
with requests.Session() as s:

    payload = {
        # 'documento[texto4]': '',
        # 'documento[texto3]': '',
        # 'documento[texto2]': '',
        # 'documento[texto1]': '',
        # 'documento[texto5]': '',
        # 'fecha_1_nullify': '',
        'documento[fecha1(3i)]': 1,
        'documento[fecha1(2i)]': 5,
        'documento[fecha1(1i)]': 2022,
        'documento[fecha2(3i)]': 1,
        'documento[fecha2(2i)]': 5,
        'documento[fecha2(1i)]': 2022,
        # 'documento[descriptor1]': '',
        # 'textoENT': '',
        # 'textoNOT': '',
        # 'adjunto': '',
    }

    for vid in vids:
        response = s.post(
            url=f'https://admin.vlex.com/vid/{vid}/update',
            cookies=parsed_cookies,
            data=payload
            )
        print(vid, response)
