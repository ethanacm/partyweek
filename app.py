from flask import Flask
import flask
from flask import request
import time
from pytz import timezone
import pytz
import sqlite3
import datetime

application = Flask(__name__, static_folder='static', template_folder='templates')

SQLLITE = '/home/ethanacm/partyweek/database.db'
GOAL = 1500

DATA = {'pcnt_funded': 20,
        'amount_raised': 230,
        'num_sponsors': 32,
        'pcnt_first_year': 10,
        'pcnt_sophomore': 20,
        'pcnt_junior': 30,
        'pcnt_senior': 40,
        'chalice_amount': 200,
        'crown_amount': 100,
        'last_updated': "3 mins ago"
        }

HISTORY = [{'timestamp': '',
            'amount': '234',
            'year': 'sophomore',
            'username': 'test',
            'caption': 'testtt'},
           {'timestamp': '',
            'amount': '234',
            'year': 'sophomore',
            'username': 'test',
            'caption': 'testtt'},
           {'timestamp': '',
            'amount': '234',
            'year': 'sophomore',
            'username': 'test',
            'caption': 'testtt'}
           ]


def calculate_data(history, top_6):
    data = {}
    data['last_updated'] = history[0]['timestamptext']
    data['num_sponsors'] = len(history)
    data['chalice_amount'] = 0
    data['crown_amount'] = 0
    if len(top_6) > 0:
        data['chalice_amount'] = top_6[0]['amount']
        data['crown_amount'] = top_6[-1]['amount']

    total = 0
    senior_total = 0
    junior_total = 0
    sophomore_total = 0
    freshman_total = 0

    for donation in history:
        amount = donation['amount']
        total += amount
        if donation['year'] == 'senior':
            senior_total += amount
        elif donation['year'] == 'junior':
            junior_total += amount
        elif donation['year'] == 'sophomore':
            sophomore_total += amount
        elif donation['year'] == 'freshman':
            freshman_total += amount

    year_total = freshman_total + sophomore_total + senior_total + junior_total
    data['pcnt_first_year'] = int(freshman_total / year_total * 100)
    data['pcnt_sophomore'] = int(sophomore_total / year_total * 100)
    data['pcnt_junior'] = int(junior_total / year_total * 100)
    data['pcnt_senior'] = int(senior_total / year_total * 100)
    data['amount_raised'] = total
    data['pcnt_funded'] = int(total / GOAL * 100)


    return data





def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@application.route('/')
def get_main_page():
    conn = sqlite3.connect(SQLLITE)
    conn.row_factory = dict_factory
    c = conn.cursor()

    c.execute('SELECT * FROM {tn} ORDER BY timestamp DESC'.format(tn='database'))
    all_rows = c.fetchall()
    c.execute('SELECT * FROM {tn} ORDER BY amount DESC LIMIT 6'.format(tn='database'))
    top_6 = c.fetchall()
    data = calculate_data(all_rows, top_6)
    conn.close()
    print('1):', all_rows)
    return flask.render_template('home.html', data=data)


@application.route('/log')
def get_log_page():
    conn = sqlite3.connect(SQLLITE)
    conn.row_factory = dict_factory
    c = conn.cursor()

    if len(request.args) > 0:
        print('args', request.args)
        args = request.args

        central = timezone('US/Central')
        time_string = datetime.datetime.now(central)
        l = time_string.strftime('%l:%M%p %Z on %b %d')
        if args["amount"]:
            c.execute("INSERT INTO database VALUES (?,?,?,?,?,?)",
                      [int(time.time() * 1000), int(args["amount"]), args["year"], args["username"], args['caption'],
                       l])
            # update db
            conn.commit()

    c.execute('SELECT * FROM {tn} ORDER BY timestamp DESC'.format(tn='database'))
    all_rows = c.fetchall()

    conn.close()

    return flask.render_template('log.html', history=all_rows)


# @application.route('/submit', methods=['POST'])
# def submit():
#     print('request files', request.form)
#     return flask.Response(200)


if __name__ == '__main__':
    application.run()
