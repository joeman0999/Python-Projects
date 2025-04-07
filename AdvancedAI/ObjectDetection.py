import tensorflow as tf
import numpy as np
from keras import models
import matplotlib.pyplot as plt
from matplotlib import gridspec
from PIL import Image

savedModel = models.load_model('BST_B10_E10_G1.h5')
class_names = np.array(['House', 'Tree'])
# Object detection
# currently only does image 1


# Object detection
# currently only does image 1

# # Predicts a single image (idea of how to do for a chunk)
# predictions = model.predict(np.array([train_images[0]]))
# score = tf.nn.softmax(predictions[0])
# print(score)
# print(
#     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     .format(class_names[np.argmax(score)], 100 * np.max(score))
# )

gridification = 4
pixels = int(256 / gridification)

imArray = []

im = np.array(Image.open('images/2023-03-13_17-53-07.png'))

imArray.append(im)

plt.figure(figsize=(10, 10))
gs = gridspec.GridSpec(gridification, gridification, width_ratios=[1, 1, 1, 1],
         wspace=0.0, hspace=0.0, top=1.0, bottom=0.0, left=0.0, right=1.0)
imNum = 1
result = []
houses = 0
trees = 0
for i in range(len(imArray)):
  for x in range(gridification):
    result.append([])
    for y in range(gridification):
      
      chunk = imArray[i][pixels*x:pixels*(x+1)-1, pixels*y:pixels*(y+1)-1, 0:3]
      ax = plt.subplot(gs[x, y])
      ax.set_aspect("auto")
      imNum = imNum + 1
      plt.imshow(chunk)
      plt.axis("off")
      chunk = np.array(Image.fromarray(chunk).resize((32,32)))
      chunk = chunk / 255.0
      predictions = savedModel.predict(np.array([chunk]),verbose = 0)
      score = tf.nn.softmax(predictions[0])
      if (100 * np.max(score) > 80):
        result[-1].append([class_names[np.argmax(score)], np.max(score) * 100])
        if class_names[np.argmax(score)] == "House":
          ax.add_patch(plt.Rectangle((0,0), pixels-1.5, pixels-1.5, lw=3, fill=False, color="red"))
          houses = houses + 1
        elif class_names[np.argmax(score)] == "Tree":
          ax.add_patch(plt.Rectangle((0,0), pixels-1.5, pixels-1.5, lw=3, fill=False, color="green"))
          trees = trees + 1
        
      else:
        result[-1].append(['nothing', np.max(score)])

plt.subplots_adjust(wspace=0,hspace=0)
plt.show()

print(result)
print("houses:", houses)
print("trees:", trees)

input("Press [Enter] to continue.") 