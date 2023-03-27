# itlyavhtmkmcxdcm

from flask import Flask,Response
from flask import render_template, request, redirect, session
import flask
import io
import requests
import pymongo
import pyshorteners
import qrcode
import random
from flask_mail import Mail,Message
import string
import datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_qrcode import QRcode


app = Flask(__name__)
qrcode = QRcode(app)
globalmylink = ''
app.secret_key = 'ihyfhbhbfrfbiihrewuibwe5436889'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='greentokennotification@gmail.com',
    MAIL_PASSWORD='wbwtiwlicoapawtx'
)
mail = Mail(app)



@app.route('/')
def index():  

    return render_template('index.html')


# @app.route('/qrcode/<data>')
# def generate_qrcode(data):
#     return qrcode(data, mode='raw')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        select =  request.form.get('select')
        email  = request.form.get('email')
        reminder = request.form.get('reminder')
        myrandomnumber = random.randint(50,200)
        length = myrandomnumber

        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for i in range(length))

        
        if select=='qr':
            client = pymongo.MongoClient('mongodb+srv://admin:xCpk78QPj9kQas8p@cluster0.snmuuol.mongodb.net/test')
            db = client['GreenToken']
            collection = db['qr']
            imformation_dictionary = {
                'Email':email,
                'Reminder':reminder,
                'Blob':random_string
            }
            collection.insert_one(imformation_dictionary)


            link1 = 'http://127.0.0.1:5000/q?sajsnbakdjkbfjbdzdbweuifbwdnadn=' + random_string
            
            s = pyshorteners.Shortener()

            # shorten a URL
            link1 = s.tinyurl.short(link1)
            
           



            return render_template('generate.html',link=link1)
    else:
        return redirect('/')
    return render_template('index.html')

def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    data = response.json()
    if data["type"] == "single":
        joke = data["joke"]
    else:
        joke = f"{data['setup']} {data['delivery']}"
    return joke


client = pymongo.MongoClient('mongodb+srv://admin:xCpk78QPj9kQas8p@cluster0.snmuuol.mongodb.net/test')
db = client['GreenToken']
collection = db['qr']   


@app.route('/q', methods=['GET', 'POST'])
def q():
    headers_dict = dict(request.headers)
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']
   
    
    
    name = request.args.get('sajsnbakdjkbfjbdzdbweuifbwdnadn')
    result = collection.find_one({'Blob':name})
    recipient = result['Email']
    reminder = result['Reminder']





    url = f'http://ip-api.com/json/{ip_address}'

    response = requests.get(url)
    data = response.json()

    # print(f"Location for {ip_address}: {data['city']}, {data['regionName']}, {data['country']}")







    msg = Message('GreenToken Triggered',sender='greentokennotification@gmail.com', recipients=[recipient])
    msg.html = f'''
    <!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>CanaryToken Email</title>
</head>
<body>
    <table cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td style="background-color: #f5f5f5; padding: 20px;">
                <table cellpadding="0" cellspacing="0" align="center" width="600">
                    <tr>
                        <td style="text-align: center; padding-bottom: 20px;">
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #ffffff; padding: 40px;">
                            <h1 style="font-size: 24px; margin-bottom: 20px;">GreenToken Triggered</h1>
                            <p style="font-size: 16px; margin-bottom: 40px;">An HTTP Canarytoken has been triggered by
                                the Source IP {ip_address}.</p>
                            <h1 style="font-size: 24px; margin-bottom: 20px;">Basic Details:</h1>
                            <table cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="background-color: #f5f5f5; padding: 20px;">
                                        <table cellpadding="0" cellspacing="0" align="center" width="600">
                                            <tr>
                                                <td style="text-align: center; padding-bottom: 20px;">
                                                    <img src="https://raw.githubusercontent.com/GreeenCat/MyPPTs/main/croped.png" alt="GreenToken" style="width:15em">
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="background-color: #ffffff; padding: 40px;">
                                                    <table cellpadding="0" cellspacing="0" style="font-size: 16px;   border: 1px solid black;
  border-collapse: collapse;">
                                                        <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                Channel</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">HTTP
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">Time
                                                            </td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                {datetime.datetime.now()} (UTC)</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                Canarytoken</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                {name}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                Token Reminder</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                {reminder}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                Token Type</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                qr_code</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                Source IP</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                {ip_address}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">User
                                                                Agent</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                {headers_dict['User-Agent']}</td>
                                                        </tr>




 <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">Accept-Language</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                {headers_dict['Accept-Language']}</td>
                                                        </tr>

                                                       

                                                          <tr>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">Expected Location</td>
                                                            <td style="padding: 5px 10px; border: 1px solid black;">
                                                                {data['city']}, {data['regionName']}, {data['country']}</td>
                                                        </tr>




                                                    </table>
                                                </td>
                                            </tr>
                                            <tr>

                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            <br>
                            <a href="mailto:greentokennotification@gmail.com?subject=Help Regarding GreenToken"
                                style="background-color: green; color: #ffffff; display: inline-block; font-size: 16px; padding: 10px 20px; text-decoration: none;">Contact
                                Support</a>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: green; color: #ffffff; padding: 20px; text-align: center;">
                            <p style="font-size: 14px; margin-bottom: 0;">&copy; 2023 GreenToken. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>
    
    '''
    mail.send(msg)
    # mail.send_message('Organization Permisson', sender='greentokennotification@gmail.com', recipients=[recipient], body="Token triggered")
    
    return render_template('slogan.html',joke=get_joke())


app.run(debug=True)
