"""Python implementation for creating a json dictionary"""
import os
from bs4 import BeautifulSoup
import json
import sys
import pandas as pd
import math

json_dict = {}
py_dir = os.path.dirname(os.path.abspath(__file__))
tst_dir = os.path.join(py_dir, "test_results")
html_path = os.path.join(tst_dir, "output.html")
tpsr_path = os.path.join(tst_dir, "output.xlsx")
json_path = os.path.join(tst_dir, "output.json")

def from_html():
    if os.path.isfile(html_path):
        with open(html_path, 'r') as f:
            contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")

        table = soup.find("table")
        rows = table.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            for i, cell in enumerate(cells):
                module_name = cells[0].text
                if i == 0:
                    if module_name not in json_dict:
                        json_dict[module_name] = []
                else:
                    if cell.text == "\u2705":
                        json_dict[module_name].append("ok")
                    elif cell.text == "\u274c":
                        json_dict[module_name].append("nok")
                    elif '🔄' in cell.text:
                        json_dict[module_name].append("open")
                    else:
                        json_dict[module_name].append(cell.text)

        r = open(json_path, 'wb')
        json_string = json.dumps(json_dict, indent=len(json_dict))
        r.write(json_string.encode('utf-8'))
        if os.path.isfile(json_path):
            print('File output.json was created')
    else:
        print('No output.json could be created')

def from_excel():
    if os.path.isfile(tpsr_path):
        data = pd.read_excel(tpsr_path, header=None, index_col=None)

    for row in data.iterrows():
        for i, elem in enumerate(row[1]):
            if i == 0:
                person = elem
                if person not in json_dict.keys():
                    json_dict[person] = []
            else:
                if not(math.isnan(elem)):
                    json_dict[person].append(int(elem))

        r = open(json_path, 'wb')
        json_string = json.dumps(json_dict, indent=len(json_dict))
        r.write(json_string.encode('utf-8'))
        if os.path.isfile(json_path):
            print('File output.json was created')
    else:
        print('No output.json could be created')

def main():
    from_excel()
    # arg = sys.argv
    # if arg[1] == 'one':
    #     print("creating output.json file, based on info from output.html, for a specific activity")
    #     from_html()
    # elif arg[1] == 'all':
    #     print("creating output.json file, based on info from output.xlsx, for all test activities")
    #     from_excel()
    # else:
    #     print("no output.json file is created")

if __name__ == "__main__":
    main()
