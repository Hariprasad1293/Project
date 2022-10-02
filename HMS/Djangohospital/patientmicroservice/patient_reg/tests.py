from django.test import TestCase
import unittest
import requests
import json

# Create your tests here.
class TestPatient(unittest.TestCase):
    def test_register(self):
        abc = requests.post('http://127.0.0.1:8000/api/patientregistration/',
                   {
                       "fname": "first",
                        "lname": "last",
                        "email": "first@gmail.com",
                        "mobile": "1111111114",
                        "password": "1234",
                        "address": "Bhimavaram"
                    })
        content = json.loads(abc.content)
        print(content)
        self.assertEqual(content["email"], ["user with this email already exists."])
    def test_patientlogin(self):
        res = requests.post('http://127.0.0.1:8000/api/patientlogin/',{
            "email": "first@gmail.com",
            "password": "1234"
        })
        content = json.loads(res.content)
        print(content)
        assert "jwt" in content

    def test_profilepage(self):
        res = requests.get("http://127.0.0.1:8000/api/patientview/")
        content = json.loads(res.content)
        assert len(content)>0
        
    def test_logout(self):
        res = requests.post("http://127.0.0.1:8000/api/patientlogout/")
        content = json.loads(res.content)
        assert len(content)>0
    
    def test_yourappointments(self):
        res = requests.get("http://127.0.0.1:8000/api/patientinfo/")
        content = json.loads(res.content)
        assert len(content)>0