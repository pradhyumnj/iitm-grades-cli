# iitm-grades-cli

**work in progress**

You'll still need an LDAP password to view grades, don't get ahead of yourself.   
Get your grades quickly from the command line without having to log in repeatedly.   

Usage:
1. Install the required librabries by running   
`pip install -r requirements.txt`
<br>
2. Login with your ldap credentials
`python grades.py login`   
<br>
3. View CGPA and Grades of the *latest sem*
`python grades.py show`   
<br>
4. You can logout (if you want to)   
`python grades.py logout`
