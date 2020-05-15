from flask import Flask, render_template

from sqlalchemy import create_engine 
from sqlalchemy import inspect

import csv
from collections import Counter

import matplotlib.pyplot as plt 
from matplotlib.ticker import FormatStrFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import pandas as pd
import seaborn as sns
import datetime
import io


with open ('covid19dataexport.csv') as covid:
    covidreader = csv.DictReader(covid)
    datelist = []
    for line in covidreader:
        datelist.append(line['Date reported']) #datelist will be filled with just the dates in the csv file 
    datecountlist = sorted(Counter(datelist).items()) #list of tuples sorted by date. Date is paired with total cases 
    datelist,caselist = map(list,zip(*datecountlist)) #unpacking the list of tuples into 2 respective lists 
        
df = pd.DataFrame({'date': datelist, 'daily_cases': caselist}) #creates dataframe for dates and daily_cases
db_uri = 'sqlite:///data/covidData'
engine = create_engine(db_uri, echo=False)
df.to_sql(name='alberta', con=engine, if_exists='replace')
engine.dispose()

app = Flask(__name__)


@app.route('/')
def plot_covid():

    try:
        name = 'alberta'
        engine = create_engine(db_uri, echo = False)
        df = pd.read_sql_table(table_name= name, con= engine)
        print(df.head())
        engine.dispose()

        fig1, (ax1,ax2) = plt.subplots(nrows=2,ncols=1,sharex=True)
        FigureCanvas(fig1)

        #Make sure dates are sorted
        df = df.sort_values(by=['date'])

        #Compute total and smoothed daily cases
        df['total_cases'] = df.daily_cases.cumsum()
        df['smooth_daily_cases'] = df.daily_cases.rolling(3).mean()

        #Checking what we have
        df.info()
        print(df.head())

        #Figure1: Seaborn plots for daily cases and total cases
        sns.barplot(x='date', y='daily_cases', data=df, ax=ax1,
            palette=sns.color_palette("Set2", 2))
        sns.lineplot(x='date', y='total_cases', data=df, ax=ax2)

        ax1.grid(b=True)
        ax2.grid(b=True)
        plt.xticks(rotation = 90, horizontalalignment='right')
        plt.tight_layout()

        image1 = io.StringIO()
        fig1.savefig(image1, format='svg')
        svg_image1 = '<svg' + image1.getvalue().split('<svg')[1]

        #Figure2: Matplotlib log-log plot of:
        # - total_cases (x-axis) and 
        # - smoothed daily_cases (y-axis)
        # as used in: https://www.youtube.com/watch?v=54XLXg4fYsc

        fig2 = plt.figure()
        FigureCanvas(fig2)

        x_str='total_cases'
        y_str='smooth_daily_cases'
        # using log-log and two minor ticks per decade
        plt.loglog(df[x_str], df[y_str], subsx=[2, 5], subsy=[2, 5])
        # Add a 'dot' to indicate last measurement
        plt.plot(df[x_str].iloc[-1], df[y_str].iloc[-1], 'ko')
        # labels
        plt.xlabel(x_str)
        plt.ylabel(y_str)
        # grid on both major and minor ticks
        plt.grid(which='both')
        # formatting major and minor tick labels
        ax = plt.gca()
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.0f"))
        ax.xaxis.set_minor_formatter(FormatStrFormatter("%.0f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.0f"))
        ax.yaxis.set_minor_formatter(FormatStrFormatter("%.0f"))

        img2 = io.StringIO()
        fig2.savefig(img2, format='svg')
        svg_image2 = '<svg' + img2.getvalue().split('<svg')[1]

    except:
        return render_template('index.html', name=name, plot1='Error in calculating values', plot2='Error in calculating values')
    else:
        return render_template('index.html',name=name, plot1 = svg_image1, plot2 = svg_image2)


if __name__ == '__main__':
    app.debug = True
    app.run()

