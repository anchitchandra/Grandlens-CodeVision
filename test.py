from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pyrebase
from PIL import Image
from PIL.ExifTags import TAGS
import pathlib

app = Flask(__name__)

path = "tdb/tempdb"

config = {
    "apiKey": "AIzaSyBZwd4f0-GtoWyaBFazLggntOFs8DR-3v4",
    "authDomain": "consolegl.firebaseapp.com",
    "databaseURL": "https://consolegl-default-rtdb.firebaseio.com",
    "projectId": "consolegl",
    "storageBucket": "consolegl.appspot.com",
    "messagingSenderId": "633458672625",
    "appId": "1:633458672625:web:5eedbfda82fcc792b4ba50",
    "measurementId": "G-LR69XDCVQ3"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
tempiD = []
idforurl = []
sessionlogin = []


@app.route('/signup.html', methods=['POST', 'GET'])
def signup():
    email = ""
    paswd = ""
    msg = ""
    submit = ""
    if request.method == 'POST' or 'GET' and 'submit' in request.form:
        email = request.form.get('email')
        paswd = request.form.get('paswd')
        msg = request.form.get('msg')
        submit = request.form.get('submit')

        if email is None and paswd is None:
            msg = "Fill the form properly"

        else:
            try:
                msg = "Please confirm the verification email before login"
                try:
                    user = auth.create_user_with_email_and_password(email, paswd)
                    auth.send_email_verification(user['idToken'])
                    msg = "Email verification link sent!"
                    tempiD.append(user['idToken'])

                except:
                    msg = "email already exist!"

            except:
                msg = "error"

    return render_template('signup.html', email=email, paswd=paswd, msg=msg, submit=submit)


@app.route('/', methods=['POST', 'GET'])
@app.route('/1.html', methods=['POST', 'GET'])
def login():
    email = ""
    paswd = ""
    msg = ""
    submit = ""
    try:
        if request.method == 'POST' or 'GET' and 'submit' in request.form:
            email = request.form.get('email')
            paswd = request.form.get('paswd')
            msg = request.form.get('msg')
            submit = request.form.get('submit')
            try:
                info = auth.get_account_info(tempiD[0])
                print(info)
                last = info['users']
                infodict = dict(last[0])
                if infodict['emailVerified']:
                    auth.sign_in_with_email_and_password(email, paswd)
                    f = open(path, "a")
                    f.write(email + "\n")
                    f.close()
                    sessionlogin.append(email)
                    infodict.clear()
                    tempiD.clear()
                    return redirect(url_for('home', email=email))

            except:
                f = open(path, "r")
                file = f.read()
                f.close()
                files = list(file.strip().split("\n"))
                if email in files:
                    user = auth.sign_in_with_email_and_password(email, paswd)
                    msg = "login success"
                    sessionlogin.append(email)
                    idforurl.append(user['idToken'])

                    return redirect(url_for('home', email=email))
                else:
                    msg = "Email not verified"
    except:
        msg = "password wrong"

    return render_template('1.html', email=email, paswd=paswd, msg=msg, submit=submit)


# clearsessionlog dont forget bitch

@app.route('/2.html/<email>', methods=['POST', 'GET'])
def home(email):
    try:
        if email in sessionlogin:
            user = db.get()
            user = dict(user.val())
            x = list(user.keys())
            print(x)
            return render_template('2.html', u=x, email=email, user=user)

        else:
            return redirect(url_for('login'))
    except:
        return render_template('2.html', email=email)

@app.route('/3.html/<email>/<id>', methods=['POST', 'GET'])
def bigpic(email, id):
    if email in sessionlogin:
        name = email[0:6]
        u = db.child(id).get()
        nm = u.val()['name']
        title = u.val()['title']
        art = u.val()['description']
        date = u.val()['date']
        image = u.val()['image']
        aboutimg = u.val()['aboutImage']
        likescount = db.child(id).child('likes').get()
        likelist = list(likescount.val())
        likes = len(likelist)

        msg = ""
        key = u.key()

        if request.method == 'POST' or 'GET' and 'like' in request.form:
            if email in sessionlogin:
                if name in likelist:
                    db.child(id).child('likes').child(name).remove()
                    msg = "Unliked!"
                    likescount = db.child(id).child('likes').get()
                    likelist = list(likescount.val())
                    likes = len(likelist)
                else:

                    db.child(id).child('likes').child(name).set("true")
                    msg = "Liked!"
                    likescount = db.child(id).child('likes').get()
                    likelist = list(likescount.val())
                    likes = len(likelist)

                return render_template('3.html', nm=nm, title=title, art=art, date=date, image=image, key=key,
                                       likes=likes,
                                       msg=msg, aboutimg=aboutimg)
            else:
                return redirect(url_for('login'))
        return render_template('3.html', nm=nm, title=title, art=art, date=date, image=image, key=key, likes=likes,
                               msg=msg, aboutimg=aboutimg)
    else:

        return redirect(url_for('login'))


@app.route('/5.html/<email>', methods=['POST', 'GET'])
def write(email):
    nm = ""
    title = ""
    art = ""
    pub = ""
    msg = ""
    try:
        if email in sessionlogin:
            if request.method == 'POST' or 'GET' and 'pub' in request.form and request.files:
                nm = request.form.get('nm')
                title = request.form.get('title')
                art = request.form.get('art')
                pub = request.form.get('pub')
                msg = request.form.get('msg')
                image = request.files['image']
                now = datetime.now()

                if request.files:
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    name = str(email[0:6]) + "/" + str(email[0:6])
                    storage.child(name).put(image)
                    url = storage.child(name).get_url(idforurl[0])
                    aboutimg = imgverification(image)
                    if not aboutimg:
                        aboutimg = [
                            "Warning your Uploaded Image does not contains any meta data please check the Help! tab for errors!"]
                    nameb = email[0:6]
                    data = {"name": nm, "email": email, "title": title, "description": art, "date": dt_string, "image": url,
                            "aboutImage": aboutimg,
                            "likes": {"0": 0}}
                    db.child(nameb).set(data)
                    idforurl.clear()
                    msg = "Sexeffully uploaded"
                    #return redirect(url_for('home', email=email))
                else:
                    msg = "Image field is empty"
        else:
            return redirect(url_for('login'))
    except:
        msg = "There might br some error Please refresh the page"

    return render_template('5.html', nm=nm, title=title, art=art, pub=pub, msg=msg, email=email)



@app.route('/logout', methods=['POST', 'GET'])
def logout():
    sessionlogin.clear()
    return redirect(url_for('login'))


@app.route('/team.html', methods=['POST', 'GET'])
def team():
    return render_template('team.html')


@app.route('/help.html', methods=['POST', 'GET'])
def help():
    return render_template('help.html')


def imgverification(image):
    aboutimg = []
    my_img = Image.open(image)

    exif_data = my_img.getexif()

    for tagId in exif_data:
        tag = TAGS.get(tagId, tagId)
        data = exif_data.get(tagId)

        aboutimg.append(f"{tag:16}: {data}")
    return aboutimg




if __name__ == '__main__':
    app.run()
