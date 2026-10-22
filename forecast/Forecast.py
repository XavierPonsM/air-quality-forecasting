import os
import numpy
import pandas
import psycopg2
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
#No se si es necesario:
from sklearn.preprocessing import MinMaxScaler
from data_forecast import data


conn = psycopg2.connect(os.environ["DATABASE_URL"])
numpy.random.seed(7)

dataset = pandas.read_sql_query("""
                        SELECT nom_estacio, "data", contaminant, unitats, latitud, longitud, no2
                        FROM definitiu.no2_csv

                        """, conn)
df= pandas.DataFrame(dataset, columns=['nom_estacio', 'data', 'contaminant', 'unitats', 'latitud', 'longitud', 'no2'])
#print(df.head())

x = df.data[:, 2:]
print (x)