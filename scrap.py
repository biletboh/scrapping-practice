import urllib2
from bs4 import BeautifulSoup


nestle = "https://www.nestleprofessional.us/lean-cuisine/lean-cuisine-macaroni-cheese-4-x-76-ounces"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

nestle_page = urllib2.Request(nestle, headers=hdr)


def extract_data(page):

    try:
        page = urllib2.urlopen(page)
    except urllib2.HTTPError, e:
        print e.fp.read()

    soup = BeautifulSoup(page)
    product = soup.h1.span.find(text=True)
    description = soup.find_all('div', class_='headline')[0].div.find(text=True)
    all_tables = soup.find_all('table')

    nutritional_table = all_tables[0]
    serving_table= all_tables[2]
    serving_size = serving_table.find_all('tr')

    nutr_info = []
    serving_info = [serving_size[0], serving_size[2]]
    info_table = serving_info + nutritional_table.find_all('tr')[1:] 

    for row in info_table:
        row_name = row.th.find(text=True)
        cells = row.find_all('td')
        info = []
        for cell in cells:
            c = cell.find(text=True)
            info.append(c)
        nutr_info.append({row_name: info})
    return {
            'product': product, 
            'description': description, 
            'nutritional info': nutr_info
            }


print extract_data(nestle_page)

