import os
import re
import requests
import bs4
import PyPDF2


# vLex issue
vlex_issue = '1-2022'

# Create CSV file
csv_file = open(f'/Users/santiagofacchini/Downloads/20989_{vlex_issue}.csv', 'a')

# Seed url varies according to year to scrape
seed_url = requests.get('https://www.cefp.gob.mx/new/pages_ingresos/div_deuda_publica.php#deudapub2022')

# Soup object, html parser
soup = bs4.BeautifulSoup(seed_url.content, 'html.parser')

# Main div for Análisis de Gasto Federalizado
# id must be set according to issue
id_regex = re.compile(r'deudapub2022')
main_div = soup.find('div', id=id_regex)


# Each document metadata is inside a <tr></tr>
trs = main_div.find_all('tr')

# Used to sort downloaded PDF files (for merging)
pdf_key = 0

# Page range
starting_page = 1
end_page = 0

for tr in trs:

    # Increment key by 1
    pdf_key += 1

    # document title
    title = tr.a.text.strip()

    # PDF file url
    url = tr.a['href']

    # Reformat date
    year, month, day = tr.td.text.strip().split('-')
    date = f'{day}/{month}/{year}'

    # Set "vLex descriptores1" based on PDF url
    # https://admin.vlex.com/descriptores1/20989
    if 'nota' in url:
        print(f'{url} is nota')
        vlex_descriptor = '01'

    elif 'documento' in url:
        print(f'{url} is estudio')
        vlex_descriptor = '02'

    elif 'infografias' in url:
        print(f'{url} is infografia')
        vlex_descriptor = '03'

    # Download PDF file
    pdf_content = requests.get(url)


    with open(f'/Users/santiagofacchini/Downloads/{str(pdf_key).zfill(2)}-{title}.pdf', 'wb') as pdf_file:
        pdf_file.write(pdf_content.content)

    # Count PDF file pages
    read_pdf = open(f'/Users/santiagofacchini/Downloads/{str(pdf_key).zfill(2)}-{title}.pdf', 'rb')
    pdf_pages = PyPDF2.PdfFileReader(read_pdf).numPages

    # Add up pages
    end_page += pdf_pages

    # Append metadata to CSV file
    csv_file.write(f'#{vlex_issue}\t{title}\t1-{pdf_pages}\t\t\t{date}\t\t{vlex_descriptor}\t{starting_page}-{end_page}\t06\n')

    # Add up pages
    starting_page += pdf_pages

# List downloaded PDF files
pdf_files = os.listdir('/Users/santiagofacchini/Downloads/')

# Call the merger
merged_object = PyPDF2.PdfFileMerger()

for pdf_file in sorted(pdf_files):
    if pdf_file.endswith('.pdf'):
        print(pdf_file)
        merged_object.append(PyPDF2.PdfFileReader(f'/Users/santiagofacchini/Downloads/{pdf_file}', 'rb'))

# Write merged data in a single PDF file
merged_object.write(f'/Users/santiagofacchini/Downloads/20989{vlex_issue}.pdf')

# Close CSV file
csv_file.close
