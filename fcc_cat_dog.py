# -*- coding: utf-8 -*-
"""fcc_cat_dog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DGUOEKRgFIkuMM3lEQzwoYRIbnAcJPZP

---
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import matplotlib.pyplot as plt

# get files
!wget https://cdn.freecodecamp.org/project-data/cats-and-dogs/cats_and_dogs.zip

!unzip cats_and_dogs.zip

PATH = 'cats_and_dogs'

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])
total_test = len(os.listdir(test_dir))

batch_size = 128
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

train_image_generator = ImageDataGenerator(rescale = 1/255)
validation_image_generator = ImageDataGenerator(rescale = 1/255)
test_image_generator = ImageDataGenerator(rescale = 1/255)

train_data_gen = train_image_generator.flow_from_directory(batch_size = batch_size, directory = train_dir, target_size = ((IMG_HEIGHT, IMG_WIDTH)), color_mode = 'rgb', class_mode = 'binary')
val_data_gen = validation_image_generator.flow_from_directory(batch_size = batch_size, directory = validation_dir, target_size = ((IMG_HEIGHT, IMG_WIDTH)), color_mode = 'rgb', class_mode = 'binary')
test_data_gen = test_image_generator.flow_from_directory(batch_size = 128, directory = test_dir, target_size = ((IMG_HEIGHT, IMG_WIDTH)), color_mode = 'rgb', classes = [''], class_mode = None, shuffle = False)

def plotImages(images_arr, probabilities = False):
    fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
    if probabilities is False:
      for img, ax in zip( images_arr, axes):
          ax.imshow(img)
          ax.axis('off')
    else:
      for img, probability, ax in zip( images_arr, probabilities, axes):
          ax.imshow(img)
          ax.axis('off')
          if probability > 0.5:
              ax.set_title("%.2f" % (probability*100) + "% dog")
          else:
              ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
    plt.show()

sample_training_images, _ = next(train_data_gen)
plotImages(sample_training_images[:5])

train_image_generator = ImageDataGenerator(rescale = 1/255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, rotation_range = 40)

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')

base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3),
                                               include_top= False,
                                               weights='imagenet'
                                               )
base_model.trainable = False
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(1, activation = 'sigmoid')

model = tf.keras.Sequential([base_model, global_average_layer, prediction_layer])

base_model.summary()

base_learning_rate = 0.0001
model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=base_learning_rate), loss = 'binary_crossentropy', metrics = ['accuracy'])

step_train=train_data_gen.n//train_data_gen.batch_size
step_val=val_data_gen.n//val_data_gen.batch_size
history = model.fit(train_data_gen, steps_per_epoch = step_train, epochs = epochs, validation_data = val_data_gen, validation_steps = step_val)

#get predictions
probabilities = list()
for i in range(total_test-1):
  sample_testing_images = next(test_data_gen)
  sample_testing_images = tf.image.resize(sample_testing_images, [224, 224])
  x = model.predict(sample_testing_images)
  probabilities.append(x.item(i))
print(probabilities)

# plot images with probabilities and classification as header 
sample_testing_images = next(test_data_gen)
plotImages(sample_testing_images[: 5], probabilities[:5])
