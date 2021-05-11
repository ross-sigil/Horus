import datetime
import os
import json


print("\n")
def wallStatsJSON():
    file = open(os.getcwd() + "/dailyStats.json")
    data = json.load(file)
    file.close()
    a = "Files Watching:\t" + str(data['stats'][0]['filesWatching']) + "\n"
    b = "Trades Added:\t" + str(data['stats'][0]['tradesAdded']) + "\n"
    c = "Calls Made:\t" + str(data['stats'][0]['callsMade']) + "\n"

    file = open(os.getcwd() + "/dailyStats.txt", "w")
    file.write(a)
    file.write(b)
    file.write(c)

wallStatsJSON()