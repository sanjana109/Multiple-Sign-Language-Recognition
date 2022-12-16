# Multiple-Sign-Language-Recognition
Multiple Sign Language to Multiple Spoken Language Translation using CNN

### Introduction
Sign language is a way of communication for deaf and mute people. For a non-deaf-mute person understanding the exact context of the symbolic expressions of these differently-abled people is a challenging job. There exists no universal sign language. This leads to a communication gap among hearing/speech impaired people from different regions of the world.

### Objective
- This project presents a solution to bridge this gap and provide a holistic system that aims to make conversation with deaf and mute people easier and effective. 
- The project implements a Multilingual Live Feed Sign Language software that Interpreters sign language using Machine Learning. 
- The proposed system facilitates the user to input the gesture in multiple sign languages and to get the multilingual output in the form of text. 
- It also provides the option of translating spoken language as well as the text-sign language conversion feature.

### AI Model 
In the proposed system Computer Vision and Natural Language Processing are used to achieve the expected outcomes.

### Methodology
The system has three modules - Sign Gesture Classification, Spoken language Translation, Text - Sign Language Translation.

#### 1. Sign Gesture Classification
- Dataset for American & Indian Sign Language was downloaded
  ASL dataset - (https://www.kaggle.com/datasets/grassknoted/asl-alphabet)
  ISL dataset - (https://www.kaggle.com/datasets/vaishnaviasonawane/indian-sign-language-dataset)
- Preprocessing of the dataset was carried out by resizing them to 128x128, converting to grayscale and then applying Gaussian blur filter for feature extraction.
- Model is trained using Convolutional Neural Network. As this system translates 2 sign languages with symbols of different complexity, 2 CNN models (one for each sign language) was designed
- Validation is done on test data and accuracy is recorded
- Real time capture of the signs is done with OpenCV. Captured image is processed & passed to CNN model for prediction. If letter is detected for more than 50 frames it is printed

#### 2. Spoken Language Translation
- This component was built using the translate module in the Tkinter GUI desktop app in python.
- Translation of major languages is provided by the translate package.
- Five language choices are provided namely English, Hindi, Kannada, Telugu & Marathi.
- By typing the sentence and choosing the appropriate input and output language the translate component translates the entered sentence into the target language.

#### 3. Text-Sign Conversion
- This component does the finger-level translation of the entered text.
- Each character of the entered text is extracted and the corresponding sign image is fetched from the training dataset.
- All the images fetched are concatenated as a list and displayed on the screen. 
