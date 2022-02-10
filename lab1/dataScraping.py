from bs4 import BeautifulSoup
from json import dump
import requests

BASE_URL = 'https://lnam.edu.ua/'
URL = f"{BASE_URL}uk/faculty.html"
result = requests.get(URL)
university = BeautifulSoup(result.content, "html.parser")
faculties = []
fac_list = university.find(class_='mod_article')


for facult in fac_list.find_all(class_='faculty'):
    facult_name = facult.figure.a['original-title']
    facult_url = facult.figure.a['href']
    faculty = {
        "name": facult_name,
        "url": facult_url,
        "departments": []
    }

    for depart in facult.find_all('li'):
        depart_url = BASE_URL + depart.a['href']
        depart_name = depart.a.getText()
        depart_res = requests.get(depart_url)
        department_page = BeautifulSoup(depart_res.content, "html.parser")
        staff_link = BASE_URL + \
            department_page.find('a', title="Колектив кафедри")['href']
        staff_res = requests.get(staff_link)
        staff_page = BeautifulSoup(staff_res.content, "html.parser")
        department = {
            "name": depart_name,
            "url": depart_url,
            "staff": []
        }
        for teacher in staff_page.find_all('h4'):
            department["staff"].append(teacher.a.getText())
        faculty["departments"].append(department)
    faculties.append(faculty)



with open("lnam.json", "w", encoding="utf-8") as json_file:
    dump(faculties, json_file, ensure_ascii=False, indent=4)
        


