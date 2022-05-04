import requests
import os
import bs4
import PyPDF2


# vLex issue
vlex_issue = '1-2022'

# Create CSV file
csv_file = open(f'/Users/santiagofacchini/Downloads/20387/20387_{vlex_issue}.csv', 'a')

# Seed url varies according to year to scrape
seed_url = requests.get('https://www.cefp.gob.mx/new/pages_gasto_federalizado/div_analisis_de_gasto_federalizado.php#analisis_gasto_fed2022I')

# Soup object, html parser
soup = bs4.BeautifulSoup(seed_url.content, 'html.parser')

# Main div for Análisis de Gasto Federalizado
# id must be set according to issue
main_div = soup.find('div', id="analisis_gasto_fed2022")

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
    # https://admin.vlex.com/descriptores1/20387
    if 'infografias' in url:
        print(f'{url} is infografia')
        vlex_descriptor = '01'

    elif 'documento' in url:
        print(f'{url} is estudio')
        vlex_descriptor = '02'

    elif 'nota' in url:
        print(f'{url} is nota')
        vlex_descriptor = '03'

    # Download PDF file
    pdf_content = requests.get(url)

    if len(str(pdf_key)) == 1: # Add 0 to one-digit numbers
        with open(f'/Users/santiagofacchini/Downloads/20387/0{pdf_key}-{title}.pdf', 'wb') as pdf_file:
            pdf_file.write(pdf_content.content)
            # Count PDF file pages
            read_pdf = open(f'/Users/santiagofacchini/Downloads/20387/0{pdf_key}-{title}.pdf', 'rb')
            pdf_pages = PyPDF2.PdfFileReader(read_pdf).numPages
            print(pdf_pages)

    elif len(str(pdf_key)) == 2: # Do nothing for two-digit numbers
        with open(f'/Users/santiagofacchini/Downloads/20387/{pdf_key}-{title}.pdf', 'wb') as pdf_file:
            pdf_file.write(pdf_content.content)
            # Count PDF file pages
            read_pdf = open(f'/Users/santiagofacchini/Downloads/20387/{pdf_key}-{title}.pdf', 'rb')
            pdf_pages = PyPDF2.PdfFileReader(read_pdf).numPages
            print(pdf_pages)

    # Add up pages
    end_page += pdf_pages

    # Append metadata to CSV file
    csv_file.write(f'#{vlex_issue}\t{title}\t1-{pdf_pages}\t\t\t{date}\t\t{vlex_descriptor}\t{starting_page}-{end_page}\t06\n')

    # Add up pages
    starting_page += pdf_pages

# List downloaded PDF files
pdf_files = os.listdir('/Users/santiagofacchini/Downloads/20387')

# Call the merger
merged_object = PyPDF2.PdfFileMerger()

for pdf_file in sorted(pdf_files):
    if pdf_file.endswith('.pdf'):
        print(pdf_file)
        merged_object.append(PyPDF2.PdfFileReader(f'/Users/santiagofacchini/Downloads/20387/{pdf_file}', 'rb'))

# Write merged data in a single PDF file
merged_object.write(f'/Users/santiagofacchini/Downloads/20387/20387_{vlex_issue}.pdf')

# Close CSV file
csv_file.close
