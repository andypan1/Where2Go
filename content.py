from flask import Flask, request, render_template, jsonify
from datetime import date
from dateutil.relativedelta import relativedelta
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
        getFlights(departCity, arrivalCity)
        getHotels(arrivalCity)
    return('', 204)

@app.route()
def returnFlights():
    pass


# flights
prices = []
origin = []
dest = []
departTime = []
arriveTime = []
duration = []
numStops = []
airlineName = []
airlineURL = []

def getFlights(departCity, arrivalCity):
    current_date = date.today()
    new_date = current_date + relativedelta(months=2)
    return_date = new_date + relativedelta(days=7)

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

    firstOrigin = originCity["data"][0]
    firstDest = destCity["data"][0]

    flightsURL = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlights"
    queryString = {"originSkyId": firstOrigin["skyId"],
                   "destinationSkyId":firstDest["skyId"],
                   "originEntityId":firstOrigin["entityId"],
                   "destinationEntityId":firstDest["entityId"],
                   "date":new_date,
                   "returnDate":return_date,
                   "sortBy":"best",
                   "currency":"USD",
                   "market":"en-US",
                   "countryCode":"US"}

    flightResponse = requests.get(flightsURL, headers=headers, params=queryString)
    
    num = len(flightResponse)
    if len(flightResponse > 4):
        num = 4

    for x in range(0, num):
        prices.append(flightResponse["data"]["itineraries"][x]["price"]["raw"])

        #departing flight (0, 2, 4, 6) MAX
        origin.append(flightResponse["data"]["itineraries"][x]["legs"][0]["origin"]["id"])
        dest.append(flightResponse["data"]["itineraries"][x]["legs"][0]["destination"]["id"])
        departTime.append(flightResponse["data"]["itineraries"][x]["legs"][0]["departure"][11:16])
        arriveTime.append(flightResponse["data"]["itineraries"][x]["legs"][0]["arrival"][11:16])
        duration.append(flightResponse["data"]["itineraries"][x]["legs"][0]["durationInMinutes"])
        numStops.append(flightResponse["data"]["itineraries"][x]["legs"][0]["stopCount"])
        airlineName.append(flightResponse["data"]["itineraries"][x]["legs"][0]["carriers"]["marketing"][0]["name"])
        airlineURL.append(flightResponse["data"]["itineraries"][x]["legs"][0]["carriers"]["marketing"][0]["logoUrl"])

        #returning flight (1, 3, 5, 7) MAX
        origin.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["origin"]["id"])
        dest.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["destination"]["id"])
        departTime.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["departure"][11:16])
        arriveTime.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["arrival"][11:16])
        duration.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["durationInMinutes"])
        numStops.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["stopCount"])
        airlineName.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["carriers"]["marketing"][0]["name"])
        airlineURL.append(flightResponse["data"]["itineraries"][x]["legs"][len(flightResponse["data"]["itineraries"][x]["legs"]) - 1]["carriers"]["marketing"][0]["logoUrl"])




#hotels

def getHotels(arrivalCity):
    pass


if __name__=='__main__':
   app.run()