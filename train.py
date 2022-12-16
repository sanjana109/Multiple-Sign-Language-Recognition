# Importing the Keras libraries and packages
from sklearn.metrics import confusion_matrix
import itertools
from keras.preprocessing.image import ImageDataGenerator
import os

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.layers import (LSTM, Activation, BatchNormalization, Convolution2D,
                          Dense, Dropout, Flatten, MaxPooling2D,
                          TimeDistributed, ZeroPadding2D)
from keras.models import Sequential

#os.environ["CUDA_VISIBLE_DEVICES"] = "1"
sz = 128

# Step 1 - Building the CNN

# Initializing the CNN
classifier = Sequential()
classifier.add(Convolution2D(32, (3, 3), padding='same',
               activation='relu', input_shape=(sz, sz, 1)))
classifier.add(Convolution2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Dropout(0.25))

classifier.add(Convolution2D(64, (3, 3), padding='same', activation='relu'))
classifier.add(Convolution2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Dropout(0.25))

classifier.add(Convolution2D(64, (3, 3), padding='same', activation='relu'))
classifier.add(Convolution2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Dropout(0.25))

classifier.add(Flatten())
classifier.add(Dense(512, activation='relu'))
classifier.add(Dropout(0.5))
classifier.add(Dense(26, activation='softmax'))

# Compiling the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[
                   'accuracy'])  # categorical_crossentropy for more than 2


# Step 2 - Preparing the train/test data and training the model
classifier.summary()

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.1
)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('data2/train',
                                                 target_size=(sz, sz),
                                                 batch_size=10,
                                                 color_mode='grayscale',
                                                 class_mode='categorical',
                                                 shuffle=True)

validation_generator = train_datagen.flow_from_directory('data2/train',
                                                         target_size=(sz, sz),
                                                         shuffle=True,
                                                         class_mode='categorical',
                                                         color_mode='grayscale',
                                                         batch_size=10,
                                                         subset="validation")

test_set = test_datagen.flow_from_directory('data2/test',
                                            target_size=(sz, sz),
                                            batch_size=10,
                                            color_mode='grayscale',
                                            class_mode='categorical',
                                            shuffle=False)
history = classifier.fit(
    training_set,
    steps_per_epoch=2400,  # No of images in training set
    epochs=1,              # No of epochs
    validation_data=test_set,
    validation_steps=240)  # No of images in test set

# Saving the model
model_json = classifier.to_json()
with open("model-bw.json", "w") as json_file:
    json_file.write(model_json)
print('Model Saved')
classifier.save_weights('model-bw.h5')
print('Weights saved')
classifier.save('model1.h5')

train_ds = train_datagen.flow_from_directory('data2/train',
                                             target_size=(sz, sz),
                                             validation_split=0.1,
                                             subset="training",
                                             batch_size=10,
                                             color_mode='grayscale',
                                             class_mode='categorical',
                                             shuffle=True)
class_names = train_ds.class_names

test_ds = test_datagen.flow_from_directory('data2/test',
                                           target_size=(sz, sz),
                                           batch_size=10,
                                           validation_split=0.01,
                                           subset="validation",
                                           color_mode='grayscale',
                                           class_mode='categorical',
                                           shuffle=False)
actual = []
pred = []
for images, labels in test_ds:
    for i in range(0, len(images)):
        image = images[i]
        image = np.expand_dims(image, axis=0)
        result = classifier.predict(image)
        pred.append(class_names[np.argmax(result)])
        actual.append(class_names[labels[i].numpy()])

# Visualizing loss

plt.figure(figsize=[8, 6])
plt.plot(history.history['loss'], 'r', linewidth=2.0)
plt.plot(history.history['val_loss'], 'b', linewidth=2.0)
plt.legend(['Training loss', 'Validation Loss'], fontsize=15)
plt.xlabel('Epochs ', fontsize=16)
plt.ylabel('Loss', fontsize=16)
plt.title('Loss Curves', fontsize=16)

# Visualizing accuracy

plt.figure(figsize=[8, 6])
print(history.history.keys())
plt.plot(history.history['accuracy'], 'r', linewidth=2.0)
plt.plot(history.history['val_accuracy'], 'b', linewidth=2.0)
plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize=15)
plt.xlabel('Epochs ', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
plt.title('Accuracy Curves', fontsize=16)


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):

    plt.figure(figsize=(15, 15))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


cm = confusion_matrix(y_true=actual, y_pred=pred)
plot_confusion_matrix(cm=cm, classes=class_names, title='Confusion Matrix')
