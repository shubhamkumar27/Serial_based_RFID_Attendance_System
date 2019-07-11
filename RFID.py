############################################# IMPORTING ################################################
import serial
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import os
import csv
import cv2
import datetime
import time
import threading
from PIL import Image,ImageFont,ImageDraw
import qrcode
from pushbullet import Pushbullet
global v
v=0
############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)
###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'shubhamkumar8180323@gmail.com' ")

###################################################################################

def label_reset():
    message1.configure(text="Please  check  all  fields  properly  before  saving !", bg="#00aeff")
    return

####################################################################################
def window2close():
    window2.destroy()
    stop_thread.clear()

#################################################################################

def RFID_scan():
    label_reset()
    try:
        ser1.close()
    except:
        pass
    i=0
    global rfid
    port = (txt9.get())
    print(port)
    try:
        ser = serial.Serial(port, 9600)
    except:
        message1.configure(text='Please  enter  the  correct  port  where  device  is  connected!', bg='red')
        return
    while 1:
        data = ser.readline()
        rfid = str(data[1:-2])
        print(rfid)
        if rfid != None:
            rfidmsg.configure(text=rfid)
            break
    exists1 = os.path.isfile("Details\Details.csv")
    if exists1:
        with open("Details\Details.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i=i+1
                if ((i > 1) and (i % 2 != 0)):
                    print(i)
                    print(str(lines[0]))
                    if (str(lines[0]) == rfid):
                        message1.configure(text="Card  is  already  registered,  please  take  a  new  card !!", bg="red")
                    else:
                        rfidmsg.configure(text='RFID is : ' + rfid)
    else:
        rfidmsg.configure(text='RFID is : '+rfid)
        return

###################################################################################

def save_pass():
    assure_path_exists("images\mfiles/")
    exists1 = os.path.isfile("images\mfiles\duinghr.db")
    if (not exists1):
        psd = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if psd == None:
            message1.configure(text='Password  not  set!!  Please  set  password')
            master.destroy()
        conn = sqlite3.connect('images\mfiles\duinghr.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Studentdetails(NAME TEXT)')
        c.execute("INSERT INTO StudentDetails VALUES (?)", (psd,))
        conn.commit()
        c.close()
        conn.close()
        message1.configure(text='Password  was  set  successfully !!')
        master.destroy()
    else:
        conn = sqlite3.connect('images\mfiles\duinghr.db')
        c = conn.cursor()
        c.execute("SELECT * FROM StudentDetails")
        data = c.fetchall()
        data = data[0]
        key = data[0]
        c.close()
        conn.close()
    op = (old.get())
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            conn = sqlite3.connect('images\mfiles\duinghr.db')
            c = conn.cursor()
            c.execute('''UPDATE Studentdetails SET NAME = ? WHERE NAME = ?''', (newp,key))
            conn.commit()
            c.close()
            conn.close()
        else:
            warn.configure(text='Confirm new password again!!!')
            return
    else:
        warn.configure(text='Please enter correct old password.')
        return
    old.delete(0, 'end')
    new.delete(0, 'end')
    nnew.delete(0, 'end')
    warn.configure(text='Password changed successfully!!',fg='green')

###################################################################################

def change_pass():
    global master
    master = tk.Toplevel()
    master.geometry("400x190")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    global warn
    warn = tk.Label(master, text='Check  new  password  properly  before  saving',fg="red" , bg='white',width = 38, font=('times', 12, ' bold '))
    warn.place(x=20, y=115)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=150)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=150)
    master.mainloop()

#####################################################################################

def psw():
    label_reset()
    assure_path_exists("images\mfiles/")
    exists1 = os.path.isfile("images\mfiles\duinghr.db")
    if (not exists1):
        psd = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if psd == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
            window.destroy
        conn = sqlite3.connect('images\mfiles\duinghr.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Studentdetails(NAME TEXT)')
        c.execute("INSERT INTO StudentDetails VALUES (?)", (psd,))
        conn.commit()
        c.close()
        conn.close()
    else:
        conn = sqlite3.connect('images\mfiles\duinghr.db')
        c = conn.cursor()
        c.execute("SELECT * FROM StudentDetails")
        data = c.fetchall()
        data = data[0]
        key = data[0]
        c.close()
        conn.close()
    password = tsd.askstring('Password', 'Enter Password', show='*')
    window2.grab_set()
    if (password == key):
        saveprofile()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    txt3.delete(0, 'end')
    txt4.delete(0, 'end')
    txt5.delete(0, 'end')
    txt6.delete(0, 'end')
    txt8.delete(0, 'end')
    rfidmsg.configure(text='Enter Port and click SCAN')
    message1.configure(text="Please  check  all  fields  properly  before  saving !",bg="#00aeff")

#######################################################################################

def saveprofile():
    global rfid
    columns = ['RFID','','ID','', 'NAME','','DOB','','BLOOD GROUP','','PHONE NO.','','EMAIL ID','','ADDRESS']
    assure_path_exists("Details/")
    exists = os.path.isfile("Details\Details.csv")
    if (not exists):
        with open("Details\Details.csv", 'a+',newline='') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
        csvFile1.close()

    Id = (txt.get())
    name = (txt2.get())
    dob = (txt3.get())
    blood = (txt4.get())
    phone = (txt5.get())
    email = (txt6.get())
    address = (txt8.get())
    if((name=='') or (Id=='') or (dob=='') or (blood=='') or (phone=='') or (email=='')):
        mess._show(title='Empty Fields',message='Please fill all fields to proceed !')
        return
    if (name.isalpha()) or (' ' in name):
        row = [rfid, '', Id, '', name, '', dob, '', blood, '', phone, '', email,'',address]
        global v
        if (v == 1):
            v=0
            print('updating')
            with open("Details\Details.csv", 'r') as inputf:
                with open("Details\Details1.csv", 'a+', newline='') as outputf:
                    writer = csv.writer(outputf)
                    reader1 = csv.reader(inputf)
                    for lines in reader1:
                        print(lines)
                        if str(lines[2]) == Id:
                            writer.writerow(row)
                        else:
                            writer.writerow(lines)
                outputf.close()
            inputf.close()
            clear()
            message1.configure(text='Profile saved successfully!', bg='#3ece48')
            os.remove("Details\Details.csv")
            os.rename("Details\Details1.csv","Details\Details.csv")
        else:
            with open("Details\Details.csv", 'r') as inputf:
                reader1 = csv.reader(inputf)
                for lines in reader1:
                    if str(lines[2]) == Id:
                        message1.configure(text='ID number is already alloted to someone', bg='red')
                        return
            with open('Details\Details.csv', 'a+',newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                csvFile.close()
            clear()
            message1.configure(text='Profile saved successfully!',bg='#3ece48')
    else:
        if name.isalpha() == False:
            res = "Enter Correct name"
            message1.configure(text=res)
            return

#########################################################################################

def update_profile():
    clear()
    label_reset()
    assure_path_exists('Details/')
    Id = tsd.askstring('ENTER ID NUMBER', 'Enter the ID number to generate I-Card')
    window2.grab_set()
    print(Id)
    if (Id == None):
        return
    exists = os.path.isfile("Details\Details.csv")
    if exists:
        with open("Details\Details.csv", 'r') as csvFile2:
            reader1 = csv.reader(csvFile2)
            for lines in reader1:
                if (str(lines[2]) == Id):
                    global rfid
                    rfid = lines[0]
                    name = lines[4]
                    id = lines[2]
                    phone = lines[10]
                    dob = lines[6]
                    blood = lines[8]
                    mail = lines[12]
                    address = lines[14]
        txt.insert(index=0, string=id)
        txt2.insert(index=0, string=name)
        txt3.insert(index=0, string=dob)
        txt4.insert(index=0, string=blood)
        txt5.insert(index=0, string=phone)
        txt6.insert(index=0, string=mail)
        txt8.insert(index=0, string=address)
        rfidmsg.configure(text=rfid)
        global v
        v=1
        csvFile2.close()

    else:
        message1.configure(text='Details  are  missing,  please  check  Details  folder !', bg='red')


########################################################################################

def sms(phone,name):
    try:
        phone = '+91'+phone
        msg = name.upper() + " is marked present at " + timeStamp + " on " + date
        pb = Pushbullet('o.2cvqqDnts32P4eD8DN5vjFOwBCXU9GzD')
        print(pb.devices)
        device = pb.devices[0]
        pb.push_sms(device, phone, msg)
    except:
        return

########################################################################################

def registration():
    stop_thread.set()
    global window2
    window2=tk.Toplevel()
    window2.grab_set()
    window2.geometry("1280x720")
    window2.resizable(False, True)
    window2.title("Attendance System")
    window2.configure(background='#262523')

    # global var
    # var = tk.Entry(window2,width=7 ,bg = '#262523',fg="#262523",font=('times', 4, ' bold '))
    # var.place(x=400, y=265)
    
    frame1 = tk.Frame(window2, bg="#00aeff")
    frame1.place(relx=0.11, rely=0.11, relwidth=0.78, relheight=0.45)

    frame2 = tk.Frame(window2, bg="#00aeff")
    frame2.place(relx=0.11, rely=0.57, relwidth=0.78, relheight=0.40)

    message3 = tk.Label(window2, text="**** REGISTRATION  FORM ****", fg="white", bg="#262523", width=55, height=1,font=('times', 29, ' bold '))
    message3.place(x=10, y=10)

    head = tk.Label(frame1, text="Personal  Details", width=83, height=1, fg="white", bg="blue", font=('times', 15, ' bold '))
    head.place(x=0, y=0)

    lbl = tk.Label(frame1, text="ID",width=20  ,height=1  ,fg="black"  ,bg="#00aeff" ,font=('times', 15, ' bold ') )
    lbl.place(x=50, y=34)
    global txt
    txt = tk.Entry(frame1,width=25 ,fg="black",font=('times', 15, ' bold '))
    txt.place(x=50, y=60)

    lbl2 = tk.Label(frame1, text="Name",width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 15, ' bold '))
    lbl2.place(x=370, y=34)
    global txt2
    txt2 = tk.Entry(frame1, width=25, fg="black", font=('times', 15, ' bold '))
    txt2.place(x=370, y=60)

    lbl3 = tk.Label(frame1, text="Date of Birth", width=20, fg="black", bg="#00aeff", font=('times', 15, ' bold '))
    lbl3.place(x=685, y=34)
    global txt3
    txt3 = tk.Entry(frame1, width=25, fg="black", font=('times', 15, ' bold '))
    txt3.place(x=685, y=60)

    lbl4 = tk.Label(frame1, text="Blood Group", width=20, fg="black", bg="#00aeff", font=('times', 15, ' bold '))
    lbl4.place(x=50, y=124)
    global txt4
    txt4 = tk.Entry(frame1, width=25, fg="black", font=('times', 15, ' bold '))
    txt4.place(x=50, y=150)

    lbl5 = tk.Label(frame1, text="Phone Number", width=20, fg="black", bg="#00aeff", font=('times', 15, ' bold '))
    lbl5.place(x=370, y=124)
    global txt5
    txt5 = tk.Entry(frame1, width=25, fg="black", font=('times', 15, ' bold '))
    txt5.place(x=370, y=150)

    lbl6 = tk.Label(frame1, text="Email ID", width=20, fg="black", bg="#00aeff", font=('times', 15, ' bold '))
    lbl6.place(x=685, y=124)
    global txt6
    txt6 = tk.Entry(frame1, width=25, fg="black", font=('times', 15, ' bold '))
    txt6.place(x=685, y=150)

    lbl8 = tk.Label(frame1, text="Address",width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 15, ' bold '))
    lbl8.place(x=50, y=214)
    global txt8
    txt8 = tk.Entry(frame1, width=57, fg="black", font=('times', 15, ' bold '))
    txt8.place(x=50, y=240)

    clearButton = tk.Button(frame1, text="Clear All Fields", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=20 ,activebackground = "white" ,font=('times', 15, ' bold '))
    clearButton.place(x=685, y=230)

    head2 = tk.Label(frame2, text="RFID  Details  and  I-Card", width=83, height=1, fg="white", bg="blue", font=('times', 15, ' bold '))
    head2.place(x=0, y=0)

    global rfidmsg
    rfidmsg = tk.Label(frame2, text="Enter Port and click SCAN",width=20,fg="black"  ,bg="white" ,font=('times', 15, ' bold '))
    rfidmsg.place(x=50, y=65)

    rfidtag = tk.Label(frame2, text="RFID Tag",width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 15, ' bold '))
    rfidtag.place(x=50, y=39)

    lbl9 = tk.Label(frame2, text="Port of Device",width=20  ,height=1  ,fg="black"  ,bg="#00aeff" ,font=('times', 15, ' bold ') )
    lbl9.place(x=370, y=39)
    global txt9
    txt9 = tk.Entry(frame2,width=25 ,fg="black",font=('times', 15, ' bold '))
    txt9.place(x=370, y=65)

    scan = tk.Button(frame2, text="SCAN", command=RFID_scan  ,fg="black"  ,bg="yellow"  ,width=20 ,activebackground = "white" ,font=('times', 15, ' bold '))
    scan.place(x=685, y=54)

    global message1
    message1 = tk.Label(frame2, text="Please  check  all  fields  properly  before  saving !", width=50, height=1, fg="black", bg="#00aeff", font=('times', 15, ' bold '))
    message1.place(x=200, y=120)

    save = tk.Button(frame2, text="SAVE PROFILE", command=psw, fg="black", bg="#3ece48", width=15,activebackground="white", font=('times', 15, ' bold '))
    save.place(x=50, y=180)

    icard = tk.Button(frame2, text="CREATE  I-CARD", command= make_icard ,fg="black", bg="orange", width=15,activebackground="white", font=('times', 15, ' bold '))
    icard.place(x=280, y=180)

    icard = tk.Button(frame2, text="EDIT PROFILE", command=update_profile, fg="black", bg="violet", width=15,activebackground="white", font=('times', 15, ' bold '))
    icard.place(x=510, y=180)

    quit = tk.Button(frame2, text="QUIT",command=window2close, fg="black", bg="red", width=15,activebackground="white", font=('times', 15, ' bold '))
    quit.place(x=740, y=180)

    ################################## MENUBAR #################################

    menubar = tk.Menu(window2, relief='ridge')
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label='Change Password', command=change_pass)
    filemenu.add_command(label='Contact Us', command=contact)
    filemenu.add_command(label='Exit', command=window.destroy)
    menubar.add_cascade(label='Help', font=('times', 29, ' bold '), menu=filemenu)
    window2.configure(menu=menubar)

    ################### CHECKING PASSWORD #############################

    assure_path_exists("images\mfiles/")
    exists1 = os.path.isfile("images\mfiles\duinghr.db")
    if (not exists1):
        psd = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if psd == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
            window2.destroy
        conn = sqlite3.connect('images\mfiles\duinghr.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Studentdetails(NAME TEXT)')
        c.execute("INSERT INTO StudentDetails VALUES (?)", (psd,))
        conn.commit()
        c.close()
        conn.close()

    window2.mainloop()

############################################################################################3

def make_icard():
    label_reset()
    assure_path_exists('images\sources\icard/')
    assure_path_exists('images\sources/')
    assure_path_exists('images/')
    assure_path_exists('Details/')
    Id = tsd.askstring('ENTER ID NUMBER', 'Enter the ID number to generate I-Card')
    window2.grab_set()
    print(Id)
    if (Id == None):
       return
    exists1 = os.path.isfile("Details\Details.csv")
    if exists1:
        pass
    else:
        message1.configure(text='Details  are  missing,  please  check  Details  folder !', bg='red')
    with open("Details\Details.csv", 'r') as csvFile2:
        reader1 = csv.reader(csvFile2)
        for lines in reader1:
            if (str(lines[2]) == Id):
                q=1
                global name
                name = lines[4]
                id = lines[2]
                phone = lines[10]
                dob = lines[6]
                blood = lines[8]
                mail = lines[12]
                try:
                    cap = cv2.VideoCapture(0)
                except:
                    try:
                        cap = cv2.VideoCapture(1)
                    except:
                        message1.configure(text='No  camera  was  found !', bg='red')
                while 1:
                    ret, fm = cap.read()
                    cv2.imshow('Photo for I-Card',fm)
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        fm = cv2.resize(fm, (0, 0), fx=0.8, fy=0.8)
                        fm = fm[50:330,150:360]
                        fm = cv2.resize(fm, (0, 0), fx=0.8, fy=0.8)
                        print(fm.shape)
                        cv2.imwrite("images\ "+name+id+".png", fm)
                        cv2.destroyAllWindows()
                        cap.release()
                        break
    if(q==0):
        message1.configure(text='ID  not  found  in records !', bg='red')

    csvFile2.close()

    icard = Image.open("images\sources\idcard.png")
    base = Image.new('RGB', (188, 242), (255, 255, 255))
    base2 = Image.new('RGB', (400, 41), (255, 255, 255))
    icard.paste(base2, (5, 365))
    photo = Image.open("images\ "+name+id+".png")
    draw = ImageDraw.Draw(icard)
    font = ImageFont.truetype('roboto\Roboto-Bold.ttf', size=31)
    fontd = ImageFont.truetype('roboto\Roboto-Bold.ttf', size=20)
    draw.text((30, 365), text=name.upper(), fill='orange', font=font)
    draw.text((60, 645), text='INSTITUTION ADDRESS', fill='white', font=font)
    draw.text((20, 20), text='INSTITUTION NAME & LOGO', fill='white', font=font)
    draw.text((30, 425), text='ID : '+id, fill='black', font=fontd)
    draw.text((30, 465), text='Contact no. : '+phone, fill='black', font=fontd)
    draw.text((30, 505), text='Blood Group : '+blood, fill='black', font=fontd)
    draw.text((30, 545), text='D.O.B. : '+dob, fill='black', font=fontd)
    draw.text((30, 585), text=mail, fill='red', font=fontd)
    qr = qrcode.make(str(name)+str(id))
    qr.save("images\sources\qr"+id+".png")
    img = cv2.imread("images\sources\qr"+id+".png")
    img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)
    cv2.imwrite("images\sources\qr"+id+".png", img)
    qri = Image.open("images\sources\qr"+id+".png")
    icard.paste(qri, (292, 155))
    icard.paste(base, (40, 101))
    icard.paste(photo, (50, 111))
    icard.save('images\icard\ '+name+id+'.png')
    Image._show('images\icard\ '+name+id+'.png')


###########################################################################################

def connect_attendance():
    global aport
    aport = (txt7.get())
    aport = aport.upper()
    t1 = threading.Thread(target=start_attendance, args=(aport,))
    t1.daemon = True
    t1.start()
    return

def start_attendance(aport):
    global ts
    ts = time.time()
    global date
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    global timeStamp
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    global flag
    global ser1
    flag=1
    try:
        ser1 = serial.Serial(aport, 9600)
        connect.configure(text ='CONNECTED')
        disconnect.configure(text='DISCONNECT')
    except:
        mess._show(title='Port Error', message='Please  enter  the  correct  port  where  device  is  connected!')
        return
    assure_path_exists("Attendance/")
    assure_path_exists("Details/")
    col_names = ['RFID','','Id', '', 'Name', '', 'Phone no.', '', 'Time', '', 'Date']
    exists1 = os.path.isfile("Details\Details.csv")
    if exists1:
        pass
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        return
    while 1:
        if stop_thread.is_set():
            break
        j = 0
        k = 0
        try:
            data = ser1.readline()
        except:
            return
        rfid = str(data[1:-2])
        print(data)
        exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
        if exists:
            with open("Attendance\Attendance_" + date + ".csv", 'r') as csvfile3:
                reader1 = csv.reader(csvfile3)
                for lines in reader1:
                    j = j + 1
                    if (j > 1) & (j % 2 != 0):
                        if (lines[0] == rfid):
                            #mess._show(title='Attendance Marked',message='Your attendance is already marked !')
                            k=1
                            break
                        else:
                            pass
            csvfile3.close()
        if (k==1):
            continue

        if (not stop_thread.is_set()):
            j=0
            print('inside')
            with open("Details\Details.csv", 'r') as csvFile2:
                reader1 = csv.reader(csvFile2)
                for lines in reader1:
                    if (str(lines[0]) == rfid):
                        for k in tv.get_children():
                            tv.delete(k)
                        name = lines[4]
                        id = lines[2]
                        phone = lines[10]
                        attendance = [rfid,'',id,'',name,'',phone,'',timeStamp,'',date]
                        t2 = threading.Thread(target=sms, args=(phone,name,))
                        t2.daemon = True
                        t2.start()
                        ser1.write('m'.encode())
                        exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
                        if exists:
                            with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                                writer = csv.writer(csvFile1)
                                writer.writerow(attendance)
                            csvFile1.close()
                        else:
                            with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                                writer = csv.writer(csvFile1)
                                writer.writerow(col_names)
                                writer.writerow(attendance)
                            csvFile1.close()
                        with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
                            reader1 = csv.reader(csvFile1)
                            for lines in reader1:
                                j = j + 1
                                if (j > 1):
                                    if (j % 2 != 0):
                                        iidd = str(lines[2])
                                        tv.insert('', 0, text=iidd, values=(str(lines[4]), str(lines[10]), str(lines[8])))
                        csvFile1.close()
                    else:
                        pass
            csvFile2.close()
        else:
            pass


def disconnect_attendance():
    #mess._show(title='Disconnected', message='Device disconnected successfully')
    try:
        ser1.close()

        disconnect.configure(text='DISCONNECTED')
        connect.configure(text='CONNECT')
    except:
        pass
    return

######################################## USED STUFFS ############################################

global key
key = ''

global stop_thread
stop_thread = threading.Event()

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }


######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(False,True)
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#00aeff")
frame1.place(relx=0.12, rely=0.17, relwidth=0.76, relheight=0.80)

message3 = tk.Label(window, text="RFID Based Attendance System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head1 = tk.Label(frame1, text="**** ATTENDANCE  SCREEN ****", fg="white",bg="blue" ,height=1,width=69,font=('times', 18, ' bold ') )
head1.place(x=0,y=0)

txt7 = tk.Entry(frame1,width=18 ,fg="black",font=('times', 15, ' bold '))
txt7.place(x=345, y=57)

message = tk.Label(frame1, text="ENTER PORT OF DEVICE" ,bg="#00aeff" ,fg="black"  ,width=22 ,height=1, activebackground = "yellow" ,font=('times', 14, ' bold '))
message.place(x=90, y=57)

lbl3 = tk.Label(frame1, text="--------------- PRESENT  ATTENDANCE ----------------",width=50  ,fg="black"  ,bg="#00aeff" ,font=('times', 15, ' bold '))
lbl3.place(x=180, y=110)

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('times', 29, ' bold '), menu=filemenu)
window.configure(menu=menubar)

###################### TREEVIEW TABLE ##########################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=150)
tv.column('name',width=250)
tv.column('date',width=190)
tv.column('time',width=180)
tv.grid(row=2,column=0,padx=(90,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

register_update = tk.Button(frame1, text="Register  or  Update  Profile", command=registration ,fg="black"  ,bg="yellow"  ,width=32  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
register_update.place(x=505, y=450)
connect = tk.Button(frame1, text="CONNECT", command=connect_attendance  ,fg="black"  ,bg="#3ece48"  ,width=13  , activebackground = "white" ,font=('times', 14, ' bold '))
connect.place(x=545,y=52)
disconnect = tk.Button(frame1, text="DISCONNECT", command=disconnect_attendance  ,fg="black"  ,bg="red"  ,width=15  , activebackground = "white" ,font=('times', 14, ' bold '))
disconnect.place(x=715,y=52)
quitWindow = tk.Button(frame1, text="Quit Application", command=window.destroy  ,fg="black"  ,bg="red"  ,width=32 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=73, y=450)

###################################################################3

j=0
exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
if exists:
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            j = j + 1
            if (j > 1):
                if (j % 2 != 0):
                    iidd = str(lines[2])
                    tv.insert('', 0, text=iidd, values=(str(lines[4]), str(lines[10]), str(lines[8])))
    csvFile1.close()

##################### END ######################################
    
window.configure(menu=menubar)
window.mainloop()
