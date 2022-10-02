from django.test import TestCase

# Create your tests here.
import unittest
import requests
import json

# Create your tests here.
class TestDoctor(unittest.TestCase):
    def test_register(self):
        abc = requests.post('http://127.0.0.1:7000/api/doctorregistration/',
                   {
                    "fname": "Dr. Def",
                    "lname": "ghi",
                    "email": "def@gmail.com",
                    "password": "1234",
                    "speciality": "Radiologist",
                    "mobile": "1111111113",
                    "address": "Bangalore"
        })
        content = json.loads(abc.content)
        print(content)
        self.assertEqual(content["email"], ["user with this email already exists."])
    def test_doctorlogin(self):
        res = requests.post('http://127.0.0.1:7000/api/doctorlogin/',{
            "email": "def@gmail.com",
            "password": "1234"
        })
        content = json.loads(res.content)
        print(content)
        assert "jwt" in content
    def test_profilepage(self):
        res = requests.get("http://127.0.0.1:7000/api/doctorview/")
        content = json.loads(res.content)
        print(content)
        assert len(content)>0

    def test_logout(self):
        res = requests.post("http://127.0.0.1:7000/api/doctorlogout/")
        content = json.loads(res.content)
        print(content)
        assert len(content)>0
    
    def test_yourappointments(self):
        res = requests.get("http://127.0.0.1:7000/api/doctorapiview/")
        content = json.loads(res.content)
        print(content)
        assert len(content)>0