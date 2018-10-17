from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST'])
def add_new_post():
    body = request.form('body')
    title = request.form('title')

    empty_error = ''

    if body == '':
        empty_error = 'Please fill in the body'
    
    if title == '':
        empty_error = 'Please fill in the title'
    
    else:
        return render_template('newpost.html',
        title=title,
        body=body,
        empty_error=empty_error)



if __name__ == '__main__':
    app.run()