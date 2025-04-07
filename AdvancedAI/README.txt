# House and Tree Detection with CNNs

This project uses a Convolutional Neural Network (CNN) to detect objects (Houses and Trees) in aerial images by analyzing image chunks in a grid layout. It's implemented using TensorFlow/Keras and includes both model training and image inference workflows.

## 🔍 Features

- **Model Training (`MakeModel.py`)**
  - Loads labeled data from `Dataset.csv`
  - Adds grayscale image augmentation
  - Builds and trains a CNN using TensorFlow/Keras
  - Saves a `.h5` model file (`BST_B10_E10_G1.h5`)

- **Object Detection (`ObjectDetection.py`)**
  - Loads an image and divides it into a grid (default 4x4)
  - Predicts each chunk using the saved model
  - Highlights detected objects:
    - **Red box** for Houses
    - **Green box** for Trees
  - Prints classification results and confidence scores

- **Jupyter Notebooks**
  - `tensorflowDetection.ipynb`: Interactive version using TensorFlow
  - `torchDetection.ipynb`: A PyTorch-based experimental notebook (optional alternative)

## 🧠 Model Architecture

The CNN consists of:
- Random data augmentation (flip, rotation)
- Three convolutional layers with ReLU and max pooling
- Dense layers with softmax output for 2 classes

## 📁 File Overview

| File | Description |
|------|-------------|
| `MakeModel.py` | Loads data, trains and saves the model |
| `ObjectDetection.py` | Loads a saved model, runs grid-based detection |
| `Dataset.csv` | Contains labeled bounding boxes and class names |
| `tensorflowDetection.ipynb` | Notebook version using TensorFlow |
| `torchDetection.ipynb` | Notebook version using PyTorch |
| `images/` | Folder with training and test images |
| `BST_B10_E10_G1.h5` | Trained model (needs to be generated or added manually) |

## 📊 Dataset Format (`Dataset.csv`)

Each row must include:
- `image_name`: filename in the `images/` folder
- `bbox_x`, `bbox_y`: top-left corner of bounding box
- `bbox_width`, `bbox_height`: size of bounding box
- `label_name`: either `House` or `Tree`

## 🛠️ Requirements

Install the required Python packages:

```bash
pip install tensorflow keras numpy matplotlib pillow csv torch