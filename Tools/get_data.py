from pyalgotrade.tools import yahoofinance
import csv
import os

import datetime

def get_instrument_data(instrument,start_year,end_year=datetime.datetime.now().year,output_file=None):
    output_file = 'data_{}_{}_{}.csv'.format(instrument,start_year,end_year)
    years = [year for year in range(start_year,end_year+1)]
    output = open(r'Data\\'+output_file,'wb')
    writer = csv.writer(output, delimiter=' ', quotechar=",")

    for year in years:
        yahoofinance.download_daily_bars(instrument, year,'tempcsv__{}'.format(year))
        tempfile = open('tempcsv__{}'.format(year),'rb')
        if year != years[0]:
            tempfile.next() #skip header
        for row in tempfile:
                output.write(row)
        tempfile.close()
        os.remove('tempcsv__{}'.format(year))
    output.close()