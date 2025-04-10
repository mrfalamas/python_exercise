import os
from bs4 import BeautifulSoup
import json

def main():
    py_dir = os.path.dirname(os.path.abspath(__file__))
    gr_dir = os.path.join(py_dir, "students_grades")
    json_path = os.path.join(gr_dir, "output.json")
    html_path = os.path.join(gr_dir, "output.html")

    json_dict = {}
    ct_dict = {}
    ct_ct = 0

    if os.path.isfile(html_path):
        with open(html_path, 'r') as f:
            contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")

        for child in soup.descendants:
            if child.name == 'th':
                json_dict[child.text] = []
                ct_dict[ct_ct] = []
                ct_ct = ct_ct + 1

        row_ct = 0
        for row in soup.find_all("tr"):
            if row_ct > 0:
                cells = row.find_all("td")
                for i, value in enumerate(cells):
                    ct_dict[i].append(value.text)

            row_ct = row_ct+1

        for grades in ct_dict:
            for i, name in enumerate(json_dict):
                if grades == i:
                    json_dict[name] = ct_dict[grades]

        r = open(json_path, 'wb')
        json_string = json.dumps(json_dict, indent=len(json_dict))
        r.write(json_string.encode('utf-8'))
        if os.path.isfile(json_path):
            print('File output.json was created')
    else:
        print('No output .json could be created')

if __name__ == "__main__":
    main()
