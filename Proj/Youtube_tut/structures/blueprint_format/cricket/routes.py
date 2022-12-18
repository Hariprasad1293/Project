
from flask import render_template,request,jsonify

from flask import Blueprint,render_template
from .employeeservice import findById,createEmployeeConfig,updateEmployeeConfig,deleteById
from .employeemodel import EmployeeModel
emppl=Blueprint('employee',__name__)

@emppl.route("/emp")
def emp():
    return render_template("index.html")




@emppl.route('/emp1', methods=['POST', 'PUT', 'GET'])

def Employeedatainsertion():
    EmployeeModelObj = EmployeeModel()
    if request.method == 'POST':
        EmployeeConfig = request.get_json(force=True)
        EmployeeModelObj  = createEmployeeConfig(EmployeeConfig)
    elif request.method == 'PUT':
        EmployeeConfig  = request.get_json(force=True)
        EmployeeModelObj = updateEmployeeConfig(EmployeeConfig)
    return jsonify(EmployeeModelObj.as_dict())



@emppl.route('/getdata/<id>',methods=['GET'])
def findbyId(id):
    Employee = findById(id)
    return jsonify(Employee.as_dict())


@emppl.route('/<id>',  methods=['DELETE'])
def deletebyId(id):
    deleteById(id)
    return jsonify({"success": True})