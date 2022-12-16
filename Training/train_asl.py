# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 12:46:04 2022

@author: shree
"""

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

sz = 128

# Step 1 - Building the CNN

# Initializing the CNN
classifier = Sequential()

# 1 convolution layer and pooling
classifier.add(Convolution2D(32, (3, 3), input_shape=(sz, sz, 1), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# 2 convolution layer and pooling
classifier.add(Convolution2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add(Flatten())

# Adding a fully connected layer 1
classifier.add(Dense(units=128, activation='relu'))


classifier.add(Dense(units=26, activation='softmax')) # softmax for more than 2

# Compiling the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) # categorical_crossentropy for more than 2


# Step 2 - Preparing the train/test data and training the model
classifier.summary()
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('data2/asl_alphabet_train',
                                                 target_size=(sz, sz),
                                                 batch_size=10,
                                                 color_mode='grayscale',
                                                 class_mode='categorical',
                                                 shuffle=True)

test_set = test_datagen.flow_from_directory('data2/asl_alphabet_test',
                                            target_size=(sz , sz),
                                            batch_size=10,
                                            color_mode='grayscale',
                                            class_mode='categorical',
                                            shuffle=False) 
classifier.fit(
        training_set,
        steps_per_epoch=2400, # No of images in training set
        epochs=5,
        validation_data=test_set,
        validation_steps=600)# No of images in test set

# Saving the model
model_json = classifier.to_json()
with open("model-asl-bw.json", "w") as json_file:
    json_file.write(model_json)
print('Model Saved')
classifier.save_weights('model-asl-bw.h5')
print('Weights saved')
