from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FindForm(FlaskForm):
    CityName = StringField('City Name', validators=[DataRequired()])
    submit = SubmitField('Choose')

class CurrentLocationForm(FlaskForm):
    Lat = StringField('Latitude', validators=[DataRequired()])
    Long = StringField('Longitude', validators=[DataRequired()])
    submit = SubmitField('You Sure?')

class AddSensorForm(FlaskForm):
    SensorName = StringField('Sensor\'s Name', validators=[DataRequired()])
    submit = SubmitField('Approve')


#<script>
#TESTER = document.getElementById('tester');
#Plotly.plot( TESTER, [{
#x: [1, 2, 3, 4, 5],
#y: [1, 2, 4, 8, 16] }], {
#margin: { t: 1 } } );
#</script>
