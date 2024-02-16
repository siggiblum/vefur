from flask import Flask, jsonify
from flask_cors import CORS
from valag import *
from framvirkir_vextir import *
import datetime
from cs1 import *
from nss2 import * 

app = Flask(__name__)
CORS(app)

@app.route('/data')
def data():
    data = nss_main()
    return jsonify(data)

@app.route('/table_data')
def table_data():
    table_data = []
    info = credit_spread()
    for i in range(len(info)):
        data = {
            'Name': info[i][0],
            'RIK': str(round(info[i][2], 4))+"%",
            'Credit Spread': str(round(info[i][3], 4))+"%",
            'Bond': str(round(info[i][1], 4))+"%"
        }
        table_data.append(data)
    return jsonify(table_data)

def test():
    return verdlag()


@app.route('/verdbolgualag')
def verdbolga():
    hnit, hnit2 = test()
    return jsonify({'hnit': hnit, 'hnit2': hnit2})

# @app.route('/verdbolgualag')
# def verdbolga():
#     hnit = [[0.5, 9.283566120394374], [1.0, 6.96207893568177], [2.0, 5.03956727311888], [3.0, 4.5816795113614095], [4.0, 4.308549094157714], [5.0, 4.183284577594507], [6.0, 4.138406537666583], [7.0, 4.103376528358779], [8.0, 4.068346519050975], [9.0, 4.035462555453079], [10.0, 4.002830916114801], [11.0, 3.9701992767765253], [12.0, 3.9375676374382476], [13.0, 3.9403495216369633]]
#     hnit2 = [['RIKB 24 0415', 0.1612021857923497, 11.371049361540507], ['RIKB 25 0612', 1.293023423183876, 6.116032365560529], ['RIKB 26 1015', 2.5121201531488575, 4.714934337477135], ['RIKB 28 1115', 4.312981000054467, 4.223064463036009], ['RIKB 31 0124', 5.781852100444339, 4.1380136506036385], ['RIKB 42 0217', 12.03462185346688, 3.9364378696026936]]
#     return jsonify({'hnit': hnit, 'hnit2': hnit2})

@app.route('/forward_rate')
def forward_rate_route():
    overd = forward_rate()
    return jsonify(overd)

@app.route('/forward_rate_verdtryggt')
def forward_rate_verdtryggt_route():
    verd = forward_rate_verdtryggt()
    return jsonify(verd)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)