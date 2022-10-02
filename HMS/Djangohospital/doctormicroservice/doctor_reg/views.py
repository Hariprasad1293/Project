from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import Doctor
from .serializers import DoctorSerializer
import jwt, datetime
import requests
# Create your views here.

class DoctorRegisterView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DoctorLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        doctor = Doctor.objects.filter(email=email).first()

        if doctor is None:
            raise AuthenticationFailed('Doctor not found')
        if not doctor.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        payload = {
            'id': doctor.id,
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


class DoctorView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        doctor = Doctor.objects.filter(id=payload['id']).first()
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)


class DoctorLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class DoctorAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        doctor = Doctor.objects.filter(id=payload['id']).first()
        serializer = DoctorSerializer(doctor)
        emails = serializer.data['email']

        #emails = PatientSerializer(data=request.data)
        #if emails.is_valid():
        #    emails = emails.validated_data['email']
        doctors = Doctor.objects.all().filter(email=emails)
        #serializer = PatientAppointmentSerializers(patients, many=True)
        #return Response(serializer.data)
        return Response(self.formatPat(p) for p in doctors)
    def formatPat(self, doc):
        appointments = requests.get('http://127.0.0.1:5000/getdoctorappointments/%s/doctors/' % doc.email).json()
        return{
            'Doctor First Name': doc.fname,
            'Doctor Email' : doc.email,
             'appointments' : appointments,
    }