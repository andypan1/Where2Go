from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

departCity = ""
arrivalCity = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getInputs', methods = ['POST'])
def getInputs():
    if request.method == 'POST':
        departCity = request.form.get('d')
        arrivalCity = request.form.get('a')
        getFlights()
    return('', 204)


# flights
def getFlights():
    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

    beginCity = {"query":departCity,"locale":"en-US"}
    endCity = {"query":arrivalCity, "locale":"en-US"}

    headers = {
        "x-rapidapi-key": "6c04748644mshcbbb06b9b2789bep1102b6jsneee9fc830bb9",
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=beginCity)
    response2 = requests.get(url, headers=headers, params=endCity)

    originCity = response.json()
    destCity = response2.json()

    




if __name__=='__main__':
   app.run()