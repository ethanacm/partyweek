from flask import Flask
import flask
from flask import request

application = Flask(__name__, static_folder='static', template_folder='templates')

DATA = {'pcnt_funded': 20,
        'amount_raised': 230,
        'num_sponsors': 32,
        'pcnt_first_year': 10,
        'pcnt_sophomore': 20,
        'pcnt_junior': 30,
        'pcnt_senior': 40,
        'chalice_amount': 200,
        'crown_amount': 100,
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


@application.route('/')
def get_main_page():
    return flask.render_template('home.html', data=DATA)


@application.route('/log')
def get_log_page():
    if len(request.args) > 0:
        print('args', request.args)
        # update db

    return flask.render_template('log.html', history=HISTORY)


# @application.route('/submit', methods=['POST'])
# def submit():
#     print('request files', request.form)
#     return flask.Response(200)


if __name__ == '__main__':
    application.run()
