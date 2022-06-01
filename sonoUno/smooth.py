# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:04:39 2022

@author: Johanna
"""

import matplotlib.pyplot as plt
from data_import.data_import import DataImport
from data_transform.data_opened import DataOpenedColumns
from data_transform import smooth


imp = DataImport()
transf = DataOpenedColumns()
data = imp.set_arrayfromfile('SDSS J171250.00+640310.6 .csv', 'csv')

x = data[0].iloc[1:,0]
y = data[0].iloc[1:,2]

transf.set_numpyxy(data[0])

x, y = transf.get_numpyxy()


# x = np.linspace(0,2*np.pi,100)
# y = np.sin(x) + np.random.random(100) * 0.2
yhat = smooth.savitzky_golay(y, 51, 3) # window size 51, polynomial order 3

plt.plot(x,y)
plt.plot(x,yhat, color='red')
plt.show()