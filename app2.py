from flask import Flask, render_template, request, jsonify
from numba import jit
import time
import json
import csv
from io import StringIO
import pandas as pd
import multiprocessing as mp
import numpy as np
num_processes = mp.cpu_count()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
# @jit
def uploadFile():
    start = time.time()
    if request.method == 'POST':

        csvFormat = json.loads(request.data)['data']
        fileName = json.loads(request.data)['file']
        fields = json.loads(request.data)['fields']
        print("NAME OF FILE: ", fileName)
        dFrame = pd.read_csv(StringIO(csvFormat))
        with open('data.txt', 'w') as out:
            dFrame.to_csv(out, index=False)
        with open('data.txt', 'r') as nowIn:
            newDFrame = pd.read_csv(nowIn)
            if fileName.__contains__('Sales Records'):
                combUnits = 0
                combPrice = 0
                combCost = 0
                combProfit = 0
                for row in newDFrame.index:
                    if row == 0:
                        print("Starting analysis...")
                    combUnits += newDFrame.get_value(row, 'Units Sold')
                    combPrice += newDFrame.get_value(row, 'Unit Price')
                    combCost += newDFrame.get_value(row, 'Unit Cost')
                    combProfit += newDFrame.get_value(row, 'Total Profit')

                avgSold = round(combUnits/len(newDFrame.index), 2)
                avgPrice = round(combPrice/len(newDFrame.index), 2)
                avgCost = round(combCost/len(newDFrame.index), 2)
                avgProfit = round(combProfit/len(newDFrame.index), 2)
                processed = len(newDFrame.index)

        end = time.time()
        print('Time to compile: ', round((end - start)*1000, 2), 'ms')
        soldObj = {'sold': avgSold}
        priceObj = {'price': avgPrice}
        costObj = {'cost': avgCost}
        profitObj = {'profit': avgProfit}
        data = [{'processed': processed}]
        if fields['sold'] == True:
            data.append(soldObj)
        if fields['price'] == True:
            data.append(priceObj)
        if fields['cost'] == True:
            data.append(costObj)
        if fields['profit'] == True:
            data.append(profitObj)
        # "sold": avgSold,
        # "price": avgPrice,
        # "cost": avgCost,
        # "profit": avgProfit,
        # "processed": processed

        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
