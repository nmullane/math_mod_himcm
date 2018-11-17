import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import schedule_generator as sg

#class network:
#    def __init__(self, days):

class_names = ['away', 'home']

model = tf.keras.Sequential([
# Adds a densely-connected layer with 64 units to the model:
layers.Dense(512, activation='relu'),
# Add another:
layers.Dense(256, activation='relu'),
# Add another:
layers.Dense(128, activation='relu'),
# Add another:
layers.Dense(64, activation='relu'),
# Add another:
layers.Dense(32, activation='relu'),
# Add another:
layers.Dense(16, activation='relu'),
# Add another:
layers.Dense(8, activation='relu'),
# Add another:
layers.Dense(4, activation='relu'),
# Add another:
layers.Dense(2, activation='relu'),
# Add a softmax layer with 10 output units:
layers.Dense(2, activation='softmax')
])

model.compile(optimizer=tf.train.AdamOptimizer(0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#insert test data here
print("DATA")

sched = sg.Schedule(test_id=10024)
data = sched.getTimesTest(1,7)
#data = np.random.randint(2, size=(1440, 7))
sched = sg.Schedule(test_id=10024+7)
labels = sched.getTimesTest(1,1)
#labels = np.random.randint(2, size=(1440,1))

print(data)
print(labels)

#insert validation data here
#val_data = np.random.random((100, 32))
#val_labels = np.random.random((100, 10))

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

#early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10000)

history = model.fit(data, labels, epochs=1000, validation_split=0.2, verbose=0, callbacks=[PrintDot()])

sched = sg.Schedule(test_id=10024+1)
data = sched.getTimesTest(1,7)
#data = np.random.randint(2, size=(1440, 7))
sched = sg.Schedule(test_id=10024+8)
labels = sched.getTimesTest(1,1)
#labels = np.random.randint(2, size=(1440,1))

print("DATA")
print(data)
print(labels)

print("EVALUATE")

eva = model.evaluate(data, labels)

print(eva)

print("PREDICT")

result = model.predict(data)
print(result.shape)
predictions = np.argmax
#for i in range(0,len(result)):
#    predictions.append(np.argmax(result[i]))
print(result.shape)
print("DONE")

def plot_history(history):
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [1000$]')
  plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),label='Train Loss')
  plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),label = 'Val loss')
  plt.legend() 
  plt.show()

def plot_predict(result, labels):
  test_predictions = result.flatten()
  print(test_predictions.shape)
  print(labels.shape)
#  for i in range(0,test_predictions.size):
#    test_predictions[i] = round(test_predictions[i])
#  plt.scatter(labels, test_predictions)
  plt.xlabel('True Values [1000$]')
  plt.ylabel('Predictions [1000$]')
  plt.axis('equal')
  _ = plt.plot([0, 1], [0, 1])
  plt.show()

#plot_history(history)
#plot_predict(result, labels)
