from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from payment.models import PaymentStatus as paystat
from appointment_update.views import appointment_details_update
import datetime
from pytz import timezone
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PaymentSerializers
# Create your views here.

def get_transaction_details(email):
    user = paystat.objects.filter(email=email)
    for data in user.values():
        return data


def store_data(email, demail, speciality, mode_of_payment, mobile, app_date, app_time):
    user_data = paystat(email=email, demail=demail, speciality=speciality, appointment_date=app_date, appointment_time=app_time, mode_of_payment=mode_of_payment, mobile=mobile, status="Success")
    user_data.save()
    return 1

@csrf_exempt
def get_payment(request):
    email = request.POST.get("Email")
    demail = request.POST.get("Doctor Email")
    speciality = request.POST.get("Speciality")
    mode_of_payment = request.POST.get("Payment mode")
    mobile = request.POST.get("Mobile")
    app_date = request.POST.get("Appointment Date")
    app_time = request.POST.get("Appointment Time")
    
    resp={}
    mydate = datetime.datetime.strptime(app_date, "%Y-%m-%d").date()
    if mydate < datetime.date.today():
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Date cannot be in the past'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    mynewdate = datetime.date.today() + datetime.timedelta(days=7)
    if mydate > mynewdate:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'You can only book the appointment with in 7 days.'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    
    todays_day = mydate.weekday()
    if todays_day == 6:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Sunday is a Holiday. Please pick some other day'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    mytime = app_time[0:2]
    mytime2 = app_time[3:5]
    mytime = int(mytime)
    mytime2 = int(mytime2)
    ind_times = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M')

    if mytime < 9 or mytime >= 17:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Appointments slots are available from 9 am to 5 pm, You cannot book before 9 am and after 5 pm'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if mydate == datetime.date.today():
        if(mytime < int(ind_times[0:2])):
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Time cannot be in the past'
            return HttpResponse(json.dumps(resp), content_type='application/json')
   # if(mytime < int(ind_times[0:2])):
      #  resp['status'] = 'Failed'
      #  resp['status_code'] = '400'
      #  resp['message'] = 'Time cannot be in the past'
       # return HttpResponse(json.dumps(resp), content_type='application/json') 
    app_dict = {}
    app_dict['Doctor Email'] = demail
    app_dict['Appointment Date'] = app_date
    app_dict['Appointment Time'] = app_time
    url = 'http://127.0.0.1:5000/appointment_availability/'
    data = json.dumps(app_dict)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    #response = requests.get(url, headers=headers)
    val1 = json.loads(response.content.decode('utf-8'))
    #val1 = json.loads(response.content)
    print("This is ", val1)
    if val1['status'] == "Failed":
        resp2={}
        resp2['status'] = "Failed"
        resp2['status_code'] = "400"
        resp2['message'] = "Same slot for this doctor is not available"
        return HttpResponse(json.dumps(resp2), content_type='application/json')




    if email and demail and speciality and mode_of_payment and mobile and app_date and app_time:

        respdata = store_data(email, demail, speciality, mode_of_payment, mobile, app_date, app_time)

        respdata2 = appointment_details_update(email)

        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Transaction is completed'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Transaction is failed, Please try again.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '404'
        resp['message'] = 'All fields are mandatory'
    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def user_transaction_info(request):
    email = request.POST.get("Email")
    resp={}
    if request.method == "POST":
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            email = val1.get('Email')
            #resp={}

            if email:
                respdata = get_transaction_details(email)
                if respdata:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['data'] = respdata
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'User not found'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Fields are mandatory'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Request type is not matched'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Request type is not matched'
    return HttpResponse(json.dumps(resp), content_type='application/json')

class PaymentsAPIView(APIView):
    def get(self, _, pk=None):
        patients = paystat.objects.all().filter(email=pk)
        serializer = PaymentSerializers(patients, many=True)
        return Response(serializer.data)