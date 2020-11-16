# COVID-19 Data Visualization Tool 
Author: Benjamin Lokanc
## What is this?

This is a Local web application built with python using flask, pandas, seaborn, matplotlib, and sqlalchemy to visualize the number of cases of COVID-19 in Alberta. 

## Preprocessing of Data

Data was downloaded from https://www.alberta.ca/stats/covid-19-alberta-statistics.htm in CSV format to be processed. 

Using python library 'csv' the data was processed and converted into a dataframe with 2 columns:
- 'date'
- 'daily_cases' 

Using sqlalchemy, the dataframe was stored in an sql database. 

## Modes of Data analysis 

There are two major figures produced to visualize the data.

The first figure is two subplots, the first being the number of daily cases reported, the second being total lifetime cases.

The seconed figure is a log-log plot of daily cases versus total cases. This is used as a measure to see how well the province is combating the virus. This is further described in the YouTube video by minute physics https://youtu.be/54XLXg4fYsc.
