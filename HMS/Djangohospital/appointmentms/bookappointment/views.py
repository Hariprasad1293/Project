from datetime import datetime
from django.shortcuts import render

# Create your views here.
import email
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from bookappointment.models import BookAppointment as book_obj
import requests
import datetime
# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AppointmentSerializers

def book_data_insert(fname, lname, email, mobile, address, speciality, d_email, app_date, app_time, payment_status, transaction_id, appointment_status):
    appointment_data = book_obj(fname=fname, lname=lname, email=email, mobile=mobile, address=address,  speciality=speciality, d_email=d_email, appointment_date=app_date, appointment_time=app_time, payment_status=payment_status, transaction_id=transaction_id,appointment_status=appointment_status)

    appointment_data.save()
    return 1

@csrf_exempt
def book_appointment(request):
    if request.method == "POST":
        resp1={}
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            fname = val1.get("First Name")
            lname = val1.get("Last Name")
            email = val1.get("Email Id")
            mobile = val1.get("Mobile Number")
            address = val1.get("Address")
            app_date = val1.get("Appointment Date")
            app_time = val1.get("Appointment Time")
            #doctor_fname = val1.get("Doctor First Name")
            #doctor_lname = val1.get("Doctor Last Name")
            speciality = val1.get("Speciality")
            d_email = val1.get("Doctor Email")
            payment_status = val1.get("Payment Status")
            transaction_id = val1.get("Transaction Id")

            appointment_status = "Booked"

            #resp1={}
            """try:
                go = book_obj.objects.get(d_email=val1.get("Doctor Email"), appointment_date=val1.get("Appointment Date"), appointment_time=val1.get("Appointment Time"))
            except book_obj.DoesNotExist:
                mydate = datetime.datetime.strptime(app_date, "%Y-%m-%d").date()
                if mydate < datetime.date.today():
                    resp1['status'] = 'Failed'
                    resp1['status_code'] = '400'
                    resp1['message'] = 'Date cannot be in the past'
                    return HttpResponse(json.dumps(resp1), content_type='application/json') """
            respdata = book_data_insert(fname, lname, email, mobile, address, speciality, d_email, app_date, app_time, payment_status, transaction_id, appointment_status)
            if respdata:
                resp1['status'] = 'Success'
                resp1['status_code'] = '200'
                resp1['message'] = 'Appointment Booked Successfully'
            
                
            return HttpResponse(json.dumps(resp1), content_type='application/json')

def appointment_data(email):
    data = book_obj.objects.all().filter(email=email)
    for val in data.values():
        return val

@csrf_exempt
def appointment_status(request):
    if request.method == "POST":
        resp={}
        if 'application/json' in request.META['CONTENT_TYPE']:
            variable1 = json.loads(request.body)
            email = variable1.get("Patient Email")
            #resp={}
            respdata = appointment_data(email)

            if respdata:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = respdata
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Patient data is not available'
        return HttpResponse(json.dumps(resp), content_type='application/json')



#  EXTRA

class AppointmentAPIView(APIView):
    def get(self, _, pk=None):
        patients = book_obj.objects.all().filter(email=pk)
        serializer = AppointmentSerializers(patients, many=True)
        return Response(serializer.data) 


class AppointmentDoctorAPIView(APIView):
    def get(self, _, pk=None):
        doctors = book_obj.objects.all().filter(d_email=pk)
        serializer = AppointmentSerializers(doctors, many=True)
        return Response(serializer.data)

@csrf_exempt
def appointment_availablity(request):
    if request.method == "POST":
        resp={}
        if 'application/json' in request.META['CONTENT_TYPE']:
            variable1 = json.loads(request.body)
            app_date = variable1.get("Appointment Date")
            app_time = variable1.get("Appointment Time")
            d_email = variable1.get("Doctor Email")

            try:
                go = book_obj.objects.get(d_email=variable1.get("Doctor Email"), appointment_date=variable1.get("Appointment Date"), appointment_time=variable1.get("Appointment Time"))
            except book_obj.DoesNotExist:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Available'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Already Available'
            return HttpResponse(json.dumps(resp), content_type='application/json')



