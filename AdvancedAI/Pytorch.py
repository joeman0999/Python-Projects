import torch
import numpy as np

# a. create n dimensional tensor
n = 5
nDim = [2] * n
nDimTensor = torch.rand(nDim, dtype=torch.float32) 
print("shape: ")
print(nDimTensor.shape)

print("\nn dimensional tensor: ")
print(nDimTensor)

# b. Compute the sum, mean, and standard deviation of all elements in a tensor.

sum = nDimTensor.sum()
print("\nSum: ", sum)

mean = nDimTensor.mean()
print("\nMean: ", mean)

std = nDimTensor.std()
print("\nStd: ", std)

# c. Perform mathematical operations on tensors, such as finding the maximum or minimum value, or taking the dot product of two tensors.

max = torch.max(nDimTensor)
print("\nMax: ", max)

# Find min value in all tensors.
min = torch.min(nDimTensor)
print("\nMin: ", min)

# d. Access and manipulate specific elements or slices of a tensor, and index and slice tensors based on certain conditions.

slice = nDimTensor[1,0]
print("Slice: ")
print(slice)
sumAll = torch.sum(slice, dim=1)
print("Sums of slice: ")
print(sumAll)
for i in range(len(sumAll)):
    for j in range(len(sumAll[i])):
        if(sumAll[i][j] > 1):
            print(sumAll[i][j]) # print the sum
print("\n")

# e. Define and call functions in TensorFlow, and pass tensors as arguments to functions

def normalize(image):
    imgNormalized = image / 255
    return imgNormalized

# 256 x 256 image with RBG values in range 0:255
img = np.random.rand(256,256,3) * 255
img = img.astype(np.uint8)

imgTensor = torch.from_numpy(img)
imgNor = normalize(imgTensor) # Normalize image
print("Image: ")
print(imgNor)
