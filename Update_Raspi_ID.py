import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.utils import class_weight
from keras.models import Sequential
from keras.layers import Conv1D, LSTM, Dense, MaxPooling1D, Dropout, BatchNormalization, ReLU, Bidirectional
from keras.optimizers import RMSprop, Adam
from tensorflow.keras.utils import to_categorical
from keras.callbacks import History
import keras_cv


#Updated code for raspberry Pi
#this should imagine user 2 and user 3 are the authorized users and everyone else is an imposter
#

global json_folder_path
json_folder_path = r'Specify-Path-to-Folder-of-JSON-PPG-Signals'  # Update with your path

global json_files
json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]

# Function to apply a moving average filter
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Function to create the CNN + LSTM model
def create_model(input_shape,num_classes):
    model = Sequential()

    # First 1D convolutional layer
    model.add(Conv1D(filters=16, kernel_size=8, activation='selu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.1))

    # Second 1D convolutional layer
    model.add(Conv1D(filters=16, kernel_size=8, activation='selu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.1))

    # 1st LSTM layer
    model.add(LSTM(128, activation='tanh', return_sequences=True))

    # 2nd LSTM layer
    model.add(LSTM(128, activation='tanh'))

    # Fully connected layer for 3-class classification
    model.add(Dense(num_classes, activation='softmax'))

    # Compile the model
    optimizer = RMSprop()
    # optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss=keras_cv.losses.FocalLoss(), metrics=['accuracy'])

    return model

# Data Preprocessing and Loading from JSON
#json_folder is the folder with all the trials across all users
#fs is the frame rate of the camera used
def load_data(json_folder, fs, window_size=9, num_of_seconds=15):
    num_of_datapoints = int(fs) * num_of_seconds

    X = []  # Store the PPG data
    y = []  # Store the labels (2 for user 2, 3 for user 3, 0 for others)

    for idx, json_file in enumerate(json_files):
        full_file_path = os.path.join(json_folder, json_file)

        # Open and load the JSON data
        with open(full_file_path, 'r') as f:
            ppg_data = json.load(f)

        # print(f"ppg_data: {ppg_data}")

        # Apply moving average filter
        filtered_ppg_data = moving_average(ppg_data, window_size)

        # Get the first N data points
        inputPPG = filtered_ppg_data[:num_of_datapoints]

        # Labeling
        if "User1" in json_file:
            label = 1  # User1
        elif "User2" in json_file:
            label = 2  # User2
        elif "User3" in json_file:
            label = 3  # User3
        else:
            label = 0  # Imposter

        print(f"signal: {json_file}, label: {label}")
        X.append(inputPPG)
        y.append(label)

    X = np.array(X)
    X = np.expand_dims(X, axis=2)  # Expand dimensions to (samples, time points, 1 channel)
    y = np.array(y)
    # print("Finished loading data!")
    return X, y

# Main Function to Run the Program
def run_identification(json_folder):
    # Sampling frequency and filtering parameters
    fs = 30
    window_size = 9

    # Load data
    X, y = load_data(json_folder, fs, window_size)

    # 5-fold stratified cross-validation
    kf = StratifiedKFold(n_splits=5, shuffle=True)  # Stratified ensures balanced splits
    subject_accuracies = []
    f1_scores_per_fold = []
    precision_scores_per_fold = []
    recall_scores_per_fold = []
    all_true_labels = []
    all_predicted_labels = []
    history_list = []

    for fold, (train_index, test_index) in enumerate(kf.split(X, y)):
        print(f"Training fold {fold + 1}...")

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        num_classes = 4

        # Get corresponding JSON files for the training and test sets
        train_files = [json_files[i] for i in train_index]
        test_files = [json_files[i] for i in test_index]

        # Print the JSON files used for training and testing
        print(f"Training files for fold {fold + 1}:")
        for file in train_files:
            print(f"- {file}")

        print(f"\nTest files for fold {fold + 1}:")
        for file in test_files:
            print(f"- {file}")

        print(f"y_train: {y_train}")
        print(f"y_test: {y_test}")

        # Compute class weights for imbalanced data
        class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
        class_weights_dict = dict(enumerate(class_weights))
        print(f"class weights: {class_weights_dict}")

        binary_y_train = to_categorical(y_train, num_classes=num_classes)
        binary_y_test = to_categorical(y_test, num_classes=num_classes)

        print(f"binary_y_train: {binary_y_train}")
        print(f"binary_y_test: {binary_y_test}")

        # Create and train the model
        model = create_model(input_shape=(X_train.shape[1], 1), num_classes=num_classes)

        # Print the model architecture
        print("\nModel Summary:")
        model.summary()

        # Track signal shape as it passes through the model
        input_signal_shape = X_train.shape
        print(f"\nInput Signal Shape: {input_signal_shape}")
        for layer in model.layers:
            input_signal_shape = layer.compute_output_shape(input_signal_shape)
            print(f"Shape after layer {layer.name}: {input_signal_shape}")

        history = model.fit(X_train, binary_y_train,
                            validation_data=(X_test, binary_y_test), epochs=100, batch_size=25,
                            verbose=1)#, class_weight=class_weights_dict)

        history_list.append(history)

        # Predict on the test set
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(binary_y_test, axis=1)  # [0 0 1 0 0 0]

        print(f"y_pred: {y_pred}")
        print(f"y_pred_classes: {y_pred_classes}")
        print(f"y_true_classes: {y_true_classes}")

        # Confusion matrix for this fold
        cm = confusion_matrix(y_true_classes, y_pred_classes)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap=plt.cm.Blues)
        plt.title(f'Confusion Matrix - Fold {fold + 1}')
        plt.show()

        # Store true and predicted labels for confusion matrix computation
        all_true_labels.extend(y_true_classes)
        all_predicted_labels.extend(y_pred_classes)

        # Evaluate performance metrics for this fold
        accuracy = accuracy_score(y_true_classes, y_pred_classes)
        f1 = f1_score(y_true_classes, y_pred_classes, average='macro')
        precision = precision_score(y_true_classes, y_pred_classes, average='macro')
        recall = recall_score(y_true_classes, y_pred_classes, average='macro')

        subject_accuracies.append(accuracy)
        f1_scores_per_fold.append(f1)
        precision_scores_per_fold.append(precision)
        recall_scores_per_fold.append(recall)

        print(f"Fold {fold + 1} - Accuracy: {accuracy:.4f}, F1 Score: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")

        # Plot accuracy vs. epochs for this fold
        plt.figure(figsize=(10, 5))
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title(f'Accuracy vs. Epochs - Fold {fold + 1}')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True)
        plt.show()

    # Save the model after training
    model_save_path = "./ppg_model.h5"  # Specify your model save path
    model.save(model_save_path)  # Save the model
    print(f"Model saved to {model_save_path}")

    # Combined confusion matrix
    combined_cm = confusion_matrix(all_true_labels, all_predicted_labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=combined_cm)
    disp.plot(cmap=plt.cm.Blues)
    plt.title('Combined Confusion Matrix')
    plt.show()

    # Overall metrics across folds
    overall_accuracy = np.mean(subject_accuracies)
    overall_f1 = np.mean(f1_scores_per_fold)
    overall_precision = np.mean(precision_scores_per_fold)
    overall_recall = np.mean(recall_scores_per_fold)

    print(f"Overall Mean Accuracy: {overall_accuracy:.4f}")
    print(f"Overall Mean F1 Score: {overall_f1:.4f}")
    print(f"Overall Mean Precision: {overall_precision:.4f}")
    print(f"Overall Mean Recall: {overall_recall:.4f}")

# Define the path to the JSON folder
run_identification(json_folder_path)

