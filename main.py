from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:ellen@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
#secret key

#Blog and User Classes
class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,body):
        self.title = title
        self.body = body
        self.owner_id = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

#Home Page Route
@app.route('/')
def index():
    entries = Blog.query.order_by(desc(Blog.id)).all()
    return render_template('blog.html', entries=entries)

#View Single Post Route
@app.route('/blog')
def post_id():
    id = request.args.get('id')
    if id is None:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)
    else:
        single_post = Blog.query.filter_by(id=id).first()
        print(single_post.title,single_post.body)
    return render_template('single_post.html', single_post=single_post)

#Add New Post Route
@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title =request.form['title']
        body = request.form['body']

        title_error = ""
        body_error = ""

        if title == "":
            title_error = "Must add a title"
            return render_template('newpost.html',title_error=title_error, body_error=body_error)
        if body == "":
            body_error = "Must add some text to the body"
            return render_template('newpost.html',title_error=title_error, body_error=body_error)
        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            id = new_post.id
            return redirect('/blog?id='+ str(id))
    
    return render_template('newpost.html')

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'single_post', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#Login Route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

#Run App
if __name__ == '__main__':
    app.run()