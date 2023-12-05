import tensorflow as tf
import numpy as np
from keras import layers, models
import matplotlib.pyplot as plt
from PIL import Image
import csv

# function to create a grayscale copy of an image
def make_gray(im):
    grayim = []
    for i in range(len(im)):
        grayim.append([])
        for j in range(len(im[i])):
            average = int(np.average(im[i][j][0:3]))
            if (len(im[i][j]) == 3):
                grayim[-1].append([average,average, average])
            else:
                grayim[-1].append([average,average, average, 255])

    grayim = np.array(grayim)

    return grayim


class_names = np.array(['House', 'Tree'])

ADD_GRAY_IMAGES = True

# Loads the labeled houses and trees
ds = []
labels = []
with open('Dataset.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        
        # Find the labeled portion of the image
        x1 = int(row['bbox_x'])
        x2 = int(row['bbox_x']) + int(row['bbox_width'])
        y1 = int(row['bbox_y'])
        y2 = int(row['bbox_y']) + int(row['bbox_height'])
        # trim image to find the correct part for training
        im = np.array(Image.open('images/' + row['image_name']))[y1:y2, x1:x2, 0:3]
        # resize the image so that it is proper size for our model
        im = np.array(Image.fromarray(im).resize((32,32)))

        # labels need to be integers
        labels.append(np.where(class_names == row['label_name'])[0])
        # append image
        ds.append(im)

        if (ADD_GRAY_IMAGES):
            # add a grayscale of the same image to the dataset
            labels.append(np.where(class_names == row['label_name'])[0])
            ds.append(make_gray(im))

# percent of labels to use for training
training_percent = 0.7
train_labels, test_labels = np.split(labels,[int(training_percent * len(labels))])
train_images, test_images = np.split(ds,[int(training_percent * len(ds))])
# 
train_images, test_images = train_images / 255.0, test_images / 255.0

# print(labels)


# i = 0
# for element in labels:
#     if element == 0:
#         i = i + 1
# print(len(labels))
# print(i)

# # prints first two figures
# plt.figure(figsize=(10, 10))

# plt.subplot(1,2,1)
# plt.imshow(ds[0])
# plt.subplot(1,2,2)
# plt.imshow(ds[1])

# # prints out the first 9 images
# pics = tf.keras.utils.image_dataset_from_directory(
#   "Images",
#   labels=None,
#   label_mode=None,
#   image_size=(256, 256))

# print(pics)
# plt.figure(figsize=(10, 10))
# for images in pics.take(1):
#   for i in range(9):
#     plt.subplot(3, 3, i + 1)
#     plt.imshow(images[i].numpy().astype("uint8"))
#     plt.axis("off")

# # tests the grayscale copy
# im = np.array(Image.open('images/2023-03-13_17-53-07.png'))

# plt.figure(figsize=(10, 10))

# plt.subplot(1,2,1)
# plt.imshow(im)
# grayim = make_gray(im)
# plt.subplot(1,2,2)
# plt.imshow(grayim)


# Make the model
model = models.Sequential()
model.add(layers.RandomFlip("horizontal_and_vertical"))
model.add(layers.RandomRotation(0.5))
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(2))

# Train the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(
                  from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=10, batch_size=10,
                    validation_data=(test_images, test_labels))

# Plot the models results
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

# Save model if it is good
# model.save("BST_B10_E10_G1.h5")

print(test_acc)
# plt.savefig("graph.png")