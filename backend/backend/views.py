"""
This file contains the code for the API endpoint that will be used to make predictions on the images.
"""

from django.http import JsonResponse
from rest_framework.decorators import api_view
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg19 import preprocess_input
from PIL import Image
import numpy as np
from io import BytesIO
import os

# Loading your pre-trained model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'backend', 'model.h5')
model = load_model(model_path)

@api_view(['POST'])
def predict_image(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)
    file = request.FILES['file']
    image = Image.open(BytesIO(file.read()))
    
    # Converting image to RGB format
    image = image.convert('RGB')
    
    image = image.resize((224, 224))  
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction[0])
    result = 'fresh' if predicted_index < 6 else 'rotten'  
    
    return JsonResponse({'status': result})