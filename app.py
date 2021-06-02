from flask import Flask, request, jsonify
from threading import Timer
from datetime import datetime, timezone
from dateutil import parser as date_parser
import requests

app = Flask(__name__)
#Some global vars
app.config['end'] = "https://uc-auction.herokuapp.com/auctions/end"
app.config['next'] = "https://uc-auction.herokuapp.com/auctions/next"
app.config['next_date'] = None
app.config['timer'] = None

#Cancels timer and sets it to time_str
def reset_timer(time_str):
    app.config['timer'].cancel()
    set_timer(time_str)

#Set timer to time_str datetime
def set_timer(time_str):
    app.config['next_date'] = date_parser.parse(time_str)
    diff = app.config['next_date'] - datetime.now(timezone.utc)
    app.config['timer'] = Timer(diff.total_seconds(), end_auctions)
    app.config['timer'].start()

#Sends request to end auction and gets next auction to end
def end_auctions():
    print("Ending Auctions...")
    #Send Request to end auctions
    requests.post(app.config.get('end'))
    r = requests.get(app.config.get('next'))
    data = r.json()
    #Reset Scheduler to Next Scheduler Date
    if data['next'] != "no auction selected":
        set_timer(data['next'])
    else:
        app.config['next_date'] = None

#Shows When Next Auction Ending is Going to Happen
@app.route('/')
def homepage():
    if app.config['next_date'] == None:
        return """
        <h1>Uc Auction Scheduler</h1>
        <p>No Auction Ending Scheduled.</p>
        """
    return """
    <h1>Uc Auction Scheduler</h1>
    <p>It is currently set to {time}.</p>
    """.format(time=app.config['next_date'])

#Endpoint to update next ending scheduled remotly
@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    date = date_parser.parse(data['time'])
    
    #No Scheduler set, set timer
    if app.config['next_date'] is None:
        set_timer(data['time'])

    #Scheduler set, reset timer
    if date < app.config['next_date'] and date > datetime.now(timezone.utc):
        reset_timer(data['time'])
    
    return jsonify({"message": f" Scheduled to {app.config.get('next_date')}"})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)