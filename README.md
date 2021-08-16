Build APIs only for a Content Management System 

● The system will have 1 user role, i.e author

● Author should be able to register and login using name and password to the CMS (Refer below table for user fields)

● Author can create, view, edit and delete contents created by him.

● Users should search content by matching terms in title, body, summary and categories.

                                ●Technology used is python,Framework used is Flask and database used is sqlite3


-------------------------------------------------------------------------------------------------------------------------------------------------
To get started, install Python and flask on your local computer 
if you don't have them already. You can optionally use another database system instead of SQLite, like Postgres

## Create a virtual environment

```bash
python -m venv env
```
### To activate virtual environment

```bash
.\env\Scripts\activate
```

## requirements.txt

```bash
pip install -r requirements.txt
```
-----------------------------------------------------------------------------------------------------------------------------
 ● Firstly setup with the database:
           
           3 tables are created ,i.e 1)author,2)content,3)category
           
           1)The schema of author table:-
                               CREATE TABLE author(
                                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           email TEXT NOT NULL,
                                           pass TEXT NOT NULL,
                                           Phno TEXT NOT NULL,
                                           fn TEXT NOT NULL,
                                           ln TEXT NOT NULL,
                                           addr TEXT,
                                           city TEXT,
                                           state TEXT,
                                           country TEXT,
                                           pincode INT NOT NULL);
           2)The schema of content table:-[author->content- one to many relationship]:-
                               CREATE TABLE content(
                                           contentid INTEGER PRIMARY KEY AUTOINCREMENT,
                                           title text not null,
                                           body text not null,
                                           summary text not null,
                                           authorid integer, file text,
                                           constraint fk_1
                                           foreign key (authorid)
                                           references author(id));
           3)The schema of category table:[content->category-one to many relationship]:-
                               CREATE TABLE category(
                                           categoryid integer not null,
                                           categoryname text not null,
                                           constraint fk_2 foreign key (categoryid) references content(id)); 
------------------------------------------------------------------------------------------------------------------------------------------------------------                                                     
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------   
**NOTE**:-
                         
                         ● After creating the database the path of database should change in the Dbconn.py file
                           
                          ● We have to create a one folder so that we can store the pdf files which uploaded by the author
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
             
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
I have created the following routes 
               
                           ● /createauthor                          -> used to create the new author 
                           
                           ● /login                                 -> used to authneticate the author
                           
                           ●/createcontent/<int:id>                 ->used to create the content for the paticular author id
                           
                           ●/getcontent/<int:id>                    ->get all the content details for the paticular author id       
                           
                           ●content/<int:authorid>/<int:contentid>  ->Get,delete,update the content content details for the paticular author id and content id
                           
                           ●searchcontent/<int:authorid>            ->Get all the content details which match with paticular keyword of paticular author id
    
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
