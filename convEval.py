# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 19:01:30 2021

@author: sebas
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import numpy as np

model = Sequential()
Xshape = [8,8,7]
model.add(Conv2D(400, (4,4), 
                 strides=2, activation='relu', input_shape=Xshape))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(400,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

Xname = "randPos(600000,8,8,7).npy"
Yname = "Winners(600000,).npy"
X = np.load(Xname)
Y = np.load(Yname)
model.fit(X, Y, batch_size=32, validation_split=0.1, epochs=5)