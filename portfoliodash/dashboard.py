
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import json
from datetime import datetime
import scipy
import pandas_datareader.data as web
from optifolio import PortfolioOptimizer
from bokeh.embed import components

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

        data_dict = request.form.to_dict(flat=False)
        start_date = datetime.strptime(data_dict['start'][0], '%Y-%m-%d')
        end_date = datetime.strptime(data_dict['end'][0], '%Y-%m-%d')
        min_ret = float(data_dict['min-ret'][0])/100
        tickers = [x.strip() for x in data_dict['tickers'][0].split(',')]
        benchmark_ticker = data_dict['benchmark'][0].strip()
        print(benchmark_ticker)

        data = web.DataReader(tickers, 'yahoo',
                              start=start_date, end=end_date)['Adj Close']

        model = PortfolioOptimizer().fit(data, min_ret=min_ret)
        p1 = model.plot_efficient_frontier(output=None, width=800, height=410,
                                           border_fill_color='#28283B', toolbar=True)
        p1.sizing_mode = "scale_width"
        script1, div1 = components(p1)

        p2 = model.plot_weights(output=None, width=500, height=500,
                                border_fill_color='#28283B')
        p2.sizing_mode = "scale_width"
        script2, div2 = components(p2)

        if benchmark_ticker == '':
            benchmark_ticker = None
        else:
            benchmark = web.DataReader(
                [benchmark_ticker], 'yahoo', start=start_date, end=end_date)['Adj Close']
        p3 = model.plot_cumulative_return(output=None, width=1200, height=300,
                                          benchmark_data=benchmark,
                                          border_fill_color='#28283B',
                                          toolbar=True)
        p3.sizing_mode = "scale_width"
        script3, div3 = components(p3)

        # open/create JSON file & save user's input
        with open('portfolio.json', 'w') as data_file:
            json.dump(data_dict, data_file)  # save url to JSON

        return render_template('index.html', data=data_dict,
                               script1=script1, div1=div1,
                               script2=script2, div2=div2,
                               script3=script3, div3=div3)
