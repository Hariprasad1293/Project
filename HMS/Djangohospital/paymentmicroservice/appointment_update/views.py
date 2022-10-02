from django.shortcuts import render

# Create your views here.
from payment.models import PaymentStatus as paystat
import requests
import json
# Create your views here.

def appointment_details_update(email):
    app_dict={}

    user = paystat.objects.filter(email=email)
    for data in user.values():
        data
    app_dict['Doctor Email'] = data['demail']
    app_dict['Speciality'] = data['speciality']
    app_dict['Payment Status'] = data['status']
    app_dict['Transaction Id'] = data['id']
    app_dict['Mobile Number'] = data['mobile']
    app_dict['Appointment Date'] = data['appointment_date']
    app_dict['Appointment Time'] = data['appointment_time']

    url = 'http://127.0.0.1:8000/api/patient_information/'

    d1={}
    d1['Email'] = data['email']
    data = json.dumps(d1)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    #response = requests.get(url, headers=headers)
    val1 = json.loads(response.content.decode('utf-8'))
    #val1 = json.loads(response.content)
    print("This is ", val1)

    app_dict['First Name'] = val1['data']['First Name']
    app_dict['Last Name'] = val1['data']['Last Name']
    app_dict['Address'] = val1['data']['Address']
    app_dict['Email Id'] = val1['data']['Email Id']

    url = 'http://127.0.0.1:5000/book_appointment/'

    data = json.dumps(app_dict)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    api_resp = json.loads(response.content.decode('utf-8'))
    #api_resp = json.loads(response.content)

    return api_resp