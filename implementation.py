"""Module providing a function printing python version."""
import os
import pandas as pd
import math
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import os.path

main_dict = {}

def append_from_json(gr_dir):
    json_file = os.path.join(gr_dir, "01_review_test_spec.json")
    with open(json_file, 'r') as file:
        data = json.load(file)

    for key in data:
        person = key
        if person not in main_dict.keys():
            main_dict[person] = data[key]

def append_from_txt(gr_dir):
    txt_file = os.path.join(gr_dir, "02_review_test_impl.txt")
    f = open(txt_file, "r")
    for line in f:
        person = line.split(':')[0]
        if person not in main_dict.keys():
            main_dict[person] = []
        grades = line.split(':')[1]
        grades = grades.replace(" ", "")
        grades = grades.replace("\n", "")
        splitgr = grades.split(',')
        for gr in splitgr:
            main_dict[person].append(int(gr))

def append_from_xml(gr_dir):
    xml_file = os.path.join(gr_dir, "03_nonsafety_test.xml")
    tree = ET.parse(xml_file)
    students = tree.findall("student")

    for student in students:
        person = student.find('name').text

        if person not in main_dict.keys():
            main_dict[person] = []

        grades = student.find('grades').text
        grades = grades.replace(" ", "")
        each_gr = grades.split(",")
        for gr in each_gr:
            main_dict[person].append(int(gr))

def append_from_xls(gr_dir):
    xls_file = os.path.join(gr_dir, "04_safety_test.xlsx")
    data = pd.read_excel(xls_file, header=None, index_col=None)

    for row in data.iterrows():
        for i, elem in enumerate(row[1]):
            if i == 0:
                person = elem
                if person not in main_dict.keys():
                    main_dict[person] = []
            else:
                if not(math.isnan(elem)):
                    main_dict[person].append(int(elem))

def create_html(gr_dir, type):
    html_file = os.path.join(gr_dir, "output.html")
    file = open(html_file, "w")

    html_dict = main_dict

    if "01" in type or "02" in type:
        for module in html_dict:
            mod_checks = html_dict[module][0]
            mod_opens = html_dict[module][1]
            mod_fails = html_dict[module][2]
            open_rate = mod_opens*100 / mod_checks
            fail_rate = mod_fails*100 / mod_checks
            html_dict[module].append(round(open_rate, 2))
            html_dict[module].append(round(fail_rate, 2))
    elif "03" in type or "04" in type:
        html_dict = html_dict

    # Write HTML content
    file.write("<html>")
    file.write("<head>")
    file.write("<title>Test Results</title>")
    file.write("</head>")
    file.write("<body>")
    if "01" in type:
        file.write("<h1>Review of Test Specification</h1>")
        file.write("<p> </p>")
        file.write("<h3>&rArr; readed from 01_test_specification.JSON</h3>")
    if "02" in type:
        file.write("<h1>Review of Test Implementation</h1>")
        file.write("<p> </p>")
        file.write("<h3>&rArr; readed from 02_test_implementation.TXT</h3>")
    if "03" in type:
        file.write("<h1>Non-Safety Tests (QM Requirements)</h1>")
        file.write("<p> </p>")
        file.write("<h3>&rArr; readed from 03_test_qm_requirements.XML</h3>")
    if "04" in type:
        file.write("<h1>Safety Tests (ASIL Requirements)</h1>")
        file.write("<p> </p>")
        file.write("<h3>&rArr; readed from 04_test_asil_requirements.XLSX</h3>")
    file.write("<h3>&rArr; report generated at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "</h3>")
    file.write("<p> </p>")
    file.write("<table style=\"border:1px solid black; border-collapse: collapse; \">")
    file.write("<tr style=\"border:1px solid black; \">")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">Name</th>")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">Checks</th>")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">Open</th>")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">Fails</th>")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">Open Rate</th>")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">Fail Rate</th>")
    file.write("</tr>")
    for row in html_dict:
        file.write("<tr style=\"border:1px solid black; \">")
        file.write("<td style=\"border:1px solid black; padding: 10px;\">" + str(row) + "</td>")
        for value in html_dict[row]:
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(value) + "</td>")
        file.write("</tr>")
    file.write("</table>")
    file.write("</body>")
    file.write("</html>")

    # Close the file
    file.close()

    print("HTML file successfully written.")

def create_report(type):
    py_dir = os.path.dirname(os.path.abspath(__file__))
    gr_dir = os.path.join(py_dir, "test_results")

    if "01" in type:
        append_from_json(gr_dir)
    if "02" in type:
        append_from_txt(gr_dir)
    if "03" in type:
        append_from_xml(gr_dir)
    if "04" in type:
        append_from_xls(gr_dir)

    create_html(gr_dir, type)

def main():
    # arg = sys.argv
    # if arg[1] == 'none':
    #     print("please select a valid option from build parameters")
    # else:
    #     print("calling python script with: " + arg[1])
    #     create_report(arg[1])
    create_report("01")

if __name__ == "__main__":
    main()