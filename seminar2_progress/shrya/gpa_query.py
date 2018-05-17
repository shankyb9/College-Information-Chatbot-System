#import db
# import Project8
import keywords as K
import sqlite3
import random

conn = sqlite3.connect('db\\sqlite\\db\\pythonsqlite.db')

c = conn.cursor()

INVALID_UNAME_RES = ['Invalid username! Would you like to retry or have changed your mood?',
                     'Username does not exist! Would you like to retry or have changed your mood?',
                     'I suppose you forgot your username! Would you like to retry or have changed your mood?']
INVALID_PWD_RES = ['Invalid password! Would you like to retry or have changed your mood?',
                     'I suppose you forgot your password! Would you like to retry or have changed your mood?']

def printBot(msg):
    print(K.bot+msg)

def printUser(msg):
    print(K.user+msg)

def login(user=False):
    if(user==False):
        printBot("Provide username")
        user = input(K.user)
        
    c.execute('SELECT id from LOGIN WHERE email=?', [user])   
    pwd=""
#    print(c.fetchone())
    if(c.fetchone()):
        printBot("Provide password")
        pwd = input(K.user)
        c.execute('SELECT id from LOGIN WHERE email=? and pswd=?', [user, pwd])
        idn = c.fetchone()
#        print(idn)
        if(idn):
            print('Logged In Successfully')
            return idn
        else:
            print(random.choice(INVALID_PWD_RES))
            choice = input(K.user)
            if('retry' in choice and 'not' not in choice):
                return login(user)
            else:
                return None
    else:
        print(random.choice(INVALID_UNAME_RES))
        choice = input(K.user)
        if('retry' in choice and 'not' not in choice):
            return login()
        else:
            return None
    # printUser(K.user + inpt1)


def displayAllGPA(idn):
    c.execute('SELECT fname, sem_id from STUD_INFO where id = ?',  idn)
    fname, sem_id = c.fetchone()
    # set predicate name to fname in AIML
    
    # find the GPA accordingly
    query = 'SELECT * from GPA_DETAILS where id = ?'
#    print(query)
    c.execute(query,  idn)
    result = c.fetchall()[0][1:]
    res_list = {}
    count = 0
    for sgpa in result:
        count = count+1
        if(sgpa==0):
            break;
        res_list["Sem-"+str(count)] = sgpa
#    print(result)
    print("Your semester wise sgpa is as follows:",res_list)
    
    
def findGPA(idn):
    c.execute('SELECT fname, sem_id from STUD_INFO where id = ?',  idn)
    fname, sem_id = c.fetchone()
    # set predicate name to fname in AIML
    
    # find the GPA accordingly
#    query = 'SELECT sem'+str(sem_id)+' from GPA_DETAILS where id = ?'
    query = 'SELECT * from GPA_DETAILS where id = ?'
#    print(query)
    c.execute(query,  idn)
    result = c.fetchall()
#    print(result)
    findCGPA(result[0][1:])
    
def findCGPA(sgpa):
#    print(sgpa)
    cgpa = 0
    sem = 0
    for gpa in sgpa:
        cgpa+=gpa
        if(gpa!=0.0):
            sem= sem+1
    if(sem==0):
        sem=1
    cgpa/=sem
    print('Your CGPA is ',cgpa)

def findGPA_sem(idn, sem_id):
    c.execute('SELECT fname from STUD_INFO where id = ?',  idn)
    fname = c.fetchone()
    # set predicate name to fname in AIML
    
    # find the GPA accordingly
    sem = 'sem'+str(sem_id);
    query = 'SELECT '+sem+' from GPA_DETAILS where id = ?'
#    print(query)
    c.execute(query,  idn)
    result = c.fetchall()[0][0]
    print('Your SGPA of '+sem+ " is ", result)
    
def findGPA_current(idn):
    c.execute('SELECT fname, sem_id from STUD_INFO where id = ?',  idn)
    fname, sem_id = c.fetchone()
    # set predicate name to fname in AIML
    
    # find the GPA accordingly
    query = 'SELECT sem'+str(sem_id)+' from GPA_DETAILS where id = ?'
#    print(query)
    c.execute(query,  idn)
    result = c.fetchall()[0][0]
    if(result==0.0):
        print('Results are not out yet!!')
    else:
        print('Your current SGPA is ', result)

    
if(__name__=='__main__'):
    idn = login()
    if(idn!=None):
        findGPA(idn)
        findGPA_current(idn)
        displayAllGPA(idn)
        findGPA_sem(idn,2)
    else:
        printBot("Operation aborted")
