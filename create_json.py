import os
from bs4 import BeautifulSoup
import json

def main():
    py_dir = os.path.dirname(os.path.abspath(__file__))
    tst_dir = os.path.join(py_dir, "test_results")
    json_path = os.path.join(tst_dir, "output.json")
    html_path = os.path.join(tst_dir, "output.html")

    json_dict = {}

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
                    json_dict[module_name].append(cell.text)

        r = open(json_path, 'wb')
        json_string = json.dumps(json_dict, indent=len(json_dict))
        r.write(json_string.encode('utf-8'))
        if os.path.isfile(json_path):
            print('File output.json was created')
    else:
        print('No output .json could be created')

if __name__ == "__main__":
    main()
