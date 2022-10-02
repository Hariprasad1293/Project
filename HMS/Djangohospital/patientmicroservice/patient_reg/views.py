from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from .models import Patient
from .serializers import PatientSerializer
import jwt, datetime
from django.http import HttpResponse
import requests
import json
# Create your views here.

class PatientRegisterView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PatientLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        patient = Patient.objects.filter(email=email).first()

        if patient is None:
            raise AuthenticationFailed('Patient not found')
        if not patient.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        payload = {
            'id': patient.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class PatientView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        patient = Patient.objects.filter(id=payload['id']).first()
        serializer = PatientSerializer(patient)
        #print(serializer.data['email'])
        return Response(serializer.data)


class PatientLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class PatientAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        patient = Patient.objects.filter(id=payload['id']).first()
        serializer = PatientSerializer(patient)
        emails = serializer.data['email']

        #emails = PatientSerializer(data=request.data)
        #if emails.is_valid():
        #    emails = emails.validated_data['email']
        patients = Patient.objects.all().filter(email=emails)
        #serializer = PatientAppointmentSerializers(patients, many=True)
        #return Response(serializer.data)
        return Response(self.formatPat(p) for p in patients)
    def formatPat(self, pat):
        appointments = requests.get('http://127.0.0.1:5000/getappointments/%s/patients/' % pat.email).json()
        return{
            'Patient First Name': pat.fname,
            'Patient Email' : pat.email,
             'appointments' : appointments,
    }

class PaymentViewAPI(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        patient = Patient.objects.filter(id=payload['id']).first()
        serializer = PatientSerializer(patient)
        emails = serializer.data['email']
        patients = Patient.objects.all().filter(email=emails)
        return Response(self.formatPat(p) for p in patients)
    def formatPat(self, pat):
        paymentshistory = requests.get('http://127.0.0.1:4000/getpaymentshistory/%s/payments/' % pat.email).json()
        return{
            'Patient First Name': pat.fname,
            'Patient Email' : pat.email,
             'your payments history' : paymentshistory,
    }


@csrf_exempt
def patient_info(request):
    email = request.POST.get("Email")
    
    if request.method == "POST":
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            email = val1.get('Email')
            resp={}
            if email:
                respdata = patient_data(email)
                dict1={}
                if respdata:
                    dict1['First Name'] = respdata.get('fname','')
                    dict1['Last Name'] = respdata.get('lname','')
                    dict1['Mobile Number'] = respdata.get('mobile','')
                    dict1['Email Id'] = respdata.get('email','')
                    dict1['Address'] = respdata.get('address','')
                if dict1:
                    resp['status'] = "Success"
                    resp['status_code'] = "200"
                    resp['data'] = dict1
                else:
                    resp['status'] = "Failed"
                    resp['status_code'] = "400"
                    resp['message'] = "Patient Not found"
            else:
                resp['status'] = "Failed"
                resp['status_code'] = "400"
                resp['message'] = "Fields are mandatory"
        else:
            resp['status'] = "Failed"
            resp['status_code'] = "400"
            resp['message'] = "Request type is not matched"
    else:
        resp['status'] = "Failed"
        resp['status_code'] = "400"
        resp["message"] = "Request type is not matched"
    return HttpResponse(json.dumps(resp), content_type='application/json')

# EXTRA


def patuser_data(email):
    user = Patient.objects.filter(email=email)
    for data in user.values():
        return data

def patient_data(email):
    patient = Patient.objects.filter(email=email)
    for data in patient.values():
        return data

'''
@csrf_exempt
def patient_appointments(request):
    email = request.POST.get("Patient Email")
    app_dict={}
    #app_dict['Patient First Name'] = data['fname']
    #app_dict['Patient Last Name'] = data['lname']
    #app_dict['Patient Email'] = message['email']
    #app_dict['Patient Mobile'] = data['mobile']
    #app_dict['Patient Address'] = data['address']
    
    url = 'http://127.0.0.1:5000/appointment_status/'
    d1={}
    #d1['Patient Email'] = message['email']
    d1['Patient Email'] = email
    data = json.dumps(d1)
    headers = {'Content-Type': 'application/json'}
    response= requests.post(url, data=data, headers=headers)
    api_resp = json.loads(response.content.decode('utf-8'))

    d1['Patient First Name'] = api_resp['message']['fname']
    d1['Patient Last Name'] = api_resp['message']['lname']
    d1['Patient Email Id'] = api_resp['message']['email']
    d1['Patient Mobile'] = api_resp['message']['mobile']
    d1['Patient Address'] = api_resp['message']['address']
    d1['Doctor Email'] = api_resp['message']['d_email']
    d1['Speciality'] = api_resp['message']['speciality']
    d1['Transaction Id'] = api_resp['message']['transaction_id']
    d1['Payment'] = api_resp['message']['payment_status']
    d1['Appointment status'] = api_resp['message']['appointment_status']

    return HttpResponse(json.dumps(d1), content_type='application/json')
# EXTRA

class PatientAPIInfoView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        patient = Patient.objects.filter(id=payload['id']).first()
        serializer = PatientSerializer(patient)
        emails = serializer.data['email']

        resp={}
        print(emails)
        if emails:
            #respdata = patient_data(emails)
            respdata = True
            dict1={}
            if respdata:
                dict1['First Name'] = respdata.get('fname','')
                dict1['Last Name'] = respdata.get('lname','')
                dict1['Mobile Number'] = respdata.get('mobile','')
                dict1['Email Id'] = respdata.get('email','')
                dict1['Address'] = respdata.get('address','')
                dict1['First Name'] = serializer.data['fname']
                dict1['Last Name'] = serializer.data['lname']
                dict1['Mobile Number'] = serializer.data['mobile']
                dict1['Email Id'] = serializer.data['email']
                dict1['Address'] = serializer.data['address']
                print(dict1)
                if dict1:
                    resp['status'] = "Success"
                    resp['status_code'] = "200"
                    resp['data'] = dict1
                else:
                    resp['status'] = "Failed"
                    resp['status_code'] = "400"
                    resp['message'] = "Patient Not found"
            else:
                resp['status'] = "Failed"
                resp['status_code'] = "400"
                resp['message'] = "Fields are mandatory"
        else:
            resp['status'] = "Failed"
            resp['status_code'] = "400"
            resp['message'] = "Request type is not matched"
    
        return HttpResponse(json.dumps(resp), content_type='application/json')
    
    
        

def patient_data(email):
    patient = Patient.objects.filter(email=email)
    for data in patient.values():
        return data


@csrf_exempt
def patient_info(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    patient = Patient.objects.filter(id=payload['id']).first()
    serializer = PatientSerializer(patient)
    emails = serializer.data['email']

    #email = request.POST.get("Email")
    resp={}
    if request.method == "POST":
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            email = val1.get('Email')
            #resp={}
            if emails:
                respdata = patient_data(emails)
                dict1={}
                if respdata:
                    dict1['First Name'] = respdata.get('fname','')
                    dict1['Last Name'] = respdata.get('lname','')
                    dict1['Mobile Number'] = respdata.get('mobile','')
                    dict1['Email Id'] = respdata.get('email','')
                    dict1['Address'] = respdata.get('address','')
                    print(dict1)
                if dict1:
                    resp['status'] = "Success"
                    resp['status_code'] = "200"
                    resp['data'] = dict1
                else:
                    resp['status'] = "Failed"
                    resp['status_code'] = "400"
                    resp['message'] = "Patient Not found"
            else:
                resp['status'] = "Failed"
                resp['status_code'] = "400"
                resp['message'] = "Fields are mandatory"
        else:
            resp['status'] = "Failed"
            resp['status_code'] = "400"
            resp['message'] = "Request type is not matched"
    else:
        resp['status'] = "Failed"
        resp['status_code'] = "400"
        resp["message"] = "Request type is not matched"
    return HttpResponse(json.dumps(resp), content_type='application/json')
    
class PatientAPIInfoViews(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        return payload
@csrf_exempt
def example(request):
    payload = PatientAPIInfoViews().get(request)
    if payload:
        patient = Patient.objects.filter(id=payload['id']).first()
        serializer = PatientSerializer(patient)
        emails = serializer.data['email']

        resp={}
        print(emails)
        if emails:
            #respdata = patient_data(emails)
            respdata = True
            dict1={}
            if respdata:
                dict1['First Name'] = respdata.get('fname','')
                dict1['Last Name'] = respdata.get('lname','')
                dict1['Mobile Number'] = respdata.get('mobile','')
                dict1['Email Id'] = respdata.get('email','')
                dict1['Address'] = respdata.get('address','')
                dict1['First Name'] = serializer.data['fname']
                dict1['Last Name'] = serializer.data['lname']
                dict1['Mobile Number'] = serializer.data['mobile']
                dict1['Email Id'] = serializer.data['email']
                dict1['Address'] = serializer.data['address']
                print(dict1)
                if dict1:
                    resp['status'] = "Success"
                    resp['status_code'] = "200"
                    resp['data'] = dict1
                else:
                    resp['status'] = "Failed"
                    resp['status_code'] = "400"
                    resp['message'] = "Patient Not found"
            else:
                resp['status'] = "Failed"
                resp['status_code'] = "400"
                resp['message'] = "Fields are mandatory"
        else:
            resp['status'] = "Failed"
            resp['status_code'] = "400"
            resp['message'] = "Request type is not matched"
    
        return HttpResponse(json.dumps(resp), content_type='application/json')
'''