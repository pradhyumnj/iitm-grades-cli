import os
import requests
import typer
from datetime import datetime
app = typer.Typer()


@app.command()
def login():

    curr_dir = os.getcwd()
    logged_in = False


    if "login_details.txt" in os.listdir(curr_dir):
        with open("login_details.txt") as file:
            usr = file.readline().split(':')[1].strip("\n")
            logged_in = True
        print(f'User already logged in as {usr}')
        x = input(f"Do you want to login with new credentails? [y/n]: ")
        logged_in = x == 'n'

    if not logged_in:
        logout()
        roll_no = input("Enter your Roll number: ").lower()
        password = input("Enter your LDAP password: ")
        if not check_credentials(roll_no, password):
            print('Invalid credentials')
            exit()

        with open('login_details.txt' ,'w') as file:
            file.write(f'roll_no:{roll_no}\n')
            file.write(f'password:{password}')
        print('Logged in successfully')

def check_credentials(roll_no, pwd):
    import warnings
    warnings.filterwarnings("ignore")
    url = "https://www.iitm.ac.in/viewgrades/studentauth/login.php"
    data = {"rollno" : roll_no,
          "pwd" : pwd}
    with requests.Session() as s:
        website = s.post(url, data = data, verify = False)
        content = s.get("https://www.iitm.ac.in/viewgrades/studentauth/btechdual.php").text
        if len(content) < 500:
            return False
        with open('content.txt', 'w') as file:
            file.write(content)
        with open('time.txt', 'w') as file:
            file.write(str(datetime.timestamp(datetime.now())))
    return True

@app.command()
def show():
    import fetch
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    content = open("content.txt").read()
    soup = bs(content, 'html5lib')
    rows = []
    for row in soup.find_all('tr')[-12:-5]:
        rows.append(row)
    courses = rows[:-1]

    grades = []
    for course in courses:
        grades.append([data.text.strip(' ') for data in course.find_all('td')])
        
    df = pd.DataFrame(grades, columns = ["No.", "Code", "Course Title", "Course Category", "Credit", "Grade", "Att"])
    df.index = df['No.']
    df.drop(["No."],axis = 1, inplace = True)

    print(df)
    print('\t'.join([x.text.strip(' ') for x in rows[-1].find_all('td')]))
      
@app.command()
def logout():
    curr_dir = os.getcwd()
    if "login_details.txt" in os.listdir(curr_dir):
        os.remove(curr_dir + "/login_details.txt")
        os.remove(curr_dir + "/content.txt")
        os.remove(curr_dir + "/time.txt")
        print('Logged out successfully')


if __name__ == "__main__":
    app()
