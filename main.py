from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ellen@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/')
def index():

    entries = Blog.query.order_by(desc(Blog.id)).all()

    return render_template('blog.html', entries=entries)



@app.route('/blog',methods= ['GET'])
def blogid():
    id = request.args.get('id')
    if id is None:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs = blogs)
    else:

        single_post = Blog.query.filter_by(id=id).first()
        print("individual=",single_post.title,single_post.body)
    return render_template('single_post.html', single_post=single_post)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title =request.form['title']
        body = request.form['body']

        error_title = ""
        error_body = ""

        if title == "" or body == "":
            error_title = "Must add a title"
            error_body = "Must add some text to the body"
            return render_template('newpost.html',title_error=error_title, body_error=error_body)
        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            id = new_post.id
            return redirect('/blog?id='+ str(id))
   
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()