# <b>ECE Senior Design mini project</b>
# <b>Mini Project S9</b></b>
# <b>Jacob Davis and Varun Lalwani</b>

# <u>Design</u>
## Introduction
 The Project's name is the World and its functionality is to display User's current location's temperature and humidity. It utilizes SSO from google sign in. The user can login from clicking the Login tab and he or she can logout from clicking the Logout tab. If a user is not logged in and tries to click on the Temperature or Humidity tab, then he or she gets redirected to the Login tab. After Logging in, the user can access the information on the temperature and the humidity tab. The project allows the user to add and delete a sensor. The user can also monitor the current output from the sensor. The project also allows to search a location's current temperature and humidity. To implement this web app, we chose to use Python Flask.

## SSO using Google Authentication
For Authentication, we followed the article by Matt Button. For Authentication, we made a separate python file which consisted of a login page, authentication page, check if logged in function, get user credentials function and a logout page. The result of login and logout redirects the user to the home page. For login we use OAuth2Session. At the start of each webpage, except for home page, we verify whether the user is signed in or not. If the user is not signed in and on a webpage that requires the user to be signed in, then the user gets directed to login in page. To save a user after sign in, we store user's hashed id on a Flask Session. Then to check if the user is logged in, we check if a hashed id is present in Flask Session or not.

## Cloud Platform and Database:
This web app uses a PostgreSQL database, which is hosted on Heroku's Cloud, and the program interacts with the cloud database by using SQLAlchemy on flask. We monitor the performance of the database by using Adminer. The Database consists of 2 classes: User and Sensor. The User is in relation with sensor. The User class has 3 Columns: Uid(Private Key), email(Unique)and name. The Sensor class has 4 Columns: Sid(Private Key), Name, Sensor Type and User_id. The Database is accessed every time when the user tries to add sensor, delete a sensor or list all the Sensors. A sensor can only be a temperature type or humidity type. The web app, prevents deleting a sensor that is not on the database and prevents adding a sensor, if it is already present in the database.

## User's Current Location
For Getting User's current location, we tried to get user's location in terms of Latitude and Longitude, we were able to do this by using the article by Google Maps Platform on Geolocation.

## Get the current Location's weather
To get the current location's weather we use OpenWeatherAPI. This API uses city name or latitude and longitude to extract weather from the API. The OpenWeatherAPI is utilized by current location weather and Find a location's weather.

## Temperature and Humidity simulation
To stimulate the sensors, we used Server Sent Events. This allowed us to send real-live, random valued data to the web app, which in a way helped us to stimulate the sensors. The SSE starts working when the user reaches a web page which is meant to display the weather, so we don't store any previous history. If we had real sensors, we would have stored the real readings from the sensor into the databse, by making another class called, weather, which would be in relation with a sensor and would store timestamp, reading value and sensor id.

# Testing
1) Open the app on localhost:5000<br>
2) Clicking on home should keep you at home<br>
3) Clicking on Temperature should take you to login Page if the user is not logged in, else should show a list of buttons<br>
4) Clicking on Humidity should take you to login Page if the user is not logged in, else should show a list of buttons<br>
5) Clicking on the Login tab, should redirect the user to the login page.<br>
6) Clicking on the Logout tab, Logout the user, i.e. clicking on the temperature tab should redirect user to login Page<br>
7) After Logging in or out, the user should get redirected to the home Page<br><br>
Inside the Temperature tab:<br>
8) Clicking on current location should redirect the user to a temporary page, that will show users latitude and longitude and then will redirect to a page that will show he temperature at user's current location.<br>
9) Clicking on Let's go back button, redirects the user back to inside of temperature tab<br>
10) Clicking on Find a Location button, redirects the user to a page that has a input bar and a choose button.<br>
11) Entering a invalid city name and then clicking choose button will result in changing on headline, which says that the weather information is unavailable for the city<br>
12) Entering a valid city name and then clicking choose button will redirect the user to a page with a graph of weather and a let's go back buttons<br>
13) Clicking on Let's go back button, redirects the user back to inside of temperature tab<br>
14) Clicking on show all sensor's button would redirect to a page. The page will say that the user has no temperature sensor, if the user doesn't has any sensors, else the page will show all the temperature sensors that the user has.<br>
15) Clicking on Let's go back button, redirects the user back to inside of temperature tab<br>
16) Clicking on any of the sensors listed should redirect to the graph page, that will show the simulated sensor's output and keep updating.<br>
17) Clicking on Let's go back button, redirects the user back to inside of temperature sensors option<br>
18) Clicking on add a sensor button should redirect the user to web page with a text box, an approve button and a let's go back button<br>
19) Entering a Unique sensor name and clicking should add a sensor, which can be seen added in the show all sensors button.<br>
20) Entering an Existing sensor name and clicking should say that the sensor already exists.<br>
21) Just clicking on approve should say please fill out the field<br>
22) Clicking on a let's go back button, should redirect the user to inside of temperature tab<br>
23) Clicking on delete a sensor button should redirect the user to web page with a text box, an approve button and a let's go back button<br>
24) Entering a Existing sensor name and clicking should delete a sensor, which can be seen deleted in the show all sensors button.<br>
25) Entering an Unique sensor name and clicking should say that the sensor doesn't exists.<br>
26) Just clicking on approve should say please fill out the field<br>
27) Clicking on a let's go back button, should redirect the user to inside of temperature tab<br><br>
Inside the Humidity tab:<br>
28) Clicking on current location should redirect the user to a temporary page, that will show users latitude and longitude and then will redirect to a page that will show he humidity at user's current location.<br>
29) Clicking on Let's go back button, redirects the user back to inside of humidity tab<br>
30) Clicking on Find a Location button, redirects the user to a page that has a input bar and a choose button.<br>
31) Entering a invalid city name and then clicking choose button will result in changing on headline, which says that the weather information is unavailable for the city<br>
32) Entering a valid city name and then clicking choose button will redirect the user to a page with a graph of weather and a let's go back buttons<br>
33) Clicking on Let's go back button, redirects the user back to inside of humidity tab<br>
34) Clicking on show all sensor's button would redirect to a page. The page will say that the user has no humidity sensor, if the user doesn't has any sensors, else the page will show all the humidity sensors that the user has.<br>
35) Clicking on Let's go back button, redirects the user back to inside of humidity tab<br>
36) Clicking on any of the sensors listed should redirect to the graph page, that will show the simulated sensor's output and keep updating.<br>
37) Clicking on Let's go back button, redirects the user back to inside of humidity sensors option<br>
38) Clicking on add a sensor button should redirect the user to web page with a text box, an approve button and a let's go back button<br>
39) Entering a Unique sensor name and clicking should add a sensor, which can be seen added in the show all sensors button.<br>
40) Entering an Existing sensor name and clicking should say that the sensor already exists.<br>
41) Just clicking on approve should say please fill out the field<br>
42) Clicking on a let's go back button, should redirect the user to inside of humidity tab<br>
43) Clicking on delete a sensor button should redirect the user to web page with a text box, an approve button and a let's go back button<br>
44) Entering a Existing sensor name and clicking should delete a sensor, which can be seen deleted in the show all sensors button.<br>
45) Entering an Unique sensor name and clicking should say that the sensor doesn't exists.<br>
46) Just clicking on approve should say please fill out the field<br>
47) Clicking on a let's go back button, should redirect the user to inside of humidity tab<br>

# Verification
<b>The Verification and the app's working can be seen in the video</b>.<br>
[![miniProject](http://img.youtube.com/vi/bgZEMIuj84Y/0.jpg)](http://www.youtube.com/watch?v=bgZEMIuj84Y "EC 463 S9 MiniProject Demonstration")<br>

# Replicate Work
Make sure to have Python 3.7.4 and pip up to date.<br>
Perform pip install -r requirements. If any of the libraries do not get installed, then it's better to google the problem and see why the platform is unable to perform installation.<br>
Then perform <b>python hello.py</b> on the command prompt.<br>
Open localhost:5000 on browser.<br>

# Contribution
Varun Lalwani: Google Sign in SSO authentication, Getting user's current Location, getting current location's weather, The webapp's UI and backend, initializing a cloud based database, making all buttons and their redirects, making all the graphs, the app's functionality and design, the readme documentation, Using Server Sent Events in the code for sensor simulation and Testing and Verification.<br>
Jacob Davis: Hosting the app on the AWS cloud. (Unfortunately, the app couldn't perform google sign when hosted on cloud and a lot of complications happened, so we couldn't include in the end)<br>

# Links:
[Link for SSO](https://www.mattbutton.com/2019/01/05/google-authentication-with-python-and-flask/)<br>
[Link for Getting Started with Flask](https://www.youtube.com/watch?v=MwZwr5Tvyxo)<br>
[Link for Getting Started with Heroku and Database](https://docs.cs50.net/web/2018/x/projects/1/project1.html)<br>
[Link for Current Location](https://developers.google.com/maps/documentation/javascript/geolocation)<br>
[Link for Server Sent Events](https://blog.easyaspy.org/post/10/2019-04-30-creating-real-time-charts-with-flask)

# APIs
OpenWeatherAPI<br>
Google OAuth APIs<br>
Google Maps API for Geolocation<br>
