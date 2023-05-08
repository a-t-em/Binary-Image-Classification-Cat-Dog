**Cat vs Dog Classifier**

This repository contains two models for classifying images of cats and dogs. The model from Kaggle was trained using the Kaggle cat vs dog dataset, which contains ~2,500 images of cats and dogs. The model for the [freeCodeCamp project](https://www.freecodecamp.org/learn/machine-learning-with-python/machine-learning-with-python-projects/cat-and-dog-image-classifier) was trained using ~2,000 images provided by freeCodeCamp. Both datasets are balanced. 

**Kaggle Model**<br>
This is a simple CNN model. The model was trained without a pretrained base layer and utilizes a simple helper function to extract image and label data from the Kaggle dataset directory. It achieves an accuracy of around 70% on a held out test dataset of ~5,000 images.

**freeCodeCamp Model**<br>
This model uses MobileNetV2 as a base layer for a Keras Sequential model. The images were augmented using ImageDataGenerator to improve prediction accuracy. It achieves over 90% accuracy on the 50 images in the testing batch for this project.
