For information see http://research.microsoft.com/en-us/projects/asirra/corpus.aspx

Contact: jelson

# Cat vs. Dog CNN Classifier with Custom Failure-Safe Pipeline

This repository contains a **Convolutional Neural Network (CNN)** built from scratch using **TensorFlow/Keras** to perform binary classification between cats (`0`) and dogs (`1`). 

The main highlight of this project is a **highly robust, failure-safe custom data pipeline** built using `tf.py_function` and Python's `Pillow` library to completely bypass native TensorFlow graph decoder crashes (`DecodeImage`) caused by corrupted bytes, non-RGB channels, and metadata flaws inherent to the historical Microsoft Cats vs. Dogs dataset.

---

## 📊 Model Performance & Statistical Analysis

The model was trained for 30 epochs on a balanced, cleaned subset. Rather than just relying on standard accuracy metrics, a customized tracking suite was engineered to analyze training speed, degradation, and overfitting zones.

### Metrics Insights:
* **Optimal Stopping Point:** The `Divergence Heatmap` and `Learning Velocity (Gradient)` models mapped peak validation harmony exactly at **Epoch 24**. 
* **Overfitting Mitigation:** By implementing dynamic on-the-fly **Data Augmentation** and a **50% Dropout layer**, the `Validation Loss` cleanly mirrored the `Training Loss` down to a steady ~0.35 baseline.
* **Accuracy:** Stable convergence was achieved on both training and validation splits at **~85% accuracy**.
* **Error Fluctuations:** Spikes in the `Generalization Error %` (e.g., Epoch 7 and 14) indicate epochs where the model attempted to memorize background noise but was penalized and self-corrected in subsequent passes.

---

## 📂 Project Architecture

```text
.
├── Cleaning_DataSet.py     # Independent script for hexadecimal and channel validation
├── configuracoes.py        # Central configuration center (ignored by Git for deployment safety)
├── p1.ipynb                # Main Jupyter Notebook containing the safe pipeline & CNN architecture
├── .gitignore              # Configured to drop virtual environments and heavy datasets
└── README.md               # You are here!
```
# 🛠️ Data Pipeline Engineering (Failure-Safe Design)

The Microsoft Cats vs. Dogs dataset contains several broken files (e.g., zero-byte images, text files masked with `.jpg` extensions, or 2-channel grayscale matrices) that cause standard Keras loading layers to break mid-training. This architecture uses a two-tier defense system:

1. Hexadecimal Magic Bytes Scan (Cleaning_DataSet.py)Before loading, this script scans the files at a binary level. It reads the first 8 bytes of every single image file to ensure it aligns with actual standardized image signatures, throwing away corrupted structural clones:

* JPEG: Begins with `b'\xff\xd8\xff'`
* PNG: Begins with `b'\x89PNG\r\n\x1a\n'`
 
2. The tf.py_function Runtime WrapperDuring batch mapping inside the dataset pipeline, the system drops native C++ graph execution and falls back into a pure Python processing layer. If a corrupted image sneaks past the initial validation scan, the `try/except` block catches the OS read error and injects a solid black image placeholder tensor array `(np.zeros)` into the batch queue, entirely preventing execution crashes.

# 🚀 How to Run Locally1.

#### 1. Requirements: Ensure you are running inside a virtual environment `(venv)`. Install the required dependencies:
```
Bash pip install tensorflow pillow numpy pandas matplotlib seaborn`
```

#### 2. Dataset Setup
* Download the official Microsoft PetImages dataset.
* Extract the archive into your workspace root folder.
* Ensure the structural path looks like this: PetImages/Cat/ and PetImages/Dog/.
  
#### 3. Execution Flow
1. Run the data validation pipeline directly from your terminal to filter out corrupt structural files and unify color channels to 3-channel RGB space:
```  
Bashpython -u Cleaning_DataSet.py
```
2. Launch your Jupyter Environment and run `p1.ipynb.`
   
The custom glob mapping layer will read, slice, and stream your datasets safely, allowing you to train the model completely smoothly on CPU or integrated graphic processing setups (such as Intel Iris Xe).

# 🧠 CNN Architecture Summary
The sequential network architecture wraps the dataset with strict safety walls:
* Layer 1: Data Augmentation: Applies random horizontal flipping, scaling, and small rotations on runtime memory to synthetically expand variations.
* Layer 2: Rescaling: Standardizes pixel byte weights from [0, 255] to a floating [0, 1] tensor space.
* Layers 3-6: Feature Extraction: Dual Conv2D feature filters (32 and 64 kernel channels) interlaced with MaxPooling2D to condense positional data.
* Layers 7-9: Dense Regularization: Flattened arrays pipe into a 64-neuron Dense Layer, choked with a Dropout(0.5) gate to strip dependent pathways before terminating into a binary Sigmoid classifier node.
