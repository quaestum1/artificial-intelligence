from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

ds = read_csv('censos2011-lisboa.csv')
X = ds.iloc[0 : 3000, 0 : 10].values.astype(float)
Y = ds.iloc[0 : 3000, 10].values.astype(float)
X1 = ds.iloc[3000:, 0 : 10].values .astype(float)

trainX, testX, trainY, testY = train_test_split(
        X, Y, test_size = 0.2, random_state = 0)

scaler = StandardScaler()
trainX = scaler.fit_transform(trainX)
testX = scaler.transform(testX)

classifier = Sequential()
classifier.add(Dense(units = 4, kernel_initializer = 'uniform', 
                     activation = 'relu', input_dim = 10))
classifier.add(Dense(units = 4, kernel_initializer = 'uniform', 
                     activation = 'relu'))
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', 
                     activation = 'sigmoid'))
classifier.compile(optimizer = 'rmsprop', loss = 'binary_crossentropy', 
                   metrics = ['accuracy'])

classifier.fit(trainX, trainY, epochs = 32)

X1 = scaler.transform(X1)
predY = (classifier.predict(X1) > 0.5).astype(int)