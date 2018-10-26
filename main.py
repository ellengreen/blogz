from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:ellen@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
app.secret_key = 'thisisasecretkey'


class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'single_post', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/')
def index():

    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    blog_user = request.args.get('user')

    if blog_id:
        blog_post = Blog.query.filter_by(id=blog_id).first()
        return render_template('single_post.html', 
        title="Blog Entry", 
        blog_post=blog_post)

    if blog_user:
        user = User.query.filter_by(username=blog_user).first()
        blog_post = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', 
        title="User's Blog", 
        blog_post=blog_post, 
        username=blog_user)
    
    else:
        blog_post = Blog.query.all()
    return render_template('blog.html', title="Blogz", blog_post=blog_post)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()


        title_error = ""
        body_error = ""

        if blank(title):
            title_error = "Must add a title"
            return render_template('newpost.html',title_error=title_error, body_error=body_error)
        if blank(body):
            body_error = "Must add some text to the body"
            return render_template('newpost.html',title_error=title_error, body_error=body_error)
        else:
            new_post = Blog(title, body, owner)
            db.session.add(new_post)
            db.session.commit()
            id = new_post.id
            flash('Blog has been posted!!', 'success')
            return redirect('/blog?id='+ str(id))
    
    return render_template('newpost.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    user_error = ''
    pass_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash(username + ' Logged in!')
            return redirect ('/newpost')
        else:
            if blank(username):
                user_error = 'Cannot leave blank'

            if blank(password):
                pass_error = 'Cannot leave blank'

            if not user:
                user_error = 'User does not exist'
            elif not user.password == password:
                pass_error = 'Password is incorrect'
            return render_template('login.html',
            username=username,
            user_error=user_error,
            pass_error=pass_error)
            
    return render_template('login.html')

def blank(form):
    if form == "":
        return True
    else:
        return False

def valid_length(data):
    if len(data) <3:
        return False
    else:
        return True

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        user_error = ''
        pass_error = ''
        verify_error = ''
        existing_user = User.query.filter_by(username=username).first()

        if not valid_length(username):
            user_error = 'Username must be more than 3 characters'
        if not valid_length(password):
            pass_error = 'Password must be more than 3 characters'
        
        if password != verify:
            verify_error = 'Passwords do not match'
        
        if blank(username):
            user_error = 'Cannot leave blank'
        if blank(password):
            pass_error = 'Cannot leave blank'
        if blank(verify):
            verify_error = 'Cannot leave blank'

        if user_error or pass_error or verify_error:
            return render_template('signup.html', user_error=user_error, pass_error=pass_error, verify_error=verify_error)

       
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
           flash('Username already exists', 'error')
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()