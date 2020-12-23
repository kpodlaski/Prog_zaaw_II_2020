#https://www.tensorflow.org/overview/

import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np

#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

mnist = tf.keras.datasets.mnist
#mnist = tf.keras.datasets.fashion_mnist
max_epoch = 50

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(64, activation='sigmoid'),
  tf.keras.layers.Dense(64, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='sgd',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
print(np.shape(x_train), np.shape(y_train))
print(type(x_train), type(y_train))

history = model.fit(x_train, y_train, epochs=max_epoch, validation_data=(x_test, y_test))
print(model.evaluate(x_test, y_test))
print(history.history)

fig, (ax1, ax2) = plt.subplots(1,2)

epochs = range(max_epoch)
ax1.plot(epochs,history.history['loss'], label='train set')
ax1.plot(epochs,history.history['val_loss'], label='test set')
ax1.set_xlabel("Epoka")
ax1.set_ylabel("F straty")
ax1.legend()
ax2.plot(epochs,history.history['accuracy'], label='train set')
ax2.plot(epochs,history.history['val_accuracy'], label='test set')
ax2.set_xlabel("Epoka")
ax2.set_ylabel("skuteczność")
ax2.legend()
plt.show()


