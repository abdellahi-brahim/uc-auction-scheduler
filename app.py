from flask import Flask, request
from timer import Timer, TimerTask
from datetime import datetime
import requests

app = Flask(__name__)

app.config['END_AUCTION'] = "https://uc-auction.herokuapp.com/auctions/end"
app.config['GET_NEXT'] = "https://uc-auction.herokuapp.com/auctions/next"

timer = Timer()

class EndAuction(TimerTask):
    def run(self):
        #End Auction
        requests.post(url = app.config['END_AUCTION'])
        #Start Next Auction
        r = requests.get(url = app.config['GET_NEXT'])
        data = r.json()
        #reset timer to next auction
        timer.schedule(self, )
        

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Uc Auction Scheduler</h1>
    <p>It is currently set to{time}.</p>
    """.format(time=the_time)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    print(data['time'])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)