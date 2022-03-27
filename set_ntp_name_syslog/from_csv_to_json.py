import json
import csv

with open ("inventory_sjca_spare.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    #next(reader)
    inventory_list = []
    for row in reader:
        inventory_list.append({"site name": row[0], "device role": row[1], "hostname": row[2], "ip address": row[3]})

with open("inventory_sjca_spare.json", "w") as json_file:
    json.dump(inventory_list, json_file, indent=4)
