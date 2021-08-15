from flask import jsonify,request,Blueprint
import Dbconn
import time
import os

def convert(data):
    newdata={}
    for item in data:
        if item[0] not in newdata:
            temp={}
            l=[]
            temp['title']=item[1]
            temp['subject']=item[2]
            temp['summary']=item[3]
            temp['filepath']='C:\\Users\\FL_LPT-255\\Desktop\\upload\\'+str(item[5])+'.pdf'
            l.append(item[4])
            temp['category']=l
            newdata[item[0]]=temp
        else:
            temp=newdata[item[0]]
            temp['category'].append(item[4])
            newdata[item[0]]=temp
    return newdata



#content details to modify and delete by using authorid and content id
content_blueprint=Blueprint('content',__name__)
@content_blueprint.route("/content/<int:authorid>/<int:contentid>",methods=['GET','PUT','DELETE'])
def content(authorid,contentid):
    data={}
    status=400
    categories=[]
    conn=Dbconn.open_conn()
    if request.method=='GET':
        cursor=conn.execute("select * from content where authorid=? and contentid=?",(authorid,contentid))
        authordetails=list(cursor)
        if len(authordetails)==1:
            authordetails=list(authordetails[0])
            data['info']='data found'
            data['title']=authordetails[1]
            data['subject']=authordetails[2]
            data['summary']=authordetails[3]
            data['filepath']='C:\\Users\\FL_LPT-255\\Desktop\\upload\\'+str(authordetails[5])+'.pdf'
            cursor=conn.execute("select * from category where categoryid=?",(contentid,))
            for item in list(cursor):
                categories.append(item[1])
            data['categories']=categories
            status=200
        else:
            data['info']='data not found!'
    if request.method=='DELETE':
        cursor=conn.execute("delete from content where authorid=? and contentid=?",(authorid,contentid))
        conn.commit()
        if cursor.rowcount==1:
            cursor1=conn.execute("delete from category where categoryid=?",(contentid,))
            conn.commit()
            if cursor1.rowcount>=0:
                data['info']='deleted sucessfully'
            else:
                data['info']='not deleted sucessfully'
        else:
            data['info']='not deleted sucessfully'
    if request.method=='PUT':
        update_dic=request.form.to_dict()
        for key,value in update_dic:
            if key in ['title','summary','subject','body']:
                cursor=conn.execute("update content set ?=? where contentid=? ",(key,value,contentid))
                conn.commit()
                if cursor.rowcount==1:
                    data['info']='updated sucessfully!'
                else:
                    data['info']='not updated'
            if key=='category':
                category=request.form['category']
                cat_list=category.split(",")
                cursor=conn.execute("delete from category where categoryid=?",(contentid,))
                conn.commit()
                for item in cat_list:
                    cursor=conn.execute("insert into category(categoryid,categoryname) values(?,?)",(contentid,item))
                    conn.commit()
                    if cursor.rowcount>=1:
                        data['info']='updated sucessfully'
                    else:
                        data['info']='not updated '
    Dbconn.close_conn(conn)
    return jsonify(data)




#searching the contents using a matching items
search_blueprint=Blueprint('search',__name__)
@search_blueprint.route("/search/<int:id>",methods=['GET'])
def searchcontent(id):
    data={}
    status=400
    if request.method=='GET':
        conn=Dbconn.open_conn()
        search_dic=request.form.to_dict()
        for key,value in search_dic:
            if key in ['title','body','summary','category']:
                try:
                    cursor=conn.execute("select contentid,title,body,summary,categoryname,file from content left join category on content.contentid=category.categoryid where ? like ? and authorid=? ",(key,'%'+value+'%',id,))
                    data=convert(list(cursor))
                    status=200
                except Exception as e:
                    data['message']=e
    Dbconn.close_conn(conn)
    return jsonify(data),status


content_by_authorid_blueprint=Blueprint('content_by_authorid',__name__)
@content_by_authorid_blueprint.route("/content/<int:authorid>",methods=['GET'])
def getcontent(authorid):
    data={}
    status=400
    if request.method=='GET':
        conn=Dbconn.open_conn()
        try:
            cursor=conn.execute("select contentid,title,body,summary,categoryname,file from content left join category on content.contentid=category.categoryid where authorid=? ",(authorid,))
            data=convert(list(cursor))
            status=200
        except Exception as e:
            data['message']=e
    
    else:
        data['message']='please check the http method correctly!'
    return jsonify(data),status


# creating a content by the author 

content_blueprint=Blueprint('content',__name__)
@content_blueprint.route("/content/<int:id>",methods=['POST'])
def createcontent(id):
    data={}
    status=400
    try:
        title=request.form['title']
        body=request.form['body']
        summary=request.form['summary']
        if request.files['file'].filename.split('.')[-1]=='pdf':
            file=request.files['file']
            filename=time.time()
            conn=Dbconn.open_conn()
            cursor=conn.execute("insert into content(title,body,summary,authorid,file) values (?,?,?,?,?)",(title,body,summary,id,str(filename)))
            conn.commit()
            file.save(os.path.join('C:\\Users\\FL_LPT-255\\Desktop\\upload',str(filename)+'.pdf'))
            category=request.form['category'].split(",")
            cursor=conn.execute("select max(contentid) from content")
            max_count=int((list(cursor)[0])[0])
            for i in range (0,len(category)):
                cursor=conn.execute("insert into category(categoryid,categoryname) values (?,?)",(max_count,str(category[i])))
                conn.commit()
            data['message']="inserted sucessfully!"
            status=201
    except Exception as e:
        data['message']=e
        status=503
    Dbconn.close_conn(conn)
    return jsonify(data),status           
                    