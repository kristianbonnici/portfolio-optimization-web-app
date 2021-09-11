from flask import (
    Blueprint, flash, redirect, render_template,
    request, url_for
)
import json
from datetime import datetime
import pandas_datareader.data as web
from optifolio import PortfolioOptimizer
from bokeh.embed import components
import bokeh

# Blueprint
#      * named 'dashboard'
#      * defined at '__name__'
#      * url_prefix will be prepended to all the URLs
#        associated with the blueprint
bp = Blueprint('dashboard', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])  # homepage
def index():
    if request.method == 'GET':
        return render_template('index.html', is_index=True)
    else:
        bokeh_version = bokeh.__version__

        data_dict = request.form.to_dict(flat=False)
        start_date = datetime.strptime(data_dict['start'][0], '%Y-%m-%d')
        end_date = datetime.strptime(data_dict['end'][0], '%Y-%m-%d')
        min_ret = float(data_dict['min-ret'][0]) / 100
        tickers = [x.strip() for x in data_dict['tickers'][0].split(',')]
        benchmark_ticker = data_dict['benchmark'][0].strip()

        if '' in tickers:
            flash("""Invalid tickers.""")
            return redirect(url_for('dashboard.index'))
        if start_date >= end_date:
            flash("""The start date must be before the end date.""")
            return redirect(url_for('dashboard.index'))

        try:
            data = web.DataReader(tickers, 'yahoo',
                                  start=start_date, end=end_date)['Adj Close']
        except:
            flash("""Failed loading data from the Yahoo Finance API.""")
            return redirect(url_for('dashboard.index'))

        for col in data:
            na_values = data[col].isna().sum()
            values = len(data[col])
            if values == na_values:
                flash("""ERROR: There is no data for {}.""".format(col))
                return redirect(url_for('dashboard.index'))
            if na_values != 0:
                flash("""{col} includes {na_val} NaN values ({na_val}/{val}).
                """.format(col=col, na_val=na_values, val=values))

        model = PortfolioOptimizer().fit(data, min_ret=min_ret)
        p1 = model.plot_efficient_frontier(output=None,
                                           width=800,
                                           height=410,
                                           border_fill_color='#28283B',
                                           toolbar=True)
        p1.sizing_mode = "scale_width"
        script1, div1 = components(p1)

        p2 = model.plot_weights(output=None, width=500, height=500,
                                border_fill_color='#28283B')
        p2.sizing_mode = "scale_width"
        script2, div2 = components(p2)

        if benchmark_ticker == '':
            benchmark = None
        else:
            benchmark = web.DataReader([benchmark_ticker], 'yahoo',
                                       start=start_date,
                                       end=end_date)['Adj Close']
            if benchmark_ticker == '^GSPC':
                benchmark.columns = ['S&P 500 (^GSPC)']
            elif benchmark_ticker == '^IXIC':
                benchmark.columns = ['NASDAQ Composite (^IXIC)']
            elif benchmark_ticker == '^DJI':
                benchmark.columns = ['Dow Jones Industrial Average (^DJI)']
            elif benchmark_ticker == '^RUT':
                benchmark.columns = ['Russell 2000 (^RUT)']

        p3 = model.plot_cumulative_return(output=None, width=1200, height=300,
                                          benchmark_data=benchmark,
                                          border_fill_color='#28283B',
                                          toolbar=True)
        p3.sizing_mode = "scale_width"
        script3, div3 = components(p3)

        ret = model.ret
        rf_ret = model.rf_ret
        vol = model.vol
        sharpe = model.sharpe
        weights = model.weights
        stock_weights = model.stock_weights
        stock_names = model.stock_names

        # open/create JSON file & save user's input
        with open('portfolio.json', 'w') as data_file:
            json.dump(data_dict, data_file)  # save url to JSON

        return render_template('index.html', is_index=True,
                               data=data_dict,
                               bokeh_version=bokeh_version,
                               script1=script1, div1=div1,
                               script2=script2, div2=div2,
                               script3=script3, div3=div3,
                               stock_names=stock_names,
                               stock_weights=stock_weights * 100,
                               ret=ret * 100, rf_ret=rf_ret * 100,
                               vol=vol * 100, sharpe=sharpe)


@bp.route('/info')
def info():
    return render_template('info.html', is_index=False)


@bp.errorhandler(404)
def page_not_found():
    return 404
