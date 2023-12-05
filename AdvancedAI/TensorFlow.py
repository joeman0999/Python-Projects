import tensorflow as tf
import numpy as np

# a. create n dimensional tensor

n = 5
nDim = [2] * n
nDimTensor = tf.random.uniform(nDim, minval=1, maxval=6, dtype=tf.int64)

print("dimensions: ")
print(tf.rank(nDimTensor))

print("shape: ")
print(tf.shape(nDimTensor))

print("\nn dimensional tensor: ")
print(nDimTensor)

# b. Compute the sum, mean, and standard deviation of all elements in a tensor.

sum = np.sum(nDimTensor)
print("\nSum of elements: ", sum)

mean = np.mean(nDimTensor)
print("\nMean of elements: ", mean)

std = np.std(nDimTensor)
print("\nStandard Deviation of elements: ", std)

# c. Perform mathematical operations on tensors, such as finding the maximum or minimum value, or taking the dot product of two tensors.

t1 = tf.constant([[1,2,3,5], [4,5,6,1], [7,9,9,9]])
t2 = tf.constant([[1,2,3,4], [3,5,5,5], [7,8,9,6], [2,7,1,9]])

dot = t1 @ t2
print("\ndot product: ")
print(dot)

# d. Access and manipulate specific elements or slices of a tensor, and index and slice tensors based on certain conditions.

print("\nTensor 2: ")
print(t2)

print("\nA slice of Tensor 2: ")
print(t2[0:2, 1:3])

t2 = tf.where(t2 < 4, 0, t2) # tf.where(condition, x, y) where x is True and y isFalse
print("\nTensor 2 with values less than 4 set to 0: ")
print(t2)

# e. Define and call functions in TensorFlow, and pass tensors as arguments to functions

def addToIndex(tensor, index, value):
    values = np.zeros(tf.shape(tensor))
    values[tuple(index)] = 1
    newTensor = tf.where(values == 1, tensor + value, tensor)
    return newTensor

t2 = addToIndex(t2, [0,1], 3)
print("\nTensor 2 with index [0,1] plus 3: ")
print(t2)

def addToSlice(tensor, index, value):
    values = np.zeros(tf.shape(tensor))
    values[index] = 1
    newTensor = tf.where(values == 1, tensor + value, tensor)
    return newTensor

t2 = addToSlice(t2, [1], 6)
print("\nTensor 2 with row 1 plus 6: ")
print(t2)