from flask import Flask
from apis.author import author_blueprint,login_blueprint
from apis.content import content_blueprint,search_blueprint,content_by_authorid_blueprint

app=Flask(__name__)
app.register_blueprint(author_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(content_blueprint)
app.register_blueprint(content_by_authorid_blueprint)
app.register_blueprint(search_blueprint)

app.run()