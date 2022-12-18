

from sqlalchemy import or_

import imp
from flask import Blueprint, request
from flask import jsonify
from .employeemodel import EmployeeModel


def findById(employee_id):
    return EmployeeModel.query.get(employee_id)



def createEmployeeConfig(EmployeedataJson):
    Employeedata = EmployeeModel()
    Employeedata = Employeedata.as_model(EmployeedataJson)
    Employeedata.save()
    return Employeedata


def updateEmployeeConfig(EmployeedataJson):
    Employeedata = EmployeeModel()
    Employeedata = Employeedata.as_model(EmployeedataJson)
    Employeedata.update()
    return Employeedata


def deleteById(id):
    Employeedata=findById(id)
    Employeedata.delete()