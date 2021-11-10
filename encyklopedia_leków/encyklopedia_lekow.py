# http://leki.urpl.gov.pl/index.php?id=%27%%27

import urllib.request
from bs4 import BeautifulSoup
import re
import csv

def fetch_url(homepage):
    html_file = urllib.request.urlopen(homepage)
    soup = BeautifulSoup(html_file, 'html.parser')
    #print(soup.prettify())

    return soup


def find_links(soup):
    medicines = []

    set_of_links = [link.get('href') for link in soup.find_all('a')]

    index = 0
    count = 0

    while (count < 2):
        index += 1
        if set_of_links[index] == '#':
            count += 1

    index += 2

    while (set_of_links[index] != '#' and re.match("/leki/strona/", set_of_links[index]) == None):
        medicines.append('https://www.doz.pl/' + set_of_links[index])
        index += 1

    return medicines



def print_medicines(list_od_medicines):
    for med in list_od_medicines:
        print(med)



def open_medicines(list_of_medicines, writer):
    for link in list_of_medicines:
        print(link)
        html_file = urllib.request.urlopen(link)
        soup = BeautifulSoup(html_file, 'html.parser')
        #print(soup.prettify())
        title = soup.title.string
        noticed = False
        result_row = ["", "", ""]
        previous = ""
        for para in soup.find_all('h3'): #h3
            #print(para.get_text())
            strigified = para.get_text()
            if re.search("nterakcj", strigified) != None:
                if not noticed:
                    title_list = title.split()[:2]
                    noticed = True
                    result_row[0] = title_list[0]
                    result_row[1] = title_list[1]
                    print(title_list)
                #print(para.next_sibling.get_text())
                next = para.find_next('p')
                next_text = next.get_text()
                if next_text != previous:
                    result_row[2] += next_text + '\n'
                    previous = next_text
                print(next_text)

        if noticed:
            writer.writerow(result_row)
        print('\n\n')



if __name__ == '__main__':
    url = 'https://www.doz.pl/leki/strona/' #1
    #soup = fetch_url(url)
    #medicines = find_links(soup)
    #print_medicines(medicines)
    with open("lekiBig3.csv", "w", newline='') as csfile:
        writer = csv.writer(csfile)
        writer.writerow(["Polska nazwa", "Angielska nazwa", "Interakcje"])
        for page in range (1, 90):
            new_page = url + str(page)
            soup = fetch_url(new_page)
            medicines = find_links(soup)
            open_medicines(medicines, writer)
   # print(response)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
