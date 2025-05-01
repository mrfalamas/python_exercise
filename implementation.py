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

def create_html(gr_dir, project, type):
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
            status = "NOK" if fail_rate > 0 else "OPEN" if open_rate > 0 else "OK"
            html_dict[module].append(f'{open_rate:.2f}' + "%")
            html_dict[module].append(f'{fail_rate:.2f}' + "%")
            html_dict[module].append(status)
    elif "03" in type or "04" in type:
        for module in html_dict:
            mod_checks = html_dict[module][0]
            mod_opens = html_dict[module][1]
            mod_fails = html_dict[module][2]
            open_rate = mod_opens*100 / mod_checks
            fail_rate = mod_fails*100 / mod_checks
            req_total = html_dict[module][3]
            req_opens = html_dict[module][4]
            req_fails = html_dict[module][5]
            req_op_rate = req_opens*100 / req_total
            req_fl_rate = req_fails*100 / req_total
            status = status = "NOK" if (fail_rate > 0 or req_fl_rate > 0) else "OPEN" if (open_rate > 0 or req_op_rate > 0) else "OK"
            html_dict[module].append(f'{open_rate:.2f}' + "%")
            html_dict[module].append(f'{fail_rate:.2f}' + "%")
            html_dict[module].append(f'{req_op_rate:.2f}' + "%")
            html_dict[module].append(f'{req_fl_rate:.2f}' + "%")
            html_dict[module].append(status)

    # Write HTML content
    file.write("<html>")
    file.write("<head>")
    file.write("<title>Test Results</title>")
    file.write("</head>")
    file.write("<body>")
    file.write("<h1><span style=\"font-size: 15px;\">&#128310; PROJECT&nbsp;&nbsp;</span><span style=\"color: #f8641a; font-size: 35px;\">" + project + "</span></h1>")
    file.write("<p> </p>")
    if "01" in type:
        file.write("<h2><span style=\"font-size: 14px;\">&#128311; ACTIVITY&nbsp;&nbsp;&nbsp;</span><span style=\"color: #0078c4; font-size: 25px;\">Review of Test Specification</span></h2>")
        file.write("<p> </p>")
        file.write("<p>&#128312; html report generated at <span style=\"color: #f8641a; font-size: 18px;\">" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "</span></h3>")
        file.write("<p>&#128313; readed from <span style=\"color: #0078c4; font-size: 18px;\">01_test_specification.JSON</span></p>")
    if "02" in type:
        file.write("<h2><span style=\"font-size: 14px;\">&#128311; ACTIVITY&nbsp;&nbsp;&nbsp;</span><span style=\"color: #0078c4; font-size: 25px;\">Review of Test Implementation</span></h2>")
        file.write("<p> </p>")
        file.write("<p>&#128312; html report generated at <span style=\"color: #f8641a; font-size: 18px;\">" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "</span></h3>")
        file.write("<p>&#128313; readed from <span style=\"color: #0078c4; font-size: 18px;\">02_test_implementation.TXT</span></p>")
    if "03" in type:
        file.write("<h2><span style=\"font-size: 14px;\">&#128311; ACTIVITY&nbsp;&nbsp;&nbsp;</span><span style=\"color: #0078c4; font-size: 25px;\">Non-Safety Tests (QM Requirements)</span></h2>")
        file.write("<p> </p>")
        file.write("<p>&#128312; html report generated at <span style=\"color: #f8641a; font-size: 18px;\">" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "</span></h3>")
        file.write("<p>&#128313; readed from <span style=\"color: #0078c4; font-size: 18px;\">03_test_qm_requirements.XML</span></p>")
    if "04" in type:
        file.write("<h2><span style=\"font-size: 14px;\">&#128311; ACTIVITY&nbsp;&nbsp;&nbsp;</span><span style=\"color: #0078c4; font-size: 25px;\">Safety Tests (ASIL Requirements)</span></h2>")
        file.write("<p> </p>")
        file.write("<p>&#128312; html report generated at <span style=\"color: #f8641a; font-size: 18px;\">" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "</span></h3>")
        file.write("<p>&#128313; readed from <span style=\"color: #0078c4; font-size: 18px;\">04_test_asil_requirements.XLSX</span></p>")
    file.write("<p> </p>")
    file.write("<table style=\"border:1px solid black; border-collapse: collapse; \">")
    file.write("<tr style=\"border:1px solid black; \">")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">Name</th>")
    if "01" in type or "02" in type:
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Checks</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Open</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Fails</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #d6eaf8;\">Open rate</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #fadbd8;\">Fail rate</th>")
    elif "03" in type or "04" in type:
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Tests</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Open</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Fails</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #d6eaf8;\">Open rate</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #fadbd8;\">Fail rate</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Requirements</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Not covered</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center;\">#Req. failed</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #85c1e9;\">Open rate</th>")
        file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #f1948a;\">Fail rate</th>")
    file.write("<th style=\"border:1px solid black; padding: 10px; text-align: center; \"><p>STATUS</th>")
    file.write("</tr>")
    if "01" in type or "02" in type:
        for row in html_dict:
            file.write("<tr style=\"border:1px solid black; \">")
            file.write("<td style=\"border:1px solid black; padding: 10px; \">" + str(row) + "</td>")
            for i, value in enumerate(html_dict[row]):
                if i == 3:
                    file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #d6eaf8;\">" + str(value) + "</td>")
                elif i == 4:
                    file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #fadbd8 ;\">" + str(value) + "</td>")
                elif i == 5:
                    if str(value) == "OK":
                        file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">&#9989;</td>")
                    elif str(value) == "OPEN":
                        file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">&#128260;</td>")
                    else:
                        file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; font-size: 14px;\">&#10060;</td>")
                else:
                    file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(value) + "</td>")
            file.write("</tr>")
    elif "03" in type or "04" in type:
        for row in html_dict:
            file.write("<tr style=\"border:1px solid black; \">")
            file.write("<td style=\"border:1px solid black; padding: 10px; \">" + str(row) + "</td>")
            #tests
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(html_dict[row][0]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(html_dict[row][1]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(html_dict[row][2]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #d6eaf8 ;\">" + str(html_dict[row][6]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #fadbd8 ;\">" + str(html_dict[row][7]) + "</td>")
            #reqs
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(html_dict[row][3]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(html_dict[row][4]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">" + str(html_dict[row][5]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #85c1e9 ;\">" + str(html_dict[row][8]) + "</td>")
            file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; background-color: #f1948a ;\">" + str(html_dict[row][9]) + "</td>")
            if str(html_dict[row][10]) == "OK":
                file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">&#9989;</td>")
            elif str(html_dict[row][10]) == "OPEN":
                file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center;\">&#128260;</td>")
            else:
                file.write("<td style=\"border:1px solid black; padding: 10px; text-align: center; font-size: 14px;\">&#10060;</td>")
            file.write("</tr>")
    file.write("</table>")
    file.write("</body>")
    file.write("</html>")

    # Close the file
    file.close()

    print("HTML file successfully written.")

def create_report(project, type):
    py_dir = os.path.dirname(os.path.abspath(__file__))
    gr_dir = os.path.join(py_dir, "test_results")

    if "01" in type:
        append_from_json(gr_dir, project)
    if "02" in type:
        append_from_txt(gr_dir, project)
    if "03" in type:
        append_from_xml(gr_dir, project)
    if "04" in type:
        append_from_xls(gr_dir, project)

    create_html(gr_dir, project, type)

def main():
    arg = sys.argv
    if arg[1] == 'none' or arg[2] == 'none':
        print("please select a valid option from build parameters")
    else:
        print("calling python script with project: " + arg[1] + " and test activity: " + arg[2])

    create_report(arg[1], arg[2])

if __name__ == "__main__":
    main()