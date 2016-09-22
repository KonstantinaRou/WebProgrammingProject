from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request, Response
from flask import redirect
import tokenlib
import json
from sqlalchemy import update
from werkzeug import secure_filename
from flask import send_from_directory
from forms import ProfileForm, RegistrationForm
import os
import wolframalpha
from dicttoxml import dicttoxml
from werkzeug.exceptions import abort


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
super_duper_secret=app.config['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

wolframkey = app.config['WOLFRAM_KEY']
client = wolframalpha.Client(wolframkey)

db = SQLAlchemy(app)


@app.route("/")
def hello():
    return render_template("firstpage.html") # render_template giati mporw na perasw mesa dynamika metablites

@app.route("/register")
def  register(): 
    return render_template("registerV.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/profile/<username>")
def show_profile(username):
    name, surname = username.split('.')
    from models.users import Profile
    profile = db.session.query(Profile).filter_by(name=name, surname=surname).first()
    if profile is None:
        abort(404)
    if len(request.args) == 0 : 
        return render_template('index.html', profile=profile)
    token = request.args["token"]
    if token !="" :
        try:
            parsed_token = tokenlib.parse_token(token, secret=super_duper_secret)
            prof = db.session.query(Profile).filter_by(user_id=parsed_token['id']).first()
            from models.users import Message
            msg = db.session.query(Message).filter_by(user_to=parsed_token['id'])
            if (prof.name == name and prof.surname == surname):
                res = client.query('weather in Vilnius')
                return render_template('index.html', profile=profile , admin=True, weather=res.pods , message=msg)
            else :
                return render_template('index.html', profile=profile)
        except ValueError : 
            return render_template('index.html', profile=profile)


@app.route("/admin_page",methods=['POST','GET'])
def admin_page():
    if len(request.args) == 0 : 
        abort(404)
    token = request.args["token"]
    if token != "":
        try:
            parsed_token = tokenlib.parse_token(token, secret=super_duper_secret)
            from models.users import User
            user = db.session.query(User).filter_by(id=parsed_token['id'], admin=True).first()
            if user:
                users = db.session.query(User).all()
                return render_template('adminPage.html',users = users)
        except ValueError:
            pass
    abort(404)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

###### API ROUTES

@app.route("/api/edit_profile" , methods=['POST'])
def  edit_profile():
    name=request.form['name']
    surname=request.form['surname']
    birthdate=request.form['birthdate']
    website=request.form['website']
    address=request.form['address']
    telephone=request.form['telephone']
    description=request.form['description']
    token = request.form['token']
    parsed_token = tokenlib.parse_token(token, secret=super_duper_secret)
    user_id = parsed_token['id']

    from models.users import Profile
    profile=db.session.query(Profile).filter_by(user_id=user_id).first()
    if name!="":
        profile.name = name
        
    if surname !="":
        profile.surname=surname
        
        
    if birthdate !="":
        profile.birthdate=birthdate
        
        
    if website !="":
        profile.website=website
        
        
    if address !="":
        profile.address=address
        
       
    if telephone !="":
        profile.telephone=telephone
        
        
    if description !="":
        profile.description=description
        
    
    db.session.commit()    
    

    return json.dumps({
        "success" : True,
        "profile_url": "/profile/{0}.{1}".format(profile.name, profile.surname)
    })

@app.route("/api/register" , methods=['POST'])
def register_user(): 
    email = request.form['email']
    password = request.form['password']
    repassword = request.form['repassword']
    regform = RegistrationForm(email,password,repassword)
    errors=regform.validate()
    if find_userbyEmail(email) is not None:
        errors['email'] = "User with that email already exists."
    if errors:
        print(errors)
        return json.dumps({
                "success" : False,
                "errors" : errors
            })
    from models.users import User   
    newuser = User(email,password)
    print(newuser)
    db.session.add(newuser)
    db.session.commit()
    return json.dumps({
                "success" : True,
                "user_id" : newuser.id
            })

@app.route("/api/createProfile" , methods=['POST'])
def create_profile():
    user_id = request.form['user_id']
    name=request.form['name']
    surname=request.form['surname']
    birthdate=request.form['birthdate']
    website=request.form['website']
    address=request.form['address']
    telephone=request.form['telephone']
    description=request.form['description']
    profform = ProfileForm(name,surname,birthdate,website)
    errors = profform.validate()
    if errors:
        return json.dumps({
                'success': False,
                "errors" : errors 
            })
    from models.users import Profile
    image=""
    newProfile=Profile(user_id,name,surname,birthdate,website,address,telephone,description,image)
    db.session.add(newProfile)
    db.session.commit()
    return json.dumps({
        "success": True
        })

@app.route("/api/login" , methods=['POST'])
def login_user(): 
    email = request.form['email']
    password = request.form['password']
    errors = {}
    print (email,password)
    if find_userbyEmail(email) is not None:
        from models.users import User  
        user = db.session.query(User).filter_by(email=email).first()
        if user.password == password:
            token = tokenlib.make_token({"id": user.id , "admin":user.admin}, secret=super_duper_secret,timeout=60*60)
            from models.users import Profile 
            prof = db.session.query(Profile).filter_by(user_id=user.id).first()
            if user.admin == True:
                print("admin" ,user)
                return json.dumps({
                    "success" : True ,
                    "token" : token,
                    "profile_url": "/admin_page",
                    "errors":errors
                })
            print("Normal user" ,user)
            return json.dumps({
                "success" : True,
                "token" : token,
                "profile_url": "/profile/{0}.{1}".format(prof.name, prof.surname),
                "errors":errors
            })
        else:
            errors['password'] = "Incorrect password"
            return json.dumps({
            "success" : False,
            "errors" : errors
            })
    else:
        print("email and password worng")
        errors['email'] = "No user with this email exists"
        return json.dumps({
        "success" : False,
        "errors" :  errors
        })

def find_userbyEmail(email):
    from models.users import User
    exists = db.session.query(User.id).filter_by(email=email).first()
    print("Exists :",exists)
    return exists

@app.route("/api/deleteuser" , methods=['DELETE'])
def delete_user ():
    user_id = request.form['user_id']
    token = request.form['token']
    parsed_token = tokenlib.parse_token(token, secret=super_duper_secret)
    if parsed_token['admin']==True :
        from models.users import Profile
        profile=db.session.query(Profile).filter_by(user_id= user_id ).first()
        db.session.delete(profile)
        from models.users import User 
        user = db.session.query(User).filter_by(id= user_id ).first()
        db.session.delete(user)
        db.session.commit()
        return json.dumps({
            "success" : True
            })
    return "Error"

@app.route("/api/viewUser", methods=['POST'])
def view_user():
    user_id = request.form['user_id']
    token = request.form['token']
    parsed_token = tokenlib.parse_token(token, secret=super_duper_secret)
    if parsed_token['admin']==True :
        from models.users import Profile
        prof=db.session.query(Profile).filter_by(user_id= user_id ).first()
        return json.dumps({
                "success" : True,
                "profile_url": "/profile/{0}.{1}".format(prof.name, prof.surname)
            })


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/api/changeImage" ,methods=['POST'])
def upload_file():
    token = request.form['token']
    parsed_token = tokenlib.parse_token(token, secret=super_duper_secret)
    from models.users import Profile
    profile=db.session.query(Profile).filter_by(user_id= parsed_token['id']).first()
    file = request.files['newimage']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_url)
        profile.imageurl=filename
        db.session.commit()
        return file.filename



@app.route("/api/sendMessage", methods=['POST'])
def send_message():
    token = request.form["token"]
    print(token)
    if token is not None:
        try:
            parsed_token = tokenlib.parse_token(token, secret=super_duper_secret)
            if parsed_token['admin'] is None:
                return json.dumos({
                        "succress": False,
                        "errors": "User is not an admin"
                    })
            message = request.form['message']
            user_id = request.form['user_id']
            from models.users import Message
            from models.users import User
            if user_id is not None:
                admin = db.session.query(User).filter_by(admin=True).first()
                new_message = Message(user_id,admin.id,message)
                db.session.add(new_message)
                db.session.commit()
                return json.dumps({
                    "success" : True
                })
        except ValueError:
            pass
    return json.dumps({
        "success":False
        })





###
#
# WEB SERVICE SPECIFIC ROUTES 
#
###

@app.route("/service/profiles", methods=['GET'])
def list_profiles_xml():
    from models.users import Profile
    profiles = db.session.query(Profile).all()
    profiles_dict = [p.as_dict() for p in profiles] 
    return Response(dicttoxml(profiles_dict, custom_root="profiles"), mimetype='type/xml')

@app.route("/service/profile/<id>", methods=['GET'])
def profile_xml(id):
    from models.users import Profile
    profile = db.session.query(Profile).filter_by(user_id=id).first().as_dict()
    return Response(dicttoxml(profile, custom_root="profile"), mimetype='type/xml')


if __name__ == "__main__":
    app.run(debug=True)