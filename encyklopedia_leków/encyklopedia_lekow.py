# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import urllib.request
from bs4 import BeautifulSoup
import re

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
        medicines.append(set_of_links[index])
        index += 1

    return medicines
    #for link in soup.find_all('a'):
    #    print(link.get('href'))

def print_medicines(list_od_medicines):
    for med in list_od_medicines:
        print(med)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = 'https://www.doz.pl/leki/strona/1'
    soup = fetch_url(url)
    medicines = find_links(soup)
    print_medicines(medicines)
   # print(response)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
