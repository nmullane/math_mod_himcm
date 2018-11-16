import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

print(tf.VERSION)
print(tf.keras.__version__)

model = tf.keras.Sequential([
# Adds a densely-connected layer with 64 units to the model:
layers.Dense(64, activation='relu'),
# Add another:
layers.Dense(64, activation='relu'),
# Add another:
#layers.Dense(14, activation='relu'),
# Add another:
#layers.Dense(64, activation='tanh'),
# Add a softmax layer with 10 output units:
layers.Dense(1)
])

model.compile(optimizer=tf.train.RMSPropOptimizer(0.001),
              loss='mse',
              metrics=['mae'])

#insert test data here
print("DATA")
data = np.random.randint(2, size=(1440,7))
labels = np.random.randint(2, size=1440)

#print(data)
#print(labels)

#insert validation data here
#val_data = np.random.random((100, 32))
#val_labels = np.random.random((100, 10))

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
#    if epoch % 100 == 0: print('')
    print('', end='')

#early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10000)

history = model.fit(data, labels, epochs=1000, validation_split=0.2, verbose=0, callbacks=[PrintDot()])

data = np.random.randint(2, size=(1440, 7))
labels = np.random.randint(2, size=1440)

print("DATA")
#print(data)
#print(labels)

print("EVALUATE")

eva = model.evaluate(data, labels)

print(eva)

print("PREDICT")

result = model.predict(data)
#print(result.shape)
print(result)
print("DONE")

def plot_history(history):
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [1000$]')
  plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),label='Train Loss')
  plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),label = 'Val loss')
  plt.legend() 
  #plt.show()

def plot_predict(result, labels):
  test_predictions = result.flatten()
  for i in range(0,test_predictions.size):
    test_predictions[i] = round(test_predictions[i])
  plt.scatter(labels, test_predictions)
  plt.xlabel('True Values [1000$]')
  plt.ylabel('Predictions [1000$]')
  plt.axis('equal')
  _ = plt.plot([0, 1], [0, 1])
  plt.show()

plot_history(history)
#plot_predict(result, labels)

"""
inputs = tf.keras.Input(shape=(32,)) # Returns a placeholder tensor

# A layer instance is callable on a tensor, and returns a tensor.
x = layers.Dense(64, activation='relu')(inputs)
x = layers.Dense(64, activation='relu')(x)
predictions = layers.Dense(10, activation='softmax')(x)

model = tf.keras.Model(inputs=inputs, outputs=predictions)

# The compile step specifies the training configuration.
model.compile(optimizer=tf.train.RMSPropOptimizer(0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Trains for 5 epochs
model.fit(data, labels, batch_size=32, epochs=5)

"""
