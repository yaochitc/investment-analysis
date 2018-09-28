from datetime import datetime
from zipline.algorithm import TradingAlgorithm
from zipline.finance.trading import TradingEnvironment
from zipline.finance.blotter import SimulationBlotter
from zipline.finance.cancel_policy import NeverCancel
from zipline.api import order, record, symbol
from zipline.utils.factory import create_simulation_parameters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from extensions.trading_calendars.exchange_calendar_shsz import SHSZExchangeCalendar

def initialize(context):
    context.asset = symbol('AAPL')
    pass


def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data.current(symbol('AAPL'), 'price'))


def load_t(trading_day, trading_days, bm_symbol):
    bm = pd.Series(data=np.random.random_sample(len(trading_days)), index=trading_days)
    tr = pd.DataFrame(data=np.random.random_sample((len(trading_days), 7)), index=trading_days,
                      columns=['1month', '3month', '6month', '1year', '2year', '3year', '10year'])
    return bm, tr


def analyze(context=None, results=None):
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel('AAPL price (USD)')
    plt.gcf().set_size_inches(18, 8)
    plt.show()


cal = SHSZExchangeCalendar()
cancel_policy = NeverCancel()
blotter = SimulationBlotter(cancel_policy=cancel_policy)
trading_environment = TradingEnvironment(load=load_t, bm_symbol='^HSI',
                                         exchange_tz='Asia/Shanghai', trading_calendar=cal)

sim_params = create_simulation_parameters(start=pd.to_datetime("2016-01-01 00:00:00").tz_localize("Asia/Shanghai"),
                                          end=pd.to_datetime("2016-09-21 00:00:00").tz_localize("Asia/Shanghai"),
                                          data_frequency="daily",
                                          emission_rate="daily",
                                          trading_calendar=cal)
algor_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data, sim_params=sim_params,
                             env=trading_environment,
                             analyze=analyze, trading_calendar=cal, blotter=blotter)

parse = lambda x: datetime.date(datetime.strptime(x, '%Y/%m/%d'))
data_s = pd.read_csv('AAPL.csv', parse_dates=['Date'], index_col=0, date_parser=parse)
data_c = pd.Panel({'AAPL': data_s})
perf_manual = algor_obj.run(data_c)
