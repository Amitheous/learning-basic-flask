from flask import Flask, render_template, request
from numba import jit
import time
import json
import csv
from io import StringIO
import pandas as pd
import multiprocessing as mp
import numpy as np
num_processes = mp.cpu_count()


def adding(df):
    answer = 0
    for row in df.index:
        answer += df.loc[row]['RefSubNets']
    return answer


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
        print("NAME OF FILE: ", fileName)
        dFrame = pd.read_csv(StringIO(csvFormat))
        with open('data.txt', 'w') as out:
            dFrame.to_csv(out, index=False)
        with open('data.txt', 'r') as nowIn:
            newDFrame = pd.read_csv(nowIn)
            # chunk_size = int(newDFrame.shape[0]/num_processes)
            # chunks = [newDFrame.ix[newDFrame.index[i:i + chunk_size]]
            #           for i in range(0, newDFrame.shape[0], chunk_size)]
            # pool = mp.Pool(processes=num_processes)
            # result = pool.map(adding(newDFrame), chunks)
            # print(result)
            # print(newDFrame)
            # print('FILENAME CHECK FOR "Sales": ', fileName.__contains__('Sales'))
            if fileName.__contains__('insurance_sample'):
                result = 0
                for row in newDFrame.index:
                    if row == 0:
                        print("Starting...")
                    result += newDFrame.loc[row]['tiv_2012']
                print('Average Total Insurance Value in 2012: ' , result/len(newDFrame.index))
                print("Number of Rows: ", len(newDFrame.index))
            if fileName.__contains__('Sales Records'):
                combUnits = 0
                combPrice = 0
                combCost = 0
                combProfit = 0
                for row in newDFrame.index:
                    if row == 0:
                        print("Starting analysis...")
                    combUnits += newDFrame.loc[row]['Units Sold']
                    combPrice += newDFrame.loc[row]['Unit Price']
                    combCost += newDFrame.loc[row]['Unit Cost']
                    combProfit += newDFrame.loc[row]['Total Profit']
                print('Average Units Sold: ', round(combUnits/len(newDFrame.index), 2))
                print('Average Unit Price: ', round(combPrice/len(newDFrame.index), 2))
                print('Average Unit Cost: ', round(combCost/len(newDFrame.index), 2))
                print('Average Profit: ', round(combProfit/len(newDFrame.index), 2))
                print("Number of Records Processed: ", len(newDFrame.index))
            # print(readDFrame.index)

            # print(result)
            # print(readDFrame.loc[12]['RefSubNets'])
        # print(jsonObj.loc[12]['Domain'])

        # print(csvFormat)
        # reader = csv.DictReader(StringIO(csvFormat))

        # size = 1e1
        # with open('data.json') as json_file:
        #   print(json_file)
            # data = pd.read_csv(json_file, chunksize = size, index_col=['\\r'])
            # json.loads()
            # del(user_log_chunk)

            # print(number)
        # for row in json_data:
        #   json.dump(row, jsonfile)
        #   jsonfile.write('\n')

        # print(json_data)

        end = time.time()
        print('Time to compile: ', round((end - start)*1000, 2), 'ms')
        return 'success'


if __name__ == '__main__':
    app.run(debug=True)
