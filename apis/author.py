from flask import Blueprint,request,jsonify
import Dbconn
import os
import time
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check(email):
    if(re.match(regex, email)):
        return True
    else:
        return False
#creating a author by using the form data,by doing certian validations

author_blueprint=Blueprint('author',__name__)
@author_blueprint.route('/author',methods=['POST'])
def createAuthor():
    data={}
    status=400
    conn=Dbconn.open_conn()
    try:
        email=request.form['email']
        cursor=conn.execute("select * from author where email=?",(email,))
        cursorlength=len(list(cursor))
        if cursorlength==0:
            pasw=request.form['password']
            phno=request.form['phno']
            fn=request.form['fn']
            ln=request.form['ln']
            if "addr" in request.form:
                addr=request.form['addr']
            else:
                addr=None
            if "city" in request.form:
                city=request.form['city']
            else:
                city=None
            country=request.form['country']
            state=request.form['state']
            pincode=request.form['pincode']
            cursor=conn.execute("insert into author(email,pass,phno,fn,ln,addr,city,state,country,pincode)values(?,?,?,?,?,?,?,?,?,?)",(email,pasw,phno,fn,ln,addr,city,state,country,pincode,))
            conn.commit()
            if cursor.rowcount==1:
                data['message']='Inserted sucessfully!'
                status=201
            else:
                status=503
                data['message']='Not inserted sucessfully!'
    except Exception as err:
        data['message']=str(err)

    Dbconn.close_conn(conn)
    return jsonify(data),status

#author login aunthentication if sucessful it returns the author id

login_blueprint=Blueprint('login',__name__)
@login_blueprint.route("/login",methods=['GET'])
def login():
    data={}
    if request.method=='GET':
        conn=Dbconn.open_conn()
        if 'email' in request.form and 'password' in request.form:
            email=request.form['email']
            password=request.form['password']
            cursor=conn.execute("select * from author where email=? and pass=?",(email,password))
            cursordata=list(cursor)
            if len(cursordata)==1:
                data['info']='authenticated'
                print(list(cursor))
                data['id']=cursordata[0][0]
            else:
                data['info']='not anthenticated'
        else:
            data['info']='enter email and password correctly!'
    else:
        data['info']='please select the http method correclty'
    return jsonify(data)

