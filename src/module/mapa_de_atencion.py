from matplotlib.lines import Line2D
import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image
from transformers import ViTModel, ViTFeatureExtractor, AutoImageProcessor, ViTForImageClassification
import matplotlib.pyplot as plt
from PIL import Image
import asyncio
import torch.nn.functional as F
import cv2

# Cargar el modelo preentrenado y extractor de características
model = ViTModel.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')
feature_extractor = ViTFeatureExtractor.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')
image_processor = AutoImageProcessor.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')
model1 = ViTForImageClassification.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')

# Obtener los valores de atención
async def clasifica(image: Image.Image):
    inputs = feature_extractor(images=image, return_tensors="pt")
    inputs1 = image_processor(image, return_tensors="pt")

    with torch.no_grad():
        logits = model1(**inputs1).logits
        outputs = model(**inputs, output_attentions=True)
        attentions = outputs.attentions

    probabilities = F.softmax(logits, dim=-1)

    # Obtener la clase predicha y su probabilidad
    predicted_label = logits.argmax(-1).item()
    resultado = model.config.id2label[predicted_label]
    porcentaje_certeza = probabilities[0, predicted_label].item()

    processed_image = graphicmap(attentions, image, resultado)
    
    return resultado, str(porcentaje_certeza)[2:4], processed_image


# Función para realizar el Attention Rollout

def compute_rollout(attentions, use_layers=[-1, -7, -9]):
    result = torch.eye(attentions[0].size(-1))
    
    # Filtrar solo las capas seleccionadas
    attentions = [attentions[layer] for layer in use_layers]

    for attention in attentions:
        attention_heads_fused = attention.mean(dim=1)
        attention_heads_fused += torch.eye(attention_heads_fused.size(-1))
        attention_heads_fused /= attention_heads_fused.sum(dim=-1, keepdim=True)
        result = torch.matmul(result, attention_heads_fused)
    
    return result[0, 0, 1:]

def graphicmap(attentions, image: Image.Image, resultado):
    
    rollout = compute_rollout(attentions)
    rollout = rollout.reshape(14, 14)

    rollout = rollout.numpy()
    rollout = Image.fromarray(rollout).resize(image.size, resample=Image.BILINEAR)
    rollout = np.array(rollout)

    image_np = np.array(image)
    image1 = image_np

    threshold_value = 0.0038

    _, binary_mask = cv2.threshold(rollout, threshold_value, 0.05, cv2.THRESH_BINARY)

    binary_mask = (binary_mask * 255).astype(np.uint8)

    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contoured_image = image1.copy()
    cv2.drawContours(contoured_image, contours, -1, (0, 255, 255), 3)  # Contorno en color rojo (BGR) y grosor 2

    plt.imshow(contoured_image)
    plt.title("Imagen analizada")
    plt.axis('on')

    legend_elements = [
        Line2D([0], [0], color=(0/255, 255/255, 255/255), lw=2, label='Resultado: ' + resultado)
    ]

    plt.legend(handles=legend_elements, loc='lower left', fontsize=12)
    return Image.fromarray(contoured_image)