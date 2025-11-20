import sqlite3
import getpass
import re
import datetime
from datetime import date, timedelta
from tabulate import tabulate

def adapt_datetime_iso(val):
    return val.isoformat()

def convert_datetime_iso(val):
    return datetime.datetime.fromisoformat(val.decode('utf-8'))

sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
sqlite3.register_converter("TIMESTAMP", convert_datetime_iso)
sqlite3.register_converter("DATETIME", convert_datetime_iso)

conn = sqlite3.connect('LibraryMGMT.db')

cursor = conn.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS Users(
               UserId INTEGER PRIMARY KEY AUTOINCREMENT,
               Username VARCHAR(30) UNIQUE NOT NULL,
               EmailId VARCHAR(100),
               Contact INTEGER,
               Passwd VARCHAR(20) NOT NULL,
               Role VARCHAR(5),
               Status VARCHAR(5),
               Join_Dt TEXT,
               End_Dt TEXT
               )
               ''')


cursor.execute(''' CREATE TABLE IF NOT EXISTS Books(
               Bk_Id INTEGER PRIMARY KEY AUTOINCREMENT,
               Bk_Name VARCHAR(50) NOT NULL,
               Bk_Category VARCHAR(100),
               Bk_Author VARCHAR(30),
               Bk_Add_Dt TEXT,
               Bk_Status VARCHAR(5),
               Bk_Stock INTEGER

               )
               ''')


cursor.execute(''' CREATE TABLE IF NOT EXISTS BooksLog(
               Log_Id INTEGER PRIMARY KEY AUTOINCREMENT,
               Bk_Id INTEGER,
               UserId INTEGER,
               Rent_Dt TEXT,
               Return_Dt TEXT,
               Retn_Status VARCHAR(5),
               Rent_Amt INTEGER,
               FOREIGN KEY (Bk_Id) references Books(Bk_Id),
               FOREIGN KEY (UserId) references Users(UserId)
               
               )
               ''')


cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transact(
               	Trn_Id INTEGER PRIMARY KEY AUTOINCREMENT,
	            Log_Id INTEGER DEFAULT NULL,
	            UserId INTEGER,
	            Trn_Desc VARCHAR(250),
	            Amt_Paid INTEGER,
                Trn_Dt TEXT,
                FOREIGN KEY (Log_Id) references BooksLog(Log_Id),
                FOREIGN KEY (UserId) references Users(UserId)
                )
               ''')

class Login:
    def __init__(self):
        conn = sqlite3.connect('LibraryMGMT.db')
        self.cursor = conn.cursor()

    def login(self,choice):
        cursor.execute('''SELECT * from Users''')
        users = cursor.fetchall()
        id = choice
        if not users and choice == 1:
            lib = Library(id)
            lib.register(id)

        elif not users and choice == 2:
            print('\n 💡 First login should be the Librarian!!! 💡')

        elif len(users) == 1 and choice == 2:
            print('\n ❌ Please contact the Librarian to Register!!! ❌')

        else:
            opt='y'
            while opt == 'y':
                print('\n===============Login==============\n')
                uname = input('Username = ')
                paswd = getpass.getpass('Password = ')

                cursor.execute(''' SELECT UserId, Role from Users where Username = ? AND Passwd = ?''', (uname,paswd))
                user = cursor.fetchone()
                if not user:
                    print('\nIncorrect Username or Password!!!\n')
                    rst = input('Do you want to reset your password? (y/n): ')
                    if rst == 'y':
                        paspat = r'[a-zA-Z0-9_.#$%@]+'
                        uname = input('\nEnter your Username: ')
                        pd = getpass.getpass('Enter the new Password to update: ')
                        cursor.execute('''SELECT UserId FROM Users WHERE Username = ?''',(uname,))
                        usid = cursor.fetchone()
                        uid = usid[0]

                        if re.search(paspat,pd):
                            cursor.execute('''UPDATE Users SET Passwd = ? WHERE UserId = ?''',(pd,uid))
                            conn.commit()
                            print('\n✅ Successfully updated your Password!!')
                            pass
                        else:
                            print('💡 Please include small letters,capital letters, numbers and special characters!!!')
                    elif rst == 'n':
                        pass

                else:
                    id = user[0]
                    rl = user[1]
                    lb = Library(id)
                    mb = Member(id)
                    if id and rl == 'L':
                        logout = lb.libmenu(id)
                        return logout
                    elif id and rl == 'M':
                        logout = mb.membermenu(id)
                        return logout
                    else:
                        print('\n❌ You are not authorized to Login, please reach out to Library Admin!!!')
                        break

            opt = input('\nDo you want to login again? (y/n):')

class Library:
    def __init__(self,id):
        conn = sqlite3.connect('LibraryMGMT.db')
        self.cursor = conn.cursor()
        id = id
    
    def libmenu(self,id):

        print('\n=========================')
        print('👩‍🏫 Welcome Librarian!!! 👩‍🏫')
        print('=========================')
        print()
        opt = 'y'
        while opt == 'y':
            try:
                print('\n===================📚 Welcome to Library Functions 📚=================')
                print('\n1.Register a User\n2.User Module\n3.Book Module\n4.Book Issued Details\n5.Transaction Details\n6.Quick Functions\n7.Logout\n')
                ch = int(input('Enter your choice: '))
                if ch == 1:
                    self.register(id)
                elif ch == 2:
                    self.users(id)
                elif ch == 3:
                    self.books(id)
                elif ch == 4:
                    self.booklogs(id)
                elif ch == 5:
                    self.transtn(id)
                elif ch == 6:
                    self.quickfunc(id)
                elif ch == 7:
                    break
                else:
                    print('\n❌ Wrong Choice!!!, Please check the input value!!!')
                
            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the input value!!!')

    def register(self,id):

        print('\n======✍️ Register a User!!!======')
        print()
        empat = r'[a-z][a-zA-Z0-9_.#$%]+@[a-zA-Z]+.[a-zA-Z]+'
        nopat = r'[0-9]{10}'
        paspat = r'[a-zA-Z0-9_.#$%@]+'

        while True:
            uname = input('Enter your Name: ')
            if not uname:
                print('💡 Please enter the Username!!!')
            else:
                break
        
        while True:
            emailid = input('Enter your Email Id: ')
            if not re.search(empat,emailid):
                print('\n❌ Not a valid Email!!')
            else:
                break

        while True:
            cont = input('Enter your Mobile No: ')
            if not re.search(nopat,cont):
                print('\n❌ Not a valid phone number!!')
            else:
                contact = int(cont)
                break

        while True:
            passwd = getpass.getpass('Enter your Password: ')
            if not re.search(paspat,passwd):
                print('\n💡 Please include small letters,capital letters, numbers and special characters!!!')
            else:
                break
    
        print('\n🧑‍🤝‍🧑 Members will get additional privileges like login facility, search books, first priority etc')
        print('\n💡💡 Note: If registering for a Librarian, give \'L\' as input 💡💡')
        rl = input('\n💵 Do you want to become a member by paying 1000 rupees?(y/n): ')
        if rl == 'y':
            role = 'M'
        elif rl == 'L':
            role = 'L'
        else:
            role = 'U'

        dt = date.today()
        yr = dt + timedelta(days = 365)
        stats = 'A'

        cursor.execute('''INSERT INTO Users(Username,EmailId,Contact,Passwd,Role,Status,Join_Dt,End_Dt) 
              VALUES(?,?,?,?,?,?,?,?)''',(uname,emailid,contact,passwd,role,stats,dt,yr))
        conn.commit()

        if role == 'M':
            cursor.execute('''SELECT MAX(UserId) from Users''')
            uid = cursor.fetchone()
            usrid = uid[0]
            if not usrid:
                print('\n👎 UserId not returned!!')
            else:

                trndesc = 'Amount paid for Library membership.'
                amt = 1000
                cursor.execute('''INSERT INTO Transact(UserId,Trn_Desc,Amt_Paid,Trn_Dt) VALUES(?,?,?,?)''',(usrid,trndesc,amt,dt))

        conn.commit()
        print('\n✅ Successfully Registered the User !!! ✅')

    def users(self,id):

        opt = 'y'
        while opt == 'y':
            try:
                print('\n=============🧑‍🤝‍🧑 Welcome to User Module 🧑‍🤝‍🧑============')
                print('\n1.View Users\n2.Edit a User\n3.Delete a User\n4.Find the User\n5.Return to Main Menu\n')
                ch = int(input('Enter your choice: '))

                if ch == 1:
                    # view_user()
                    cursor.execute('''SELECT * FROM Users''')
                    6

                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n👎 No Data Found!!!')
                    else:
                        print('\nUser Details')
                        print('===============')
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 2:

                    print('\nUpdate User Details!!!')
                    print('=========================')
                    empat = r'[a-z][a-zA-Z0-9_.#$%]+@[a-zA-Z]+.[a-zA-Z]+'
                    nopat = r'[0-9]{10}'
                    paspat = r'[a-zA-Z0-9_.#$%@]+'
                    Id = int(input('\nEnter the User Id to Edit: '))
                    optn = 'y'
                    while optn == 'y':
                        detail = input('\nEnter the field to update(email,contact,password,role): ').lower()

                        if detail == 'email':
                            em = input('\nEnter the new email id to be updated: ')
                            if re.search(empat,em):
                                cursor.execute('''UPDATE Users SET EmailId = ? WHERE UserId = ?''',(em,Id))
                                print('\n✅ Successfully updated the User Email ID!!!')
                                # conn.commit()
                                pass
                            else:
                                print('\n❌ Not a valid Email!!')

                        elif detail == 'contact':
                            cn = input('Enter the new contact to be updated: ')
                            if re.search(nopat,cn):
                                cursor.execute('''UPDATE Users SET Contact = ? WHERE UserId = ?''',(cn,Id))
                                # conn.commit()
                                print('\n✅ Successfully updated the User Contact!!!')
                                pass
                            else:
                                print('\n❌ Not a valid phone number!!')
                                
                        elif detail == 'password':
                            
                            pd = getpass.getpass('Enter your Password: ')
                            if re.search(paspat,pd):
                                cursor.execute('''UPDATE Users SET Passwd = ? WHERE UserId = ?''',(pd,Id))
                                # conn.commit()
                                print('\n✅ Successfully updated the User Password!!!')
                                pass
                            else:
                                print('💡 Please include small letters,capital letters, numbers and special characters!!!')
        
                        elif detail == 'role':
                            cursor.execute('''SELECT Role FROM Users WHERE UserId = ?''',(id,))
                            usrrl = cursor.fetchone()
                            userol = usrrl[0]
                            if userol == 'U' or userol != 'M' or userol != 'L':
                                print('\n🧑‍🤝‍🧑 Members will get additional privileges like login facility, search books, first priority etc')
                                rl = input('\n💵 Are you ready to pay 1000 rupees for Library Membership? (y/n): ')
                                if rl == 'y':
                                    role = 'M'
                                    cursor.execute('''UPDATE Users SET Role = ? WHERE UserId = ?''',(role,Id))
                                    dt = date.today()
                                    trndesc = 'Amount paid for Library membership.'
                                    amt = 1000
                                    cursor.execute('''INSERT INTO Transact(UserId,Trn_Desc,Amt_Paid,Trn_Dt) VALUES(?,?,?,?)''',(Id,trndesc,amt,dt))

                                    print('\n✅ Successfully updated the User Role!!!')
                                else:
                                    print('\nYou are already a Member!!! 👍')
                                    pass

                            else: 
                                print('\nYou are already a Member or Librarian!!! 👍')

                        else:
                            print('\n❌ Not a valid field!!!')
                        
                        conn.commit()
                        optn = input('\nDo you want to edit more fields (y/n) ❓: ')

                elif ch == 3:
                    
                    print('\nDelete User Details!!!')
                    print('======================')
                    Id = int(input('\nEnter the User Id to Delete: '))
                    pf = input('Are you sure you want to delete this User?(y/n): ').lower()
                    if pf == 'y':
                        cursor.execute('''DELETE from Users WHERE UserId = ?''',(Id,))
                        print('\n✅ Successfully Removed the User Details!!!')
                    else:
                        print('\n🙌 You are saved, User details are not Removed!!!')
                    conn.commit()   

                elif ch == 4:
                    
                    print('\n\nFind a User!!!')
                    print('===============')
                    Id = int(input('\nEnter the User Id to Find: '))
                    cursor.execute('''SELECT * from Users WHERE UserId = ?''',(Id,))

                    detls = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not detls:
                        print('\n👎 No Data Found!!!')
                    else:
                        print(tabulate(detls,headers=cols,tablefmt='grid'))

                elif ch == 5:
                    break
                
                else:
                    print('\n❌ Wrong Choice!!!')

            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check your input value!!!')

    def books(self,id):
        
        opt = 'y'
        while opt == 'y':
            try:
                print('\n================📚 Welcome to Books Module 📚================')
                print('\n1.Add Books\n2.View Books\n3.Edit a Book\n4.Delete a Book\n5.Find the Books\n6.Return to Main Menu')
                ch = int(input('\nEnter your choice: '))

                if ch == 1:
                    print('\n Add a Book!!!')
                    print('=================\n')
                    
                    while True:
                        bname = input('Enter the Book Name: ')
                        if not bname:
                            print('\n💡 Please enter the Book Name!!!')
                        else:
                            break

                    bcat = input('Enter the Book Category: ')
                    bauth = input('Enter the Author Name: ')
                    bstk = input('Enter the Book Stock available: ')

                    bdt = date.today()
                    stats = 'A'

                    cursor.execute('''INSERT INTO Books(Bk_Name,Bk_Category,Bk_Author,Bk_Add_Dt,Bk_Status,Bk_Stock) 
                        VALUES(?,?,?,?,?,?)''',(bname,bcat,bauth,bdt,stats,bstk))
                    
                    conn.commit()
                    
                    print('\n✅ Successfully Added the Book !!!')

                elif ch == 2:
                    self.booklst(id)

                elif ch == 3:

                    print('\nUpdate Books Details!!!')
                    print('========================')
                    Id = int(input('\nEnter the Book Id to Edit: '))
                    optn = 'y'
                    while optn == 'y':
                        detail = input('\nEnter the field to update(name,category,author,date,stock): ').lower()

                        if detail == 'name':
                            nm = input('Enter the book name to be updated: ')
                            cursor.execute('''UPDATE Books SET Bk_name = ? WHERE Bk_Id = ?''',(nm,Id))
                            print('\n✅ Successfully updated the Book Name!!!')
                            pass
                        elif detail == 'category':
                            ct = input('Enter the new category to be updated: ')
                            cursor.execute('''UPDATE Books SET Bk_Category = ? WHERE Bk_Id = ?''',(ct,Id))
                            print('\n✅ Successfully updated the Book Category!!!')
                            pass                        
                        elif detail == 'author':
                            au = input('Enter the author details or names: ')
                            cursor.execute('''UPDATE Books SET Bk_Author = ? WHERE Bk_Id = ?''',(au,Id))
                            print('\n✅ Successfully updated the Author Name!!!')
                            pass    
                        elif detail == 'date':
                            dt = input('Enter the new Date: ')
                            cursor.execute('''UPDATE Books SET Bk_Add_Dt = ? WHERE Bk_Id = ?''',(dt,Id))
                            print('\n✅ Successfully updated the Book Added Date!!!')
                            pass
                        elif detail == 'stock':
                            st = input('Enter the stock: ')
                            cursor.execute('''UPDATE Books SET Bk_Stock = ? WHERE Bk_Id = ?''',(st,Id))
                            print('\n✅ Successfully updated the Stock!!!')
                            pass
                        else:
                            print('\n❌ Not a valid field!!!')
                        
                        optn = input('\nDo you want to edit any other fields(y/n): ❓')    

                        conn.commit()

                elif ch == 4:
                    
                    print('\nDelete Books!!!')
                    print('==================')
                    Id = int(input('\nEnter the Book Id to Delete: '))
                    pf = input('\nAre you sure you want to delete this Book?(y/n): ').lower()
                    if pf == 'y':
                        cursor.execute('''DELETE from Books WHERE Bk_Id = ?''',(Id,))
                        print('\n✅ Successfully Removed the Book!!!')
                    else:
                        print('\n🙌 You are saved, book details not Removed!!')

                    conn.commit()      

                elif ch == 5:
                    self.findbooks(id)

                elif ch == 6:
                    break
                
                else:
                    print('\n❌ Wrong Choice!!!')   

            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the input value!!!')

    def findbooks(self,id):
        print('\nFind the Books!!!')
        print('====================')
        dets = input('\n💡 How you want to find the Book, with Id, Name, Category or Author : ').lower()
                
        if dets == 'id':

            Id = int(input('Enter the Book Id to find the book: '))
            cursor.execute('''SELECT * from Books WHERE Bk_Id = ?''',(Id,))

        elif dets == 'name':

            nm = input('Enter the Book Name to find the book: ')
            search_txt = f"%{nm}%"
            cursor.execute('''SELECT * from Books WHERE Bk_Name LIKE ?''',(search_txt,))

        elif dets == 'category':
                    
            ct = input('Enter the Book Category to find the book: ')
            search_txt = f"%{ct}%"
            cursor.execute('''SELECT * from Books WHERE Bk_Category LIKE ?''',(search_txt,))
                
        elif dets == 'author':
                    
            au = input('Enter the Book Author to find the book: ')
            search_txt = f"%{au}%"
            cursor.execute('''SELECT * from Books WHERE Bk_Author LIKE ?''',(search_txt,))
        
        else:
            print('\n❌ Not a valid entry, please check the field!!!')

        detls = cursor.fetchall()
        cols = [description[0] for description in cursor.description]

        if not detls:
            print('\n👎 No Data Found!!!')
        else:
            print(tabulate(detls,headers=cols,tablefmt='grid'))

    def booklst(self,id):
                    
        print('\nFull List of Books!!!')
        print('========================\n')
        cursor.execute('''SELECT * FROM Books''')
        alldata = cursor.fetchall()

        cols = [description[0] for description in cursor.description]

        if not alldata:
            print('\n👎 No Data Found!!!')
        else:
            print(tabulate(alldata,headers=cols,tablefmt='grid'))    

    def booklogs(self,id):
        opt = 'y'
        while opt == 'y':
            try:
                print('\n=================Welcome to Books Log Module===============')
                print('\n1.Add Book Issue Log\n2.View Book Logs\n3.Edit a Log Entry\n4.Delete a Log Entry\n5.Find the Logs\n6.Return to Main Menu\n')
                ch = int(input('Enter your choice: '))

                if ch == 1:

                    print('\nBook Log Entry')
                    print('=================')

                    bkid = int(input('\nEnter the Book Id: '))
                    uid = int(input('Enter the User Id: '))
                    rentamt = int(input('Enter the Rent Amount: '))
                    stats = 'Issued'

                    rntdt = date.today()
                    retdt = rntdt + timedelta(days = 30)

                    cursor.execute('''INSERT INTO BooksLog(Bk_Id,UserId,Rent_Dt,Return_Dt,Retn_Status,Rent_Amt) 
                        VALUES(?,?,?,?,?,?)''',(bkid,uid,rntdt,retdt,stats,rentamt))
                    
                    conn.commit()
                    
                    print('\n✅ Successfully Added the Log !!!\n')

                elif ch == 2:
                    
                    print('\nView Books Log Details')
                    print('========================\n')
                    cursor.execute('''SELECT * FROM BooksLog''')
                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n👎 No Data Found!!!')
                    else:
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 3:
                    
                    print('\nUpdate Books Log Details!!!')
                    print('===========================')
                    Id = int(input('\nEnter the Log Id to Edit: '))
                    optn = 'y'
                    while optn == 'y':
                        detail = input('\nEnter the field to update(status,amount): ').lower()

                        if detail == 'status':
                            st = input('\nEnter the Log Status to be updated: ').lower()
                            cursor.execute('''UPDATE BooksLog SET Retn_Status = ? WHERE Log_Id = ?''',(st,Id))
                            print('\n✅ Successfully updated the Status!!!')
                            conn.commit()

                            if st == 'returned':
                                cursor.execute('''SELECT UserId, Rent_Amt FROM BooksLog WHERE Log_Id = ?''',(Id,))
                                det = cursor.fetchone()
                                det1 = det[0]
                                det2 = det[1]
                                dt = date.today()
                                desc = 'Book rent amount paid after returning the Book'
                                cursor.execute('''INSERT INTO Transact(Log_Id,UserId,Trn_Desc,Amt_Paid,Trn_Dt) VALUES(?,?,?,?,?)''',(Id,det1,desc,det2,dt))

                                conn.commit()
                            else:
                                pass

                        elif detail == 'amount':
                            am = input('\nEnter the amount to be updated: ')
                            cursor.execute('''UPDATE BooksLog SET Rent_Amt = ? WHERE Log_Id = ?''',(am,Id))
                            print('\n✅ Successfully updated the Amount!!!')

                            conn.commit()

                            if am != 50 and st != 'returned':
                                pass

                            elif am !=50 and st == 'returned':

                                cursor.execute('''SELECT UserId, Rent_Amt FROM BooksLog WHERE Log_Id = ?''',(Id,))
                                det = cursor.fetchone()
                                det1 = det[0]
                                det2 = det[1]
                                dt = date.today()
                                desc = 'Book rent amount paid after returning the Book'
                                cursor.execute('''UPDATE Transact SET Amt_Paid = ? WHERE Log_Id = ? AND UserId = ?''', (am,Id,det1))

                                conn.commit()

                            else:
                                pass

                        else:
                            print('\n❌ Not a valid field!!!')

                        optn = input('\nDo you want to edit any other fields(y/n)❓:')    

                        conn.commit()
                        
                elif ch == 4:

                    print('\nDelete Book Logs!!!')
                    print('=====================\n')
                    Id = int(input('Enter the Log Id to Delete: '))
                    pf = input('\nAre you sure you want to delete this Log?(y/n): ').lower()
                    if pf == 'y':
                        cursor.execute('''DELETE from BooksLog WHERE Log_Id = ?''',(Id,))
                        print('\n✅ Successfully Removed the Log Entry!!!')
                    else:
                        print('\n🙌 You are saved!, Log Entry not Removed!!')

                    conn.commit()      

                elif ch == 5:
                    
                    print('\nFind the Logs!!!')
                    print('==================')
                    optn = 'y'
                    while optn == 'y':
                        dets = input('\n💡 How you want to find the Log, with LogId, UserId, or BookId : ').lower()
                        
                        if dets == 'logid':

                            lid = int(input('Enter the Log Id to find the entry: '))
                            cursor.execute('''SELECT * from BooksLog WHERE Log_Id = ?''',(lid,))
                            pass

                        elif dets == 'userid':

                            uid = int(input('Enter the User Id to find the entry: '))
                            cursor.execute('''SELECT * from BooksLog WHERE UserId = ?''',(uid,))
                            pass

                        elif dets == 'bookid':
                            
                            bid = int(input('Enter the Book Id to find the book: '))
                            cursor.execute('''SELECT * from BooksLog WHERE Bk_Id = ?''',(bid,))
                            pass
                        
                        else:
                            print('\n❌ Not a valid field!!!')

                        detls = cursor.fetchall()
                        cols = [description[0] for description in cursor.description]

                        if not detls:
                            print('\n👎 No Data Found!!!')
                        else:

                            print(tabulate(detls,headers=cols,tablefmt='grid'))

                        optn = input('\nDo you want to continue to find other logs? (y/n)❓: ')

                elif ch == 6:
                    break

                else:
                    print('\n❌ Wrong Choice!!')
            
            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the input value!!!')

        # opt = input('\nDo you want to continue?(y/n): ')

    def transtn(self,id):
        opt = 'y'
        while opt == 'y':
            try:

                print('\n==================Welcome to Transaction Module===================')
                print('\n1.Add a Transaction\n2.View Transactions\n3.Edit a Transaction Entry\n4.Find the Transactions\n5.Return to Main Menu\n')
                ch = int(input('Enter your choice: '))

                if ch == 1:

                    print('\nAdd a Transaction')
                    print('====================')

                    lid = input('\nEnter the Log Id: ')
                    uid = input('Enter the User Id: ')
                    desc = input('Enter the Transaction Description: ')
                    amtpd = input('Enter the Amount Paid: ')
                    trndt = date.today()


                    cursor.execute('''INSERT INTO Transact(Log_Id,UserId,Trn_Desc,Amt_Paid,Trn_Dt) 
                        VALUES(?,?,?,?,?)''',(lid,uid,desc,amtpd,trndt))
                    
                    conn.commit()
                    
                    print('\n✅ Successfully Added the Transaction !!!\n')

                elif ch == 2:
                    
                    print('\nView Transaction Details')
                    print('==========================\n')
                    cursor.execute('''SELECT * FROM Transact''')
                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n👎 No Data Found!!!')
                    else:
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 3:

                    print('\nUpdate Transaction Details!!!')
                    print('================================')
                    Id = int(input('\nEnter the Transaction Id to Edit: '))
                    optn = 'y'
                    while optn == 'y':
                        detail = input('\nEnter the field to update(description,amount): ').lower()

                        if detail == 'description':
                            desc = input('Enter the Transaction Description to be updated: ')
                            cursor.execute('''UPDATE Transact SET Trn_Desc = ? WHERE Trn_Id = ?''',(desc,Id))
                            print('\n✅ Successfully updated the Description!!!')

                        elif detail == 'amount':
                            amt = input('Enter the amount to be updated: ')
                            cursor.execute('''UPDATE Transact SET Amt_Paid = ? WHERE Trn_Id = ?''',(amt,Id))
                            print('\n✅ Successfully updated the Amount!!!')
                        else:
                            print('\n❌ Not a valid field!!!')
                        
                        optn = input('\nDo you want to edit any other fields(y/n)❓:')    

                        conn.commit()

                elif ch == 4:

                    print('\nFind the Transactions!!')
                    print('=========================')

                    optn = 'y'
                    while optn == 'y':
                        dets = input('\n💡 How you want to find the Transaction, with Trn_Id, Log_Id or UserId : ').lower()
                        
                        if dets == 'trn_id':

                            tid = int(input('Enter the Transaction Id to find the entry: '))
                            cursor.execute('''SELECT * from Transact WHERE Trn_Id = ?''',(tid,))
                            pass

                        elif dets == 'log_id':

                            lid = int(input('Enter the Log Id to find the entry: '))
                            cursor.execute('''SELECT * from Transact WHERE Log_Id = ?''',(lid,))
                            pass

                        elif dets == 'userid':
                            
                            uid = int(input('Enter the User Id to find the entry: '))
                            cursor.execute('''SELECT * from Transact WHERE UserId = ?''',(uid,))
                            pass
                        
                        else:
                            print('\n❌ Not a valid field!!!')

                        detls = cursor.fetchall()
                        cols = [description[0] for description in cursor.description]

                        if not detls:
                            print('\n👎 No Data Found!!!')
                        else:
                            print('\nTransaction Details')
                            print('=======================\n')
                            print(tabulate(detls,headers=cols,tablefmt='grid'))
                            
                            optn = input('\nDo you want to continue to find other Transaction? (y/n)❓: ')

                elif ch == 5:
                    break
                
                else:
                    print('\n❌ Wrong Choice!!!')
                    
            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the input value!!!')   
   
    def quickfunc(self,id):
        
        opt = 'y'
        while opt == 'y':
            try:

                print('\n⏩ Quick Functions!!! ⏪')
                print('=====================')
                print('\n 1. Find the users details who has rented the books \n 2. Find the users details who has return date tomorrow \n 3. Find the users who has not returned the Book/s  \n 4. Find the books which are out of stock\n 5. Return to Main Menu')
                ch = int(input('\nEnter your choice: '))
                if ch == 1:
                    cursor.execute('''SELECT ur.UserId, ur.Username, bl.Bk_Id, bl.Rent_Dt FROM Users ur
                                INNER JOIN BooksLog bl 
                                ON ur.UserId = bl.UserId WHERE Retn_Status = 'Issued' ''')
                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n👎 No Data Found!!!')
                    else:
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 2:
                    dt = date.today()
                    rtdt = dt + timedelta(days = 1)
                    cursor.execute('''SELECT ur.UserId, ur.Username, bl.Bk_Id, bl.Rent_Dt FROM Users ur
                                INNER JOIN BooksLog bl 
                                ON ur.UserId = bl.UserId  WHERE Return_Dt = ? ''',(rtdt,))
                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n👎 No Data Found!!!')
                    else:
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 3:
                    dt = date.today()
                    cursor.execute('''SELECT ur.UserId, ur.Username, bl.Bk_Id, bl.Rent_Dt, bl.Retn_Status FROM Users ur
                                INNER JOIN BooksLog bl 
                                ON ur.UserId = bl.UserId WHERE Return_Dt < ?''',(dt,))
                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n👎 No Data Found!!!')
                    else:
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 4:
                    
                    cursor.execute('''SELECT * FROM Books WHERE Bk_Stock = 0''')
                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n👎 No Data Found!!!')
                    else:
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 5:
                    break

                else:
                    print('\n❌ Wrong Choice !!!')

            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the input value!!!')

class Member(Library):

    def __init__(self,id):
        conn = sqlite3.connect('LibraryMGMT.db')
        self.cursor = conn.cursor()
        self.uid = id

    def membermenu(self,uid):

        print('\n=========================')
        print('😃 Welcome Member!!! 😃')
        print('=========================')
        print()
        opt = 'y'
        while opt == 'y':
            try:
                print('\n=====================📚 Welcome to A to Z Library 📚===================')
                print('\n1.Your Account\n2.Library Books\n3.Book Issued Details\n4.Transaction Details\n5.Logout\n')
                ch = int(input('Enter your choice: - '))

                if ch == 1:
                    self.account(uid)
                elif ch == 2:
                    self.books(uid)
                elif ch == 3:
                    self.booklogs(uid)
                elif ch == 4:
                    self.transtn(uid)
                elif ch == 5:
                    return 'You are logged out!!!'
                else:
                    break

            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the value!!!')

    
    def account(self,uid):

        opt = 'y'
        while opt == 'y':
            try:
                print('\nYour Account Details')
                print('======================')
                print('\n1.View Account Details\n2.Update Account Details\n3.Return to Main Menu\n')
                ch = int(input('Enter your choice: '))
                if ch == 1:
                    print('\nYour Details')
                    print('===============')
                    cursor.execute('''SELECT * FROM Users WHERE UserId = ?''', (uid,))
                    alldata = cursor.fetchall()

                    cols = [description[0] for description in cursor.description]

                    if not alldata:
                        print('\n❌ No Data Found!!!')
                    else:
                        print(tabulate(alldata,headers=cols,tablefmt='grid'))

                elif ch == 2:
                    print('\nUpdate Account Details !!!')
                    print('==========================\n')
                    empat = r'[a-z][a-zA-Z0-9_.#$%]+@[a-zA-Z]+.[a-zA-Z]+'
                    nopat = r'[0-9]{10}'
                    paspat = r'[a-zA-Z0-9_.#$%@]+'
                    
                    optn = 'y'
                    while optn == 'y':
                        detail = input('\nEnter the field to update(email,contact,password): ').lower()

                        if detail == 'email':
                            em = input('\nEnter the new email id to be updated: ')
                            if re.search(empat,em):
                                cursor.execute('''UPDATE Users SET EmailId = ? WHERE UserId = ?''',(em,uid))
                                conn.commit()
                                print('\n✅ Successfully updated the your Email ID!!')
                                pass
                            else:
                                print('\n❌ Not a valid Email!!')

                        elif detail == 'contact':
                            cn = input('\nEnter the new contact to be updated: ')
                            if re.search(nopat,cn):
                                cursor.execute('''UPDATE Users SET Contact = ? WHERE UserId = ?''',(cn,uid))
                                conn.commit()
                                print('\n✅ Successfully updated the your Contact!!')
                                pass
                            else:
                                print('\n❌ Not a valid phone number!!')
                                    
                        elif detail == 'password':
                                
                            pd = getpass.getpass('Enter your Password: ')
                            if re.search(paspat,pd):
                                cursor.execute('''UPDATE Users SET Passwd = ? WHERE UserId = ?''',(pd,uid))
                                conn.commit()
                                print('\n✅ Successfully updated the your Password!!')
                                pass
                            else:
                                print('\n💡 Please include small letters,capital letters, numbers and special characters!!!')
                        else:
                            print('\n❌ Not a valid field!!!')
                            
                        conn.commit()
                        optn = input('\nDo you want to edit more fields (y/n)❓: ')    
                elif ch == 3:
                    break

                else:
                    print('\n❌ Wrong Choice!!!')

            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the input value!!!')

    def books(self,uid):

        opt = 'y'
        while opt == 'y':
            try:
                print('\n================Welcome to Books Module==============')
                print('\n1.View Books\n2.Find the Books\n3.Return to Main Menu\n')
                ch = int(input('Enter your choice: '))

                if ch == 1:
                     super().booklst(uid)
                elif ch == 2:
                    
                     super().findbooks(uid)
                elif ch == 3:
                    break

                else:
                    print('\n❌ Wrong Choice!!')

            except Exception as er:
                print('\n❌ Wrong Choice!!!, Please check the input value!!!')

    
    def booklogs(self, uid):
        
        print('\nView Books Log Details')
        print('=========================\n')
        cursor.execute('''SELECT * FROM BooksLog WHERE UserId = ?''',(uid,))
        alldata = cursor.fetchall()

        cols = [description[0] for description in cursor.description]

        if not alldata:
            print('\n👎 No Data Found!!!')
        else:
            print(tabulate(alldata,headers=cols,tablefmt='grid'))

        conn.commit()
        
    def transtn(self,uid):
                
            print('\nView Transaction Details')
            print('==========================\n')
            cursor.execute('''SELECT * FROM Transact WHERE UserId = ?''',(uid,))
            alldata = cursor.fetchall()

            cols = [description[0] for description in cursor.description]

            if not alldata:
                print('\n👎 No Data Found!!!')
            else:
                print(tabulate(alldata,headers=cols,tablefmt='grid'))


def main():

    lg = Login()
    while True:
    
        try:
            print('\n================================================')
            print('📚 Welcome to A - Z Library Management System!!! 📚')
            print('================================================')
            print()
            print('1.Librarian Login\n2.Member Login\n3.Close\n')
            ch = int(input('Enter your choice: '))
            if ch == 1:
                lg.login(ch)
            elif ch == 2:
                lg.login(ch)
            elif ch == 3:
                break
            else:
                print("\n❌ Wrong Choice!!!")
        
        except Exception as er:
            print('\n❌ Please check your input value!!!\n')

main()