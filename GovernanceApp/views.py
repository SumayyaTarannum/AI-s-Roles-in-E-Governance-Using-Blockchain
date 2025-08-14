from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
import json
from web3 import Web3, HTTPProvider
import pickle
import time
import pyaes, pbkdf2, binascii, os, secrets
import base64

global username, hospitalList, educationList, studentList, patientList
global contract, web3

def getKey(): #generating AES key based on Diffie common secret shared key
    password = "s3cr3t*c0d3"
    passwordSalt = str("0986543")#get AES key using diffie
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key

def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'   #7545    9545
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Governance.json' #Givernance contract file
    deployed_contract_address = '0x9B0d0214B4fCCb95837322494b6F6acB52625864' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getHospitalList():
    global hospitalList, contract
    hospitalList = []
    count = contract.functions.getHospitalCount().call()
    for i in range(0, count):
        hospital = contract.functions.getHospital(i).call()
        encrypted = base64.b64decode(hospital)
        decrypted = decrypt(encrypted).decode()
        arr = decrypted.split("$")
        hospitalList.append([arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]])

def getEducationList():
    global educationList, contract
    educationList = []
    count = contract.functions.getEducationCount().call()
    for i in range(0, count):
        education = contract.functions.getEducation(i).call()
        encrypted = base64.b64decode(education)
        decrypted = decrypt(encrypted).decode()
        arr = decrypted.split("$")
        educationList.append([arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]])

def getStudentList():
    global studentList, contract
    studentList = []
    count = contract.functions.getStudentCount().call()
    for i in range(0, count):
        student = contract.functions.getStudent(i).call()
        encrypted = base64.b64decode(student)
        decrypted = decrypt(encrypted).decode()
        arr = decrypted.split("$")
        studentList.append([arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9]])

def getPatientList():
    global patientList, contract
    patientList = []
    count = contract.functions.getPatientCount().call()
    for i in range(0, count):
        patient = contract.functions.getPatient(i).call()
        encrypted = base64.b64decode(patient)
        decrypted = decrypt(encrypted).decode()
        arr = decrypted.split("$")
        patientList.append([arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9]])        

getHospitalList()
getEducationList()    
getStudentList()
getPatientList()

def UserLoginAction(request):
    if request.method == 'POST':
        global username, contract, studentList, patientList
        username = request.POST.get('t1', False)
        output = ""
        flag = False
        output = 'User Healthcare Details<br/><table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Patient Name</font></th>'
        output+='<th><font size=3 color=black>Hospital Name</font></th>'
        output+='<th><font size=3 color=black>Disease Details</font></th>'
        output+='<th><font size=3 color=black>Gender</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Doctor Name</font></th>'
        output+='<th><font size=3 color=black>Prescription</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Visit Date</font></th>'
        output+='<th><font size=3 color=black>Username</font></th></tr>'
        for i in range(len(patientList)):
            hl = patientList[i]
            if hl[9] == username:
                flag = True
                output+='<tr><td><font size=3 color=black>'+hl[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[5]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[6]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[7]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[8]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[9]+'</font></td></tr>'
        output += "</table><br/>"

        output += 'User Education Details<br/><table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Student Name</font></th>'
        output+='<th><font size=3 color=black>Education Institution</font></th>'
        output+='<th><font size=3 color=black>Course Name</font></th>'
        output+='<th><font size=3 color=black>Gender</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Joining Date</font></th>'
        output+='<th><font size=3 color=black>Duration</font></th>'
        output+='<th><font size=3 color=black>Username</font></th></tr>'
        for i in range(len(studentList)):
            hl = studentList[i]
            print(hl)
            if hl[9] == username:
                flag = True
                output+='<tr><td><font size=3 color=black>'+hl[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[5]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[6]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[7]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[8]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[9]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        if flag == True:
            context= {'data':output}        
            return render(request,'UserScreen.html', context)
        else:
            context= {'data':'No record found in Blockchain for given username'}        
            return render(request,'UserLogin.html', context)

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def ViewPatients(request):
    if request.method == 'GET':
        global patientList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Patient Name</font></th>'
        output+='<th><font size=3 color=black>Hospital Name</font></th>'
        output+='<th><font size=3 color=black>Disease Details</font></th>'
        output+='<th><font size=3 color=black>Gender</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Doctor Name</font></th>'
        output+='<th><font size=3 color=black>Prescription</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Visit Date</font></th>'
        output+='<th><font size=3 color=black>Username</font></th></tr>'
        for i in range(len(patientList)):
            hl = patientList[i]
            if hl[1] == username:
                output+='<tr><td><font size=3 color=black>'+hl[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[5]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[6]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[7]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[8]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[9]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'HospitalScreen.html', context)  
 

def AddPatientsAction(request):
    if request.method == 'POST':
        global patientList, username
        today = str(datetime.now())
        patient_name = request.POST.get('t1', False)
        disease = request.POST.get('t2', False)
        gender = request.POST.get('gender', False)
        contact = request.POST.get('t3', False)
        doctor = request.POST.get('t4', False)
        prescription = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        uname = request.POST.get('t7', False)
        data = patient_name+"$"+username+"$"+disease+"$"+gender+"$"+contact+"$"+doctor+"$"+prescription+"$"+address+"$"+today+"$"+uname
        encrypted = encrypt(data.encode())
        encrypted = base64.b64encode(encrypted).decode()
        msg = contract.functions.savePatient(encrypted).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        patientList.append([patient_name, username, disease, gender, contact, doctor, prescription, address, today, uname])
        context= {'data':'Patient Details added using below Blockchain Transaction Details<br/>'+str(tx_receipt)}
        return render(request, 'AddPatients.html', context)        

def AddPatients(request):
    if request.method == 'GET':
       return render(request, 'AddPatients.html', {})

def ViewStudent(request):
    if request.method == 'GET':
        global studentList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Student Name</font></th>'
        output+='<th><font size=3 color=black>Education Institution</font></th>'
        output+='<th><font size=3 color=black>Course Name</font></th>'
        output+='<th><font size=3 color=black>Gender</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Joining Date</font></th>'
        output+='<th><font size=3 color=black>Duration</font></th>'
        output+='<th><font size=3 color=black>Username</font></th></tr>'
        for i in range(len(studentList)):
            hl = studentList[i]
            if hl[1] == username:
                output+='<tr><td><font size=3 color=black>'+hl[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[5]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[6]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[7]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[8]+'</font></td>'
                output+='<td><font size=3 color=black>'+hl[9]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'EducationScreen.html', context)  

def AddStudentAction(request):
    if request.method == 'POST':
        global studentList, username
        today = str(datetime.now())
        std_name = request.POST.get('t1', False)
        course = request.POST.get('t2', False)
        gender = request.POST.get('gender', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        duration = request.POST.get('t6', False)
        uname = request.POST.get('t7', False)
        data = std_name+"$"+username+"$"+course+"$"+gender+"$"+contact+"$"+email+"$"+address+"$"+today+"$"+duration+"$"+uname
        encrypted = encrypt(data.encode())
        encrypted = base64.b64encode(encrypted).decode()
        msg = contract.functions.saveStudent(encrypted).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        studentList.append([std_name, username, course, gender, contact, email, address, today, duration, username])
        context= {'data':'Student Details added using below Blockchain Transaction Details<br/>'+str(tx_receipt)}
        return render(request, 'AddStudent.html', context)
        
def AddStudent(request):
    if request.method == 'GET':
       return render(request, 'AddStudent.html', {})

def StudentLogin(request):
    if request.method == 'GET':
       return render(request, 'StudentLogin.html', {})

def PatientLogin(request):
    if request.method == 'GET':
       return render(request, 'PatientLogin.html', {})    

def EducationLogin(request):
    if request.method == 'GET':
       return render(request, 'EducationLogin.html', {})
    
def index(request):
    if request.method == 'GET':
        return render(request,'index.html', {})

def AddHospitals(request):
    if request.method == 'GET':
       return render(request, 'AddHospitals.html', {})
    
def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def HospitalLogin(request):
    if request.method == 'GET':
       return render(request, 'HospitalLogin.html', {})

def AddEducation(request):
    if request.method == 'GET':
       return render(request, 'AddEducation.html', {})    

def AddEducationAction(request):
    if request.method == 'POST':
        global educationList
        name = request.POST.get('t1', False)
        courses = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        username = request.POST.get('t6', False)
        password = request.POST.get('t7', False)
        status = "none"
        for i in range(len(educationList)):
            el = educationList[i]
            if el[5] == username:
                status = "exists"
                break
        if status == "none":
            data = name+"$"+courses+"$"+contact+"$"+email+"$"+address+"$"+username+"$"+password
            encrypted = encrypt(data.encode())
            encrypted = base64.b64encode(encrypted).decode()
            msg = contract.functions.saveEducation(encrypted).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            educationList.append([name, courses, contact, email, address, username, password])
            context= {'data':'Education Institution Details added using below Blockchain Transaction Details<br/>'+str(tx_receipt)}
            return render(request, 'AddEducation.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'AddEducation.html', context)    

def AddHospitalsAction(request):
    if request.method == 'POST':
        global usersList
        name = request.POST.get('t1', False)
        speciality = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        username = request.POST.get('t6', False)
        password = request.POST.get('t7', False)
        status = "none"
        for i in range(len(hospitalList)):
            hl = hospitalList[i]
            if hl[5] == username:
                status = "exists"
                break
        if status == "none":
            data = name+"$"+speciality+"$"+contact+"$"+email+"$"+address+"$"+username+"$"+password
            encrypted = encrypt(data.encode())
            encrypted = base64.b64encode(encrypted).decode()
            msg = contract.functions.saveHospital(encrypted).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            hospitalList.append([name, speciality, contact, email, address, username, password])
            context= {'data':'Hospital Details added using below Blockchain Transaction Details<br/>'+str(tx_receipt)}
            return render(request, 'AddHospitals.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'AddHospitals.html', context)

def EducationLoginAction(request):
    if request.method == 'POST':
        global username, contract, educationList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        for i in range(len(educationList)):
            elist = educationList[i]
            user1 = elist[5]
            pass1 = elist[6]
            if user1 == username and pass1 == password:
                status = "success"
                break
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "EducationScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'EducationLogin.html', context)
        
def HospitalLoginAction(request):
    if request.method == 'POST':
        global username, contract, hospitalList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        for i in range(len(hospitalList)):
            ulist = hospitalList[i]
            user1 = ulist[5]
            pass1 = ulist[6]
            if user1 == username and pass1 == password:
                status = "success"
                break
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "HospitalScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'HospitalLogin.html', context)

def AdminLoginAction(request):
    if request.method == 'POST':
        global username, contract, hospitalList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "AdminScreen.html", context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'AdminLogin.html', context)        

def ViewHospitals(request):
    if request.method == 'GET':
        global hospitalList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Hospital Name</font></th>'
        output+='<th><font size=3 color=black>Speciality</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Username</font></th>'
        output+='<th><font size=3 color=black>Password</font></th></tr>'
        for i in range(len(hospitalList)):
            hl = hospitalList[i]
            output+='<tr><td><font size=3 color=black>'+hl[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[2]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[3]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[4]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[5]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[6]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'AdminScreen.html', context)              


def ViewEducation(request):
    if request.method == 'GET':
        global educationList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Education Institution Name</font></th>'
        output+='<th><font size=3 color=black>Courses Offered</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Username</font></th>'
        output+='<th><font size=3 color=black>Password</font></th></tr>'
        for i in range(len(educationList)):
            hl = educationList[i]
            output+='<tr><td><font size=3 color=black>'+hl[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[2]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[3]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[4]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[5]+'</font></td>'
            output+='<td><font size=3 color=black>'+hl[6]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'AdminScreen.html', context)  







        


        
