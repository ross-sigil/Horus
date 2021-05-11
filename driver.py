# IMPORTS
import pandas as pd
import math
import os.path
import time
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook #(Optional, used for progress-bars)
from os import path
import smtplib 
import emoji
import json
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#Settings stuff
email = "metatron@waifu.club"
pas = "praisetheprofit"
gateway = '6189324037@mms.cricketwireless.net'
smtp = "mail.cock.li" 
port = 587

dt = datetime.now()

### API
binance_api_key = '[6TkIhnXqMyXv65eAfpxMpq2OGvd4y7qwKO5joAPMkBmddLZqIF2pxOgd5lxlV3Zp]'    #Enter your own API-key here
binance_api_secret = '[CwOtLOtgUWA1z3TF7lPQXxpucTnwxfX473yY33Ux3FQzFq8FvdAEsggGXo5hmpZ8]' #Enter your own API-secret here

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:  old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance": old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    if source == "binance": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    return old, new

def get_all_binance(symbol, kline_size, save = False):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv((os.getcwd() + "/data/" + filename))
    updateStatsJSON(len(data_df.index))
    print('All caught up..!')

    return data_df

def alertToPhone(email, pas, gateway, smtp, port, message):
    server = smtplib.SMTP(smtp,port)
    server.starttls()
    server.login(email,pas)

    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = "Horus"
    msg['To'] = gateway

    msg.attach(MIMEText(message, 'plain'))

    sms = msg.as_string()

    server.sendmail(email,gateway,sms)
    server.quit()

def generateAndSendMessage():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    file = open(os.getcwd() + "/dailyStats.json")
    data = json.load(file)
    file.close()
    greet = "Good Evening Technomancer.\n:eye: Your daily update. :eye:\n\n"
    f = u'Currencies Watching: \t' + str(data['stats'][0]['filesWatching'])
    t = u'Trades Added: \t\t\t\t\t\t\t\t' + str(data['stats'][0]['tradesAdded'])
    c = u'API Calls Made: \t\t\t\t\t\t' + str(data['stats'][0]['callsMade'])
    #t = "Trades Added: \t\t\t\t\t\t\t\t" + str(data['stats'][0]['tradesAdded']) + "\n"
    #c = "API Calls Made: \t\t\t\t\t\t" + str(data['stats'][0]['callsMade']) + "\n"
    update = f + t + c
    sig = "\nMay your empire grow.\n-Horus :bird: "
    out = greet + update + sig
    out = emoji.emojize(out)
    alertToPhone(email,pas,gateway,smtp,port,out)
    clearStatsJSON()


def updateStatsJSON(linesAdded):
    file = open(os.getcwd() + "/dailyStats.json")
    data = json.load(file)
    file.close()
    x = len(os.listdir("./data"))

    data['stats'][0]['filesWatching'] = x
    data['stats'][0]['tradesAdded'] = data['stats'][0]['tradesAdded'] + linesAdded
    data['stats'][0]['callsMade'] = data['stats'][0]['callsMade'] + 1
    
    with open(os.getcwd() + "/dailyStats.json", 'w') as jsonfile:
        json.dump(data, jsonfile, indent= 4)
    jsonfile.close()

def clearStatsJSON():
    data = {}
    data['stats'] = []

    zeroes = {
        "filesWatching" : 0,
        "tradesAdded" : 0,
        "callsMade" : 0
    }

    data['stats'].append(zeroes)

    with open(os.getcwd() + "/dailyStats.json", 'w') as jsonfile:
        json.dump(data, jsonfile, indent= 4)
    jsonfile.close()
    
def runUpdate():
    binance_symbols = ["BTCUSDT", "ETHBTC", "XRPBTC"]
    for symbol in binance_symbols:
        get_all_binance(symbol, '5m', save = True)

#if(dt.hour == 22):
#    runUpdate()
#    generateAndSendMessage()
#    pass
#else:
#   runUpdate()

generateAndSendMessage()

