
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import json

# Blueprint
#      * named 'dashboard'
#      * defined at '__name__'
#      * url_prefix will be prepended to all the URLs
#        associated with the blueprint
bp = Blueprint('dashboard', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])  # homepage
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        data = {}
        data = request.form

        #urls[request.form['code']] = {'url': request.form['url']}

        # open/create JSON file & save user's input
        with open('portfolio.json', 'w') as data_file:
            json.dump(data, data_file)  # save url to JSON

        return render_template('index.html', data=data)
