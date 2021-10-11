from flask import Flask, render_template, url_for, session, redirect, request, Response
from flask_sqlalchemy import SQLAlchemy
import pygeoip
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
import string
import google_auth
import random
import requests
import json
import socket
from all_forms import FindForm, CurrentLocationForm, AddSensorForm
import datetime as dt
import plotly
from datetime import datetime
import time


app = Flask(__name__)
app.secret_key = 'Viku'
ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE ='openid email profile'

AUTH_REDIRECT_URI ='http://localhost:5000/auth'
BASE_URI = 'http://localhost:5000'
CLIENT_ID = '136055742959-bhmdvt7dpkf4c24en3hjd6d39unftbu6.apps.googleusercontent.com'
CLIENT_SECRET = '3S4TvoNl3VWnGvSiRc_1ciDk'

AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

IP_STACK_CLIENT_ID = '993a50ff836063dd477d3a5c57a952f0'
WEATHER_CLIENT_ID = '19a4d990cefbc675dd5dd56c82781454'
weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"
SQLALCHEMY_DATABASE_URI = "postgres://tqvihewxklkiup:f89206c0773f7cbd6949af5c4ae83486d65f523b772e9ce560dc00d5c0cf3dde@ec2-54-243-47-196.compute-1.amazonaws.com:5432/d543h31a176rsd"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
random.seed()
db = SQLAlchemy(app)


app.register_blueprint(google_auth.app)
#geo = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    sensors = db.relationship('Sensor', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Sensor(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    sensor_type = db.Column(db.Boolean, nullable = False)#True for Temperature and False for Humidity
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)

    def __repr__(self):
        return f"User('{self.name}')"

#class Quantity(db.Model):
#    qid = db.Column(db.Integer,)

@app.route("/")
@app.route("/home")
def home():
    if google_auth.is_logged_in():
        information = google_auth.get_user_info()
        email = information['email']
        name = information['name']
        if not(User.query.filter_by(email=email).first()):
            user = User(email=email,name=name)
            db.session.add(user)
            db.session.commit()
    return render_template('home.html')


@app.route("/temperature")
def temperate():
    if google_auth.is_logged_in():
        #user_info = google_auth.get_user_info()
        client_ip = request.remote_addr
        #geo_data = geo.record_by_addr(client_ip)
        return render_template('temperature.html', title='Temperature')
        #str = "/temperature"
    return redirect('/login')


@app.route("/humidity")
def humid():
    if google_auth.is_logged_in():
        #user_info = google_auth.get_user_info()
        client_ip = request.remote_addr
        #geo_data = geo.record_by_addr(client_ip)
        return render_template('humidity.html', title='Humidity', client_ip=client_ip)
    return redirect('/login')


@app.route("/temperature/current", methods=['GET', 'POST'])
def temp_current():
    if google_auth.is_logged_in():
        form = CurrentLocationForm()
        if form.validate_on_submit():
            text1 = request.form['Lat']
            text2 = request.form['Long']
            complete_weather_request = weather_base_url + "appid=" + WEATHER_CLIENT_ID + "&lat=" + text1 + "&lon=" + text2
            response = requests.get(complete_weather_request)
            response_format = response.json()
            returner = '/temperature'
            if response_format['cod'] != "404":
                rep = response_format['main']
                found = rep["temp"] - 273.15
                result = 'The Temperature at your location is ' + str(round(found)) + ' degree celcius'
                return render_template('current.html', title='Current Temperature', result=result, returner=returner)
            else:
                result = 'The Weather is currently unavailable for your location'
                return render_template('current.html', title='Current Error', result=result, returner=returner)
        else:
            return render_template('current.html',title = 'Current Temperature', form = form)
    else:
        return redirect('/login')


@app.route("/humidity/current", methods=['GET', 'POST'])
def humid_current():
    if google_auth.is_logged_in():
        form = CurrentLocationForm()
        if form.validate_on_submit():
            text1 = request.form['Lat']
            text2 = request.form['Long']
            complete_weather_request = weather_base_url + "appid=" + WEATHER_CLIENT_ID + "&lat=" + text1 + "&lon=" + text2
            response = requests.get(complete_weather_request)
            response_format = response.json()
            returner = '/humidity'
            if response_format['cod'] != "404":
                rep = response_format['main']
                found = rep["humidity"]
                result = 'The Humidity at your current location is ' + str(found) +'%'
                return render_template('current.html', title='Current Humidity', result=result, returner=returner)
            else:
                result = 'The Weather is currently unavailable for your location'
                return render_template('current.html', title='Current Error', result=result, returner=returner)
        else:
            return render_template('current.html',title = 'Current Humidity', form = form)
    else:
        return redirect('/login')


@app.route("/temperature/find", methods=['GET', 'POST'])
def temp_find():
    if google_auth.is_logged_in():
        form = FindForm()
        if form.validate_on_submit():
            graphs = []
            text = request.form['CityName']
            complete_weather_request = weather_base_url + "appid=" + WEATHER_CLIENT_ID + "&q=" + text
            response = requests.get(complete_weather_request)
            response_format = response.json()
            #print(response_format)
            if response_format['cod'] != "404":
                noun = 'temperature'
                returner = '/temperature'
                current_hour = dt.datetime.today().hour
                rep = response_format['main']
                found = rep["temp"] - 273.15

                # Making the input for the graph
                graphs.append(dict(data=[dict(\
                x=[current_hour-11, current_hour-10, current_hour-9,\
                current_hour-8, current_hour-7, current_hour-6, current_hour-5,\
                current_hour-4, current_hour-3, current_hour-2, current_hour-1, current_hour],\
                y=[found, found*0.95, found - 4, found*1.1, found*1.3,\
                found + 3, found + 4, found * 1.15, found*0.8, found*0.8,\
                found*0.93, found], type='line'),],layout=dict(title='Temperature')),)

                ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
                graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
                print(len(graphs))
                print(len(ids))
                return render_template('result.html', title='Result', text=text, noun=noun, returner=returner, ids=ids, graphJSON=graphJSON)
            else:
                reporter = 'The Weather is currently unavailable for ' + text
                return render_template('t_find.html', title='Find a Location', form = form, reporter=reporter)
        else:
            return render_template('t_find.html', title='Find a Location', form = form)
    else:
        return redirect('/login')


@app.route("/humidity/find", methods=['GET', 'POST'])
def humid_find():
    if google_auth.is_logged_in():
        form = FindForm()
        if form.validate_on_submit():
            graphs = []
            text = request.form['CityName']
            complete_weather_request = weather_base_url + "appid=" + WEATHER_CLIENT_ID + "&q=" + text
            response = requests.get(complete_weather_request)
            response_format = response.json()
            if response_format["cod"] != "404":
                noun = 'humidity'
                returner = '/humidity'
                current_hour = dt.datetime.today().hour
                rep = response_format['main']
                found = rep['humidity']

                # Making the input for the graph
                graphs.append(dict(data=[dict(\
                x=[current_hour-11, current_hour-10, current_hour-9,\
                current_hour-8, current_hour-7, current_hour-6, current_hour-5,\
                current_hour-4, current_hour-3, current_hour-2, current_hour-1, current_hour],\
                y=[found, found*0.95, found - 4, found*1.1, found*1.3,\
                found + 3, found + 4, found * 1.15, found*0.8, found*0.8,\
                found*0.93, found], type='line'),],layout=dict(title='Humidity')),)

                ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
                graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
                return render_template('result.html', title='Result', text=text, noun=noun, returner=returner, ids=ids, graphJSON=graphJSON)
            else:
                reporter = 'The Weather is currently unavailable for the previously searched City.'
                return render_template('h_find.html', title='Find a Location', form = form, reporter=reporter)
        else:
            return render_template('h_find.html', title='Find a Location', form = form)
    else:
        return redirect('/login')

@app.route("/temperature/add", methods=['GET', 'POST'])
def temp_add():
    if google_auth.is_logged_in():
        form = AddSensorForm()
        acting = 'add'
        if form.validate_on_submit():
            sensor_name = request.form['SensorName']
            information = google_auth.get_user_info()
            sensor_user_email = information['email']
            sensor_user = User.query.filter_by(email=sensor_user_email).first()
            if not(Sensor.query.filter_by(sensor_type=True, name=sensor_name, user_id=sensor_user.uid).first()):
                temp_sensor = Sensor(name=sensor_name, sensor_type=True, user_id=sensor_user.uid)
                db.session.add(temp_sensor)
                db.session.commit()
                reporter ='You have successfully added the sensor: ' + sensor_name
                returner = '/temperature'
                return render_template('add.html', title='Add Temperature Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
            else:
                reporter = 'The sensor: ' + sensor_name + ' already exits'
                returner = '/temperature'
                return render_template('add.html', title='Add Temperature Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
        else:
            return render_template('add.html', title='Add Temperature Sensor', form=form, acting=acting, returner='/temperature')
    else:
        return redirect('/login')


@app.route("/humidity/add", methods=['GET', 'POST'])
def humid_add():
    if google_auth.is_logged_in():
        form = AddSensorForm()
        acting = 'add'
        if form.validate_on_submit():
            sensor_name = request.form['SensorName']
            information = google_auth.get_user_info()
            sensor_user_email = information['email']
            sensor_user = User.query.filter_by(email=sensor_user_email).first()
            if not(Sensor.query.filter_by(sensor_type=False, name=sensor_name, user_id=sensor_user.uid).first()):
                temp_sensor = Sensor(name=sensor_name, sensor_type=False, user_id=sensor_user.uid)
                db.session.add(temp_sensor)
                db.session.commit()
                reporter ='You have successfully added the sensor: ' + sensor_name
                returner = '/humidity'
                return render_template('add.html', title='Add Humidity Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
            else:
                reporter = 'The sensor: ' + sensor_name + ' already exits'
                returner = '/humidity'
                return render_template('add.html', title='Add Humidity Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
        else:
            return render_template('add.html', title='Add Humidity Sensor', form=form, acting=acting, returner='/humidity')
    else:
        return redirect('/login')

@app.route("/temperature/delete", methods=['GET', 'POST'])
def temp_delete():
    if google_auth.is_logged_in():
        form = AddSensorForm()
        acting = 'delete'
        if form.validate_on_submit():
            sensor_name = request.form['SensorName']
            information = google_auth.get_user_info()
            sensor_user_email = information['email']
            sensor_user = User.query.filter_by(email=sensor_user_email).first()
            if Sensor.query.filter_by(sensor_type=True, name=sensor_name, user_id=sensor_user.uid).first():
                Sensor.query.filter_by(sensor_type=True, name=sensor_name, user_id=sensor_user.uid).delete()
                db.session.commit()
                reporter ='You have successfully deleted the sensor: ' + sensor_name
                returner = '/temperature'
                return render_template('add.html', title='Delete Temperature Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
            else:
                reporter = 'The sensor: ' + sensor_name + ' does not exits'
                returner = '/temperature'
                return render_template('add.html', title='Delete Temperature Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
        else:
            return render_template('add.html', title='Delete Temperature Sensor', form=form, acting=acting, returner='/temperature')
    else:
        return redirect('/login')

@app.route("/humidity/delete", methods=['GET', 'POST'])
def humid_delete():
    if google_auth.is_logged_in():
        form = AddSensorForm()
        acting = 'delete'
        if form.validate_on_submit():
            sensor_name = request.form['SensorName']
            information = google_auth.get_user_info()
            sensor_user_email = information['email']
            sensor_user = User.query.filter_by(email=sensor_user_email).first()
            if Sensor.query.filter_by(sensor_type=False, name=sensor_name, user_id=sensor_user.uid).first():
                Sensor.query.filter_by(sensor_type=False, name=sensor_name, user_id=sensor_user.uid).delete()
                db.session.commit()
                reporter ='You have successfully deleted the sensor: ' + sensor_name
                returner = '/humidity'
                return render_template('add.html', title='Delete Humidity Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
            else:
                reporter = 'The sensor: ' + sensor_name + ' does not exits'
                returner = '/humidity'
                return render_template('add.html', title='Delete Humidity Sensor', form=form, acting=acting, reporter=reporter, returner=returner)
        else:
            return render_template('add.html', title='Delete Humidity Sensor', form=form, acting=acting, returner='/humidity')
    else:
        return redirect('/login')

@app.route("/temperature/saved")
def temp_saved():
    if google_auth.is_logged_in():
        temp_sensor_list = []
        if (Sensor.query.filter_by(sensor_type=True).first()):
            sensors = Sensor.query.filter_by(sensor_type=True).all()
            for sensor in sensors:
                temp_sensor_list.append(sensor.name)
            return render_template('t_lister.html', title='Temperature List', sensor_list=temp_sensor_list)
        else:
            reporter = "You have no Sensors"
            return render_template('t_lister.html', title='Temperature List', reporter=reporter)
    else:
        return redirect('/login')

@app.route("/humidity/saved")
def humid_saved():
    if google_auth.is_logged_in():
        humid_sensor_list = []
        if (Sensor.query.filter_by(sensor_type=False).first()):
            sensors = Sensor.query.filter_by(sensor_type=False).all()
            for sensor in sensors:
                humid_sensor_list.append(sensor.name)
            return render_template('h_lister.html', title='Humidity List', sensor_list=humid_sensor_list)
        else:
            reporter = "You have no Sensors"
            return render_template('h_lister.html', title='Humidity List', reporter=reporter)
    else:
        return redirect('/login')

@app.route("/temperature/plot")
def temp_display():
    if google_auth.is_logged_in():
        return render_template('t_end.html',title='Temperature Plot', returner='/temperature/saved')
    else:
        return redirect('/login')

@app.route("/humidity/plot")
def humid_display():
    if google_auth.is_logged_in():
        return render_template('h_end.html',title='Humidity Plot', returner='/humidity/saved')
    else:
        return redirect('/login')

@app.route("/Temp_Data_Plotter")
def temp_data():
    def temperate_data():
        while True:
            data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.uniform(-1,1) * 5 + 22.5})
            yield f"data:{data}\n\n"
            time.sleep(1)

    return Response(temperate_data(), mimetype='text/event-stream')

@app.route("/Humid_Data_Plotter")
def humid_data():
    def humidity_data():
        while True:
            data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': (random.uniform(-1,1) * 29 + 71)})
            yield f"data:{data}\n\n"
            time.sleep(1)

    return Response(humidity_data(), mimetype='text/event-stream')

#def is_logged_in():
#    return True if AUTH_TOKEN_KEY in session else False


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
