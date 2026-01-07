import os
import time
import hashlib
import sqlite3
from cryptography.fernet import Fernet
import base64
import atexit
import base64
import pwinput

s1 = '#'*12
s2 = '-'*12
my_path = os.path.dirname(os.path.abspath(__file__))
_time = time.strftime('[%Y-%m-%d] %p: %H:%M:%S')
with open(f'{my_path}\\logdata.txt', 'a') as f:
    f.write(f'\n\n{s2} {_time} {s2}\n\n')


def at_exit():
    if os.path.exists(f'{my_path}\\BioDataBase.db'):
        try:
            db = sqlite3.connect(f'{my_path}\\BioDataBase.db')
            db.close()
        except Exception:
            None

def goto_about():
    save_to_log('goto about')
    print(f'\n\n{s2} ABOUT DEVELOPER {s2}')
    print(f"""
    Developer Name : Vimitha S.
    Age            : 14 Years
    Tools Used     : Python (OS, Time, Hashlib, SQLite3, cryptography, base64, pwinput)
    GitHub         : https://github.com/VimithaProCoding
    
    Description    : 
    A secure and robust Bio Data Management System developed with a focus on 
    data privacy and security. This application implements advanced SHA-256 
    hashing for password protection and AES-based Fernet encryption for 
    securing user notes.
          
    App Version : version 3.0
    App Release Date : 01 / 07 / 2026
    """)
    print(f"{s2}{s2}{s2}\n")
    
    try:    
        input('Press Enter to go back to Main Menu...')
        main_page()
    except KeyboardInterrupt:
        print(f'\n\n{s1} You Cant Use COMMANDS...{s1}\n\n')
        save_to_log('Trying to use Commands')
        main_page()
    except Exception as e:
        main_page()   

def save_to_log(text):
    try:
        with open(f'{my_path}\\logdata.txt', 'a') as f:
            f.write(f'{_time} >> {text}\n')
            f.close()
    except FileNotFoundError:
        print('Log File Not Found')
    except Exception as e:
        print('Error (e) code: ',e)

def goto_exit():
    save_to_log('exited')
    print('Exiting...')
    time.sleep(1)
    exit()

def save_data(n, a, p, note):
    save_to_log('new user aded')
    db = sqlite3.connect(f'{my_path}\\BioDataBase.db')
    cmd = db.cursor()
    try:
        cmd.execute("INSERT INTO users (user_name, user_age, user_password, user_note) VALUES (?, ?, ?, ?)", (n, a, p, note))
        db.commit()
        db.close()
        return 'saved'
        
    except sqlite3.IntegrityError:
        #print('\n....Something Went Wrong....\n')
        db.close()
        return 'error1'
        

    except Exception as e:
        #print(f'\nError code: {e}\n')
        db.close()
        print(f'\ncode : {e}\n')
        return f'error2'

def turn_to_encript(name, note):
    key = base64.urlsafe_b64encode(name.encode().ljust(32)[:32])
    f = Fernet(key)

    en_note = f.encrypt(note.encode())
    return en_note

def turn_to_decript(name, note):
    key = base64.urlsafe_b64encode(name.encode().ljust(32)[:32])
    f = Fernet(key)

    en_note = f.decrypt(note).decode()
    return en_note

def update_data(name, note):
    save_to_log('updated data')
    conn = sqlite3.connect(f'{my_path}\\BioDataBase.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET user_note = ? WHERE user_name = ?", (note, name))
    conn.commit()
    conn.close()
    return 'saved'

def convert_to_hash(psw):
    save_to_log('password convert to hash')
    byte_psw = psw.encode()
    hash_pasw = hashlib.sha256(byte_psw)
    return hash_pasw.hexdigest()

def load_data(name):
    save_to_log('load user data')
    db = sqlite3.connect(f'{my_path}\\BioDataBase.db')
    cmd = db.cursor()

    cmd.execute('SELECT * FROM users WHERE user_name = ?', (name,))
    user = cmd.fetchone()
    return(user)
    
def goto_register():
    save_to_log('goto register')
    print(f'\n\n{s2} REGISTER {s2}\n')
    while True:
        try:
            while True:
                try:
                    r_f_name = input('Enter First Name\n: ')
                    if not r_f_name.isalpha():
                        print(f'{s1} Please Enter Name {s1}\n')
                        main_page()
                        break

                    r_l_name = input('Enter Last Name\n: ')
                    if not r_l_name.isalpha():
                        print(f'{s1} Please Enter Name {s1}\n')
                        main_page()
                        break
                    full_name = f'{r_f_name.lower()}{r_l_name.lower()}'
                    full_name = full_name.replace(' ','')
                    
                    if os.path.exists(f'{my_path}\\BioDataBase.db'):
                        try:
                            db = sqlite3.connect(f'{my_path}\\BioDataBase.db')
                            cmd = db.cursor()

                            cmd.execute('SELECT * FROM users WHERE user_name = ?', (full_name,))
                            user = cmd.fetchone()
                            if user == None:
                                break
                            else:
                                print(f'\nEROR....\n{s1} Use Another Name {s1}\n')
                                main_page()
                                break
                        except sqlite3.IntegrityError:
                            print('\n....Something Went Wrong....\n')
                            db.close()

                        except Exception as e:
                            print(f'\nError code: e\n')
                            db.close()
                    else:
                        break

                except KeyboardInterrupt:
                    save_to_log('Trying to use Commands')
                    print(f'\n\n{s1} You Cant Use COMMANDS...{s1}\n\n')
                    continue
                except Exception as e:
                    print('Error code: ',e)
                    main_page()
                    break
                

            r_age = input('Enter Your Age\n: ')
            if r_age.isdigit():
                r_age = int(r_age)
                if r_age <= 10:
                    print(f'{s1} Your Under 10.. {s1}\n')
                    main_page()
                    break
                else:
                    while True:
                        r_password = pwinput.pwinput(prompt='Enter Password\n: ', mask='*')
                        longp = len(r_password) > 6
                        isdigit = False
                        for leter in r_password:
                            if leter.isdigit():
                                isdigit = True
                        if longp and isdigit:
                            hashed_password = convert_to_hash(r_password)
                            print(f'\n\nWelcome {r_f_name}. \nYour Data Is Saving....... \n')
                            time.sleep(1)

                            #save data
                            conection = sqlite3.connect(f'{my_path}\\BioDataBase.db')
                            cursor = conection.cursor()

                            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users(
                                           user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           user_name TEXT UNIQUE,
                                           user_age INTEGER,
                                           user_password TEXT,
                                           user_note TEXT
                            )
                            ''')
                            conection.close()

                            User_name = f'{r_f_name.lower()}{r_l_name.lower()}'
                            User_name = User_name.replace(' ','')
                            User_age = r_age
                            User_password = hashed_password
                            User_note = None
                            stext = save_data(User_name, User_age, User_password, User_note)

                            if stext == 'saved':
                                print('Saved Successfull')
                                time.sleep(1)
                                user_details = load_data(User_name)
                                print(f'\n\n{s2} User Details {s2}\n\n  User ID : {user_details[0]}\n  Name is : {user_details[1]}\n  Age is  : {user_details[2]}\n')
                                
                                try:    
                                    input('')
                                except KeyboardInterrupt:
                                    print(f'\n\n{s1} You Cant Use COMMANDS...{s1}\n\n')
                                    main_page()
                                    break
                                except Exception as e:
                                    print(f'\n\n{s1} You Cant Use COMMANDS...e{s1}\n\n')
                                    main_page()
                                    break

                                main_page()
                                break

                            elif stext == 'error1':
                                print(f'\n{s1} EROR(1) {s1}\n')
                                main_page()
                                break
                            elif stext == 'error2':
                                print(f'\n{s1} EROR(2) {s1}\n')
                                main_page()
                                break
                            else:
                                print(f'\n{s1} EROR(else) {s1}\n')

                        else:
                            print('\n## (please enter storng password) ##\n')
                            continue         
        
            print(f'{s1} Please Enter Number.. {s1}\n')
            main_page()
            break

        except KeyboardInterrupt:
            print(f'\n\n{s1} You Cant Use COMMANDS...{s1}\n\n')
            continue
        except Exception:
            main_page()
            break

def goto_login():
    save_to_log('goto login')
    print(f'\n\n{s2} LOGIN {s2}\n\n')
    while True:
        try:
            l_name = input('Enter Your Full Name\n: ')
            full_name = l_name.lower()
            full_name = full_name.replace(' ','')
                    
            if os.path.exists(f'{my_path}\\BioDataBase.db'):
                try:
                    db = sqlite3.connect(f'{my_path}\\BioDataBase.db')
                    cmd = db.cursor()

                    cmd.execute('SELECT * FROM users WHERE user_name = ?', (full_name,))
                    user = cmd.fetchone()
                    if user == None:
                        print(f'\n{s1} Wrong Name {s2}\n')
                        db.close()
                        main_page()
                        break
                    else:
                        l_password = pwinput.pwinput(prompt='\nEnter You Password\n: ', mask='*')
                        l_hash_password = convert_to_hash(l_password)
                        if l_hash_password == user[3]:
                            print(f'\n\n\nLOGIN SUCCESS...\n')
                            time.sleep(1)
                            print(f'\nWelcome {user[1]}\nLoding Your Data....')
                            time.sleep(1)
                            print(f'\n\n{s2} User Details {s2}\n\n  User ID : {user[0]}\n  Name is : {user[1]}\n  Age is  : {user[2]}\n\n(1) Show Note\n(2) Add Note\n')

                            try:    
                                a = input(': ')
                                if a == '1':
                                    try:
                                        if user[4] == None:
                                            print(f'\n{s2} Note {s2}\n\n{user[4]}\n\n{s2}{s2}------')
                                            try:
                                                input('')
                                            except KeyboardInterrupt:
                                                continue
                                            except Exception:
                                                continue
                                            main_page()
                                            break
                                        else:
                                            load_note = turn_to_decript(user[3], user[4])
                                            print(f'\n{s2} Note {s2}\n\n{load_note}\n\n{s2}{s2}------')
                                            try:
                                                input('')
                                            except KeyboardInterrupt:
                                                continue
                                            except Exception:
                                                continue
                                            main_page()
                                            break

                                    except Exception as e:
                                        print('Error : ',e)
 
                                if a == '2':
                                    try:

                                        note = input('Enter Note\n\n: ')
                                        time.sleep(1)

                                        try:
                                            ennote = turn_to_encript(user[3], note)
                                        except Exception as e:
                                            print('Error : ',e)          
                                        try:              
                                            update_data(user[1], ennote)
                                            print('Saved Note\n')
                                            main_page()
                                            break
                                        except Exception as e:
                                            print('Error : ',e)

                                    except KeyboardInterrupt:
                                        main_page()
                                        break
                                    except Exception:
                                        main_page()
                                        break  

                            except KeyboardInterrupt:
                                print(f'\n\n{s1} You Cant Use COMMANDS...{s1}\n\n')
                                save_to_log('Trying to use Commands')
                                main_page()
                                break
                            except Exception as e:
                                print(f'\n\n{s1} You Cant Use COMMANDS...e{s1}\n\n')
                                main_page()
                                break

 
                        else:
                            print(f'\n{s1} Incorrect Password {s1}\n')
                            db.close()
                            continue
                        
                    
                        
                    db.close()

                except sqlite3.IntegrityError:
                    print('\n....Something Went Wrong....\n')
                    db.close()
                    main_page()
                    break
                except Exception as e:
                    print(f'\nError code: e\n')
                    db.close()
                    main_page()
                    break
            else:
                print(f'\n\n{s1} Data Base Not Found {s1}\nPlease try Register To Start.\n\n')
                try:    
                    input('')
                except KeyboardInterrupt:
                    print(f'\n\n{s1} You Cant Use COMMANDS...{s1}\n\n')
                    save_to_log('Trying to use Commands')
                    main_page()
                    break
                except Exception as e:
                    print(f'\n\n{s1} You Cant Use COMMANDS...e{s1}\n\n')
                    main_page()
                    break

                main_page()
                break

        except KeyboardInterrupt:
            print(f'\n\n{s1} You Cant Use COMMANDS...{s1}\n\n')
            save_to_log('Trying to use Commands')
            continue
        except Exception as e:
            print('Error e')
            main_page()
            break


def main_page():
    save_to_log('goto home')
    while True:
        print(f'\n{s2} Bio Data {s2}\n\n(1) LOGIN\n(2) REGISTER\n(3) About\n(4) EXIT')
        try:
            answer = input('\n: ')
        except Exception:
            continue
        except KeyboardInterrupt:
            save_to_log('Trying to use Commands')
            continue

        if answer=='1':
            goto_login()
            break
        elif answer=='2':
            goto_register()
            break
        elif answer=='3':
            goto_about()
            break
        elif answer=='4':
            goto_exit()
            break
        else:
            print(f'\n{s1} Please Enter 1 or 2 {s1}\n')
            continue



main_page()
atexit.register(at_exit())
