import pandas as pd
import numpy as np
import math
import datetime
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv


earthRadii = 6371.0088

def fileWrite(df, filename):
  f = open(filename, 'w+')
  df.to_excel(filename)
  f.close()

rawfilename = 'data.text'
raw = []
with open("data.text") as f:
  for line in f:
    raw.append(line)

df = pd.DataFrame(raw)

store = []
deb = []
for i in range(0, df.size - 3, 3):
  temp = []
  temp.append(str(df.iloc[i][0]))
  temp.append(str(df.iloc[i + 1][0]))
  temp.append(str(df.iloc[i + 2][0]))
  testSat = twoline2rv(str(df.iloc[i + 1][0]), str(df.iloc[i + 2][0]), wgs84)
  position, velocity = testSat.propagate(2019, 11, 2, 11, 0 , 0)
  temp.append(position)
  alt = math.sqrt(position[0] * position[0] + position[1] * position[1] + position[2] * position[2]) - earthRadii
  temp.append(alt)
  temp.append(velocity)
  tangspd = math.sqrt(velocity[0] * velocity[0] + velocity[1] * velocity[1] + velocity[2] * velocity[2])
  temp.append(tangspd)
  temp.append(testSat.error)
  temp.append(testSat.error_message)
  store.append(temp)
  if "DEB" not in temp[0]:
    continue
  else:
    deb.append(temp)


data = pd.DataFrame(store, columns=['name', 'tle1', 'tle2', 'pos', 'alt', 'vel', 'tangspd', 'errNo', 'errMsg'])
data_deb = pd.DataFrame(deb, columns=['name', 'tle1', 'tle2', 'pos', 'alt', 'vel', 'tangspd', 'errNo', 'errMsg'])

print(data_deb.head())


fileWrite(data, "test.xlsx")
fileWrite(data_deb, "deb.xlsx")

print("Done Processing!")

