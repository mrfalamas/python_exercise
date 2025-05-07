"""Python implementation for creating a json dictionary"""
import os
from bs4 import BeautifulSoup
import json
import sys
import pandas as pd
import math

activity_dict = {}
module_dict = {}
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

        for j, row in enumerate(data.iterrows()):
            if j == 0:
                for i, elem in enumerate(row[1]):
                    if i in [1, 7, 13, 24]:
                        if elem not in activity_dict.keys():
                            activity_dict[elem] = {}
            if j > 1:
                for i, elem in enumerate(row[1]):
                    module_name = row[1][0]
                    if (i >= 1 and i < 7):
                        if module_name not in activity_dict["Review of Test Specification"].keys():
                            activity_dict["Review of Test Specification"][module_name] = []
                        else:
                            activity_dict["Review of Test Specification"][module_name].append(str(elem))
                    if (i >= 7 and i < 13):
                        if module_name not in activity_dict["Review of Test Implementation"].keys():
                            activity_dict["Review of Test Implementation"][module_name] = []
                        else:
                            activity_dict["Review of Test Implementation"][module_name].append(str(elem))
                    if (i >= 13 and i < 24):
                        if module_name not in activity_dict["Non-Safety Tests (QM Requirements)"].keys():
                            activity_dict["Non-Safety Tests (QM Requirements)"][module_name] = []
                        else:
                            activity_dict["Non-Safety Tests (QM Requirements)"][module_name].append(str(elem))
                    if (i >= 24 and i < 35):
                        if module_name not in activity_dict["Safety Tests (ASIL Requirements)"].keys():
                            activity_dict["Safety Tests (ASIL Requirements)"][module_name] = []
                        else:
                            activity_dict["Safety Tests (ASIL Requirements)"][module_name].append(str(elem))

        print(activity_dict)
        print(module_dict)

        r = open(json_path, 'wb')
        json_string = json.dumps(activity_dict, indent=len(activity_dict))
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
