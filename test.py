from threading import Timer
from datetime import date, datetime

def hello():
    print("hello, Timer")

if __name__ == '__main__':
    time = datetime.strptime('2021-06-02 03:59:20.005939', '%Y-%m-%d %H:%M:%S.%f')
    diff = time - datetime.now()
    t = Timer(diff.total_seconds(), hello)
    t.start()