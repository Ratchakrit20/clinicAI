from tensorflow.keras.models import load_model

# Load the model
model = load_model('path/to/your/model.h5')

# Use the model for predictions
predictions = model.predict(input_data)
