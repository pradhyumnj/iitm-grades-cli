from datetime import datetime
time = float(open('time.txt').read().strip('\n'))
if datetime.timestamp(datetime.now()) - time < 600:
    pass
else:

    import requests
    import warnings
    from bs4 import BeautifulSoup as bs
    warnings.filterwarnings("ignore")


    url = "https://www.iitm.ac.in/viewgrades/studentauth/login.php"
    with open("login_details.txt") as file:
        roll_no = file.readline().split(':')[1].strip("\n")
        pwd = file.readline().split(':')[1].strip("\n")
    data = {"rollno" : roll_no,
            "pwd" : pwd}
    with requests.Session() as s:
        website = s.post(url, data = data, verify = False)
        content = s.get("https://www.iitm.ac.in/viewgrades/studentauth/btechdual.php").text
    with open('content.txt', 'w') as file:
        file.write(content)

    with open('time.txt', 'w') as file:
        file.write(str(datetime.timestamp(datetime.now())))
    
    with open('login_details.txt', 'a') as file:
        soup = bs(content, "html5lib")
        name = soup.find_all("th")[2].text
        file.write(name)
