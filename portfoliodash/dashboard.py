
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# Blueprint
#      * named 'dashboard'
#      * defined at '__name__'
#      * url_prefix will be prepended to all the URLs associated with the blueprint
bp = Blueprint('dashboard', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])  # homepage
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return render_template('index.html')
