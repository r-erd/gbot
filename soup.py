from bs4 import BeautifulSoup
from locale import atof, setlocale, LC_NUMERIC
import hashlib

#def get_html_debug():
    #soup = BeautifulSoup(open("fsu.html"), "html5lib")
    #print(get_data(soup))



def clean_data(subjects):
    for subject in subjects:
        if subject[2] == "":
            subject[2] = "-"  #falls keine Note angegeben

    for subject in subjects:
        del subject[0] #entferne Prüfungsnummer
        del subject[1] #entferne Semestername

    return subjects


def get_hash(subjects):
    hashstring = ""
    for subject in subjects:
        for entry in subject:
            hashstring += entry

    return hashlib.sha256(hashstring.encode()).hexdigest()

def get_data(soup):
    setlocale(LC_NUMERIC, '')
    tables = soup.find_all("table", {"class": "FSUinfotable", "style" : "margin-bottom:0.0em;margin-top:0.0em;","width":"100%", "cellspacing": "0", "cellpadding": "2", "align": "left"})
    subjects = []
    for table in tables:

            for tbody in table.find_all("tbody"):
                exam_info = []
                for td in tbody.find_all("td"):
                        tdtext = td.get_text()
                        tdtext.strip()
                        if len(tdtext) != 0 and "Gruppe" not in tdtext and "FMI" not in tdtext:
                            exam_info.append(td.get_text().strip())
                

                subjects.append(exam_info[0:4])  #prüfnr : semester : titel : note

    return clean_data(subjects)

