from flask import Flask, render_template, redirect, url_for, request
from currentWeather.currentWeather import weatherAPICall

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home', methods=["GET", "POST"])
def home():
  if request.method == "POST":
    city = request.form.get("city")
    state = request.form.get("state")
    cityAndState = city + ", " + state

    try:
      weather = weatherAPICall(cityAndState)
      temp = weather.Temp
      tempUnit = weather.TempUnit
      return render_template('home.html', cityAndState=cityAndState, temp=temp, tempUnit=tempUnit)
    except Exception as e:  # Handle potential API errors
      error_message = f"Error fetching weather: {str(e)}"
      return render_template('home.html', cityAndState=cityAndState, error_message=error_message)
  else:
    # Set default values for initial page load (optional)
    cityAndState = "Chandler, AZ"
    weather = weatherAPICall(cityAndState)
    temp = weather.Temp
    tempUnit = weather.TempUnit
    return render_template('home.html', cityAndState=cityAndState, temp=temp, tempUnit=tempUnit)

