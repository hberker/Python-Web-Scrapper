import requests
import csv
from bs4 import BeautifulSoup
url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'

# get Page #
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

table = soup.find('tbody', attrs={'class': 'stripe'})
list_of_rows = []

for row in table.findAll('tr')[1:]:
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)
for i in list_of_rows:
    try:
        i.pop()
    except IndexError:
        pass
    print(i)
outfile = open("./inmates.csv", "w") 
writer = csv.writer(outfile)
writer.writerow(["Last", "First", "Middle", "Gender", "Race", 0, "City", "State" ])
#writer.writerow(['Last', 'First', 'Middle', 'Gender', 'Race', 'Age', 'City', 'State'])
writer.writerows(list_of_rows)
