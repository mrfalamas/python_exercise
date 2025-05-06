"""Python implementation for 1 project, all test activities"""
import os
import pandas as pd
import math
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import os.path

main_dict = {}

def append_from_json(gr_dir, project):
    json_file = os.path.join(gr_dir, project + "_01_review_test_spec.json")
    with open(json_file, 'r') as file:
        data = json.load(file)

    for key in data:
        module = key
        if module not in main_dict.keys():
            main_dict[module] = data[key]

def append_from_txt(gr_dir, project):
    txt_file = os.path.join(gr_dir, project + "_02_review_test_impl.txt")
    f = open(txt_file, "r")
    for line in f:
        module = line.split(':')[0]
        if module not in main_dict.keys():
            main_dict[module] = []
        results = line.split(':')[1]
        results = results.replace(" ", "")
        results = results.replace("\n", "")
        split_res = results.split(',')
        for res in split_res:
            main_dict[module].append(int(res))

def append_from_xml(gr_dir, project):
    xml_file = os.path.join(gr_dir, project + "_03_nonsafety_test.xml")
    tree = ET.parse(xml_file)
    modules = tree.findall("module")

    for module in modules:
        mod_name = module.find('name').text

        if mod_name not in main_dict.keys():
            main_dict[mod_name] = []

        results = module.find('results').text
        results = results.replace(" ", "")
        each_res = results.split(",")
        for res in each_res:
            main_dict[mod_name].append(int(res))

def append_from_xls(gr_dir, project):
    xls_file = os.path.join(gr_dir, project + "_04_safety_test.xlsx")
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

def create_excel(gr_dir, project):
    py_dir = os.path.dirname(os.path.abspath(__file__))
    tst_dir = os.path.join(py_dir, "test_results")
    tpsr_path = os.path.join(tst_dir, "output.xlsx")

    excel_dict = main_dict
    print(excel_dict)

def create_report(project):
    py_dir = os.path.dirname(os.path.abspath(__file__))
    gr_dir = os.path.join(py_dir, "test_results")

    append_from_json(gr_dir, project)
    append_from_txt(gr_dir, project)
    append_from_xml(gr_dir, project)
    append_from_xls(gr_dir, project)

    create_excel(gr_dir, project)

def main():
    arg = sys.argv
    if arg[1] == 'none':
        print("please select a valid option from build parameters")
    else:
        print("calling python script with project: " + arg[1])

    create_report(arg[1])

if __name__ == "__main__":
    main()