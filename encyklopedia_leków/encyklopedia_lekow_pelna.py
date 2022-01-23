# http://leki.urpl.gov.pl/index.php?id=%27%%27

import urllib.request
from urllib.error import HTTPError
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
        try :
            html_file = urllib.request.urlopen(link)
            soup = BeautifulSoup(html_file, 'html.parser')
            #print(soup.prettify())
            title = soup.title.string
            noticed = False
            result_row = ["", "", "", link]
            previous = ""
            for para in soup.find_all('h3'): #h3
                #print(para.get_text())
                stringified = para.get_text()
                if re.search("nterakcj", stringified) != None:
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
                for active in soup.find_all('dt'):
                    stringified_active = active.get_text()
                    #print(stringified_active)
                    if re.search("Substancje aktywne", stringified_active):
                        print(stringified_active)
                        next = active.find_next('div')
                        next_text = next.get_text()
                        splitted = next_text.split('  ')
                        #print(splitted)
                        res_splitted = [el for el in splitted if el != '' and el != '\n']
                        print(res_splitted)
                        res_string = " ".join(res_splitted)
                        print(res_string)
                        result_row.append(res_string)

                # for indications in soup.find_all('button'):
                #     stringified_button = indications.get_text()
                #     print(stringified_button, " button")

                for ind in soup.find_all('h3'):
                    stringified_ind = ind.get_text()
                    #print(stringified_ind, " h2")
                    res = []
                    if re.search("Wskazania", stringified_ind):
                        next = ind.find_next('p')
                        next_text = next.get_text()
                        result_row.append(next_text)
                        print(next_text)

                for ind2 in soup.find_all('dt'):
                    stringified_ind2 = ind2.get_text()
                    #print(stringified_ind2, "ind2")
                    if re.search("Działanie", stringified_ind2):
                        next = ind2.find_next('div')
                        next_text = next.get_text()
                        splitted = next_text.split('  ')
                        # print(splitted)
                        res_splitted = [el for el in splitted if el != '' and el != '\n']
                        print(res_splitted)
                        res_string = " ".join(res_splitted)
                        print(res_string)
                        result_row.append(res_string)

                writer.writerow(result_row)
                print(result_row)
                print("WRITTEN")
                print('\n\n')

        except HTTPError as err:
            if err.code == 404:
                pass
            else:
                raise




if __name__ == '__main__':
    url = 'https://www.doz.pl/leki/strona/' #1
    #soup = fetch_url(url)
    #medicines = find_links(soup)
    #print_medicines(medicines)
    with open("lekiPelne.csv", "w", newline='') as csfile:
        writer = csv.writer(csfile)
        writer.writerow(["Polska nazwa", "Angielska nazwa", "Interakcje", "Strona",  "Substancja aktywna", "Wskazania", "Działanie"])
        for page in range (1, 90):
            new_page = url + str(page)
            soup = fetch_url(new_page)
            medicines = find_links(soup)
            open_medicines(medicines, writer)
   # print(response)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
