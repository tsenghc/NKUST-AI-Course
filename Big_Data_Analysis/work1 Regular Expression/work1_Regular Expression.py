import re


import requests

# headers = {"cookie":"_ga=GA1.3.243265463.1616469635; _gid=GA1.3.1526699430.1616469635; _gat=1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"}
url_list = ["http://www.csie.kuas.edu.tw/teacher.php",
            "https://university.1111.com.tw/api/university/get_data.asp?apitype=teachers&type=2&pageshow=100&code=1000031203",
            "http://www.csie.ncku.edu.tw/ncku_csie/depmember/teacher",
            "https://www.nstm.gov.tw/Service/Volunteer/Ask/Contact.htm"]
for i in url_list:
    res = requests.get(i).text
    regex = '[a-zA-Z0-9_]+@[a-zA-Z0-9\._]+\.'
    find_email = re.findall(regex, res)
    print(len(find_email))
    print("----------")
