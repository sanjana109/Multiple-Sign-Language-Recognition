
# Importing the Keras libraries and packages
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense, Dropout
from keras.layers import TimeDistributed
from keras.layers import LSTM
from keras.layers import Activation
from keras.layers import BatchNormalization
from keras.layers import ZeroPadding2D

import os

#os.environ["CUDA_VISIBLE_DEVICES"] = "1"
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


# softmax for more than 2
classifier.add(Dense(units=26, activation='softmax'))

# Compiling the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[
                   'accuracy'])  # categorical_crossentropy for more than 2


# Step 2 - Preparing the train/test data and training the model
classifier.summary()


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
                                            target_size=(sz, sz),
                                            batch_size=10,
                                            color_mode='grayscale',
                                            class_mode='categorical',
                                            shuffle=False)
classifier.fit(
    training_set,
    steps_per_epoch=3000,   # No of images in training set
    epochs=1,               # No of epochs
    validation_data=test_set,
    validation_steps=0)     # No of images in test set

# Saving the model
model_json = classifier.to_json()
with open("//model//model-asl-bw.json", "w") as json_file:
    json_file.write(model_json)
print('Model Saved')
classifier.save_weights('//model//model-asl-bw.h5')
print('Weights saved')
