import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import schedule_generator as sg
import time

class Regression:
    def __init__(self):
        self.model = tf.keras.Sequential([
            layers.Dense(512, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(8, activation='relu'),
            layers.Dense(4, activation='relu'),
            layers.Dense(2, activation='relu'),
            layers.Dense(1)
            ])
        self.loss = 'mse'
        self.metric = 'mae'
        self.step_size = 0.001
        self.history = 0
        self.results = 0

    def trainNetwork(self,epoch_num,data,labels):
        train_data = data.flatten('F')
        train_labels = labels.flatten('F')
        self.model.compile(
              optimizer=tf.train.RMSPropOptimizer(self.step_size),
              loss=self.loss,
              metrics=[self.metric])
        class PrintDot(keras.callbacks.Callback):
          def on_epoch_end(self, epoch, logs):
           if epoch % 100 == 0: print('')
           print('.', end='')    
        #early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10000)
        self.history = self.model.fit(data, labels, epochs=epoch_num, validation_split=0.2, verbose=0, callbacks=[PrintDot()])
        return self.history

    def testNetwork(self,data,labels):
        test_data = data.flatten('F')
        test_labels = labels.flatten('F')
        eva = self.model.evaluate(data, labels)
        print(eva)
        self.results = self.model.predict(data)
        correct = 0
        for i in range(0,labels.size): 
            if round(self.results[i,0]) == labels[i]:
                correct = correct + 1
        print(correct/labels.size)
        return self.results

    def plot_history(self,history):
        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Mean Abs Error [1000$]')
        plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),label='Train Loss')
        plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),label = 'Val loss')
        plt.legend() 
        plt.show()

    def plot_predict(self,results, labels): 
        plt.scatter(labels, results)
        plt.xlabel('True Values [1000$]')
        plt.ylabel('Predictions [1000$]')
        plt.axis('equal')
        _ = plt.plot([0, 1], [0, 1])
        plt.show()

if __name__=="__main__":
    event = np.random.randint(233100)
    days = 365
    before=time.time()

    model = Regression()    

    sched = sg.Schedule(test_id=event)
    train_data = sched.getTimesTest(1,days)
    sched = sg.Schedule(test_id=event+days)
    train_labels = sched.getTimesTest(1,1)
    history = model.trainNetwork(1000,train_data,train_labels)

    sched = sg.Schedule(test_id=event+1)
    test_data = sched.getTimesTest(1,days)
    sched = sg.Schedule(test_id=event+days+1)
    test_labels = sched.getTimesTest(1,1)
    results = model.testNetwork(test_data,test_labels)
    print(time.time()-before)
    
    model.plot_predict(results, test_labels)