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
    return None


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

def create_html(gr_dir, title):
    html_file = os.path.join(gr_dir, "output.html")
    file = open(html_file, "w")

    for keys in main_dict:
        no_rows = 0
        if no_rows < len(main_dict[keys]):
            no_rows = len(main_dict[keys])

    rows = {}
    rows[0] = []
    for keys in main_dict:
        rows[0].append(keys)
    for i in range (1, no_rows+1):
        rows[i] = []
        for keys in main_dict:
            try:
                rows[i].append(main_dict[keys][i-1])
            except:
                rows[i].append(0)

    # Write HTML content
    file.write("<html>")
    file.write("<head>")
    file.write("<title>CATALOG</title>")
    file.write("</head>")
    file.write("<body>")
    file.write(title)
    file.write("<p> </p>")
    file.write("<h2>generated at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "</h12>")
    file.write("<p> </p>")
    file.write("<table style=\"border:1px solid black; border-collapse: collapse; \">")
    for row in rows:
        file.write("<tr style=\"border:1px solid black; \">")
        for value in rows[row]:
            if row == 0:
                file.write("<th style=\"border:1px solid black; padding: 10px;\">" + str(value) + "</th>")
            else:
                file.write("<td style=\"border:1px solid black; padding: 10px;\">" + str(value) + "</td>")
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

    if type == "xml":
        append_from_xml(gr_dir)
        title = "<h1>HTML Report based Non-Safety Tests - XML</h1>"
    if type == "xls":
        append_from_xls(gr_dir)
        title = "<h1>HTML Report based on Safety Tests - XLS</h1>"
    if type == "txt":
        append_from_txt(gr_dir)
        title = "<h1>HTML Report based on Review Test Implementation - TXT</h1>"
    if type == "json":
        append_from_json(gr_dir)
        title = "<h1>CHTML Report based on Review Test Specification - JSON</h1>"

    create_html(gr_dir, title)

def main():
    # arg = sys.argv
    # if arg[1] == 'none':
    #     print("please select a valid option from build parameters")
    # else:
    #     print("calling python script with: " + arg[1])
    #     create_report(arg[1])
    create_report()

if __name__ == "__main__":
    main()