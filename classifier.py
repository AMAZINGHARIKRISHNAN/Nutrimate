import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping

# Load the dataset
file_path = 'food.csv'
data = pd.read_csv(file_path, encoding='utf-8')  # Changed to utf-8 for better compatibility

# Display the first few rows of the dataset
print(data.head())

# Define a threshold for "healthy" vs "unhealthy" based on calories
calorie_threshold = 200  # Adjust as needed

# Create labels based on calories
data['Label'] = np.where(data['Calories'] > calorie_threshold, 'unhealthy', 'healthy')

# Display the updated dataset with labels
print(data.head())

# Use the 'Food' column as the text data
texts = data['Food'].values
labels = data['Label'].values

# Preprocess the labels: Convert "healthy" and "unhealthy" into binary values
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)  # 0: healthy, 1: unhealthy

# Tokenize the text data
tokenizer = Tokenizer(num_words=5000)  # Use a max vocabulary size of 5000
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Pad sequences to the same length (for LSTM input)
max_len = 20  # Adjust based on the average length of food descriptions
X = pad_sequences(sequences, maxlen=max_len)

# Split data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, labels, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Display the shapes of the training and test data
print(f"Training data shape: {X_train.shape}, Training labels shape: {y_train.shape}")
print(f"Validation data shape: {X_val.shape}, Validation labels shape: {y_val.shape}")
print(f"Test data shape: {X_test.shape}, Test labels shape: {y_test.shape}")

# Build the LSTM model
model = Sequential()
model.add(Embedding(input_dim=5000, output_dim=128, input_length=max_len))  # Embedding layer
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))  # LSTM layer
model.add(Dense(1, activation='sigmoid'))  # Output layer for binary classification

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Define EarlyStopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Train the model
model.fit(X_train, y_train, epochs=18, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stopping])

# Evaluate the model on the test data
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy * 100:.2f}%")

# Additional evaluation metrics
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Function to predict healthiness of food description based on user input
def predict_healthiness(food_description):
    food_description = food_description.strip()  # Clean input
    if not food_description:  # Check for empty input
        return "Input cannot be empty."
    
    new_seq = tokenizer.texts_to_sequences([food_description])
    new_pad = pad_sequences(new_seq, maxlen=max_len)
    prediction = model.predict(new_pad)
    predicted_label = "unhealthy" if prediction > 0.5 else "healthy"
    return predicted_label

# Test the prediction function
user_input = input("Enter a food description to check if it's healthy or unhealthy: ")
predicted_label = predict_healthiness(user_input)
print(f"Predicted label: {predicted_label}")
