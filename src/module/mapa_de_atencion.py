from matplotlib.lines import Line2D
import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image
from transformers import ViTModel, ViTFeatureExtractor, AutoImageProcessor, ViTForImageClassification
import matplotlib.pyplot as plt
from PIL import Image
import asyncio

# Cargar el modelo preentrenado y extractor de características
model = ViTModel.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')
feature_extractor = ViTFeatureExtractor.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')
image_processor = AutoImageProcessor.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')
model1 = ViTForImageClassification.from_pretrained('F:/entrenamientos/fastapi/species_catalogue/src/module/vit-base-patch16-224-mascotas')

# Obtener los valores de atención
async def clasifica(image: Image.Image):
    print('entró a clasificador')
    inputs = feature_extractor(images=image, return_tensors="pt")
    inputs1 = image_processor(image, return_tensors="pt")

    with torch.no_grad():
        logits = model1(**inputs1).logits
        outputs = model(**inputs, output_attentions=True)
        attentions = outputs.attentions


    predicted_label = logits.argmax(-1).item()
    resultado = model.config.id2label[predicted_label]
    print(resultado)
    return resultado

"""
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

# Calcular el mapa de atención
rollout = compute_rollout(attentions)
rollout = rollout.reshape(14, 14)  # Cambia la forma según tu configuración de ViT

# Redimensionar el mapa de atención a la resolución original de la imagen
rollout = rollout.numpy()
rollout = Image.fromarray(rollout).resize(image.size, resample=Image.BILINEAR)
rollout = np.array(rollout)

# Cargar la imagen original
image = cv2.imread(url)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Verificar el rango de valores en el mapa de atención
print("Rango de valores en rollout:", rollout.min(), rollout.max())

# Ajustar el umbral para que sea adecuado para los valores de rollout
threshold_value = 0.0038  # Ajusta este valor según sea necesario
 
# Umbralizar el mapa de atención para crear una máscara binaria
_, binary_mask = cv2.threshold(rollout, threshold_value, 0.05, cv2.THRESH_BINARY)

# Convertir la máscara binaria a un formato de 8 bits (0-255)
binary_mask = (binary_mask * 255).astype(np.uint8)

# Verificar la máscara binaria
#plt.imshow(binary_mask, cmap='gray')
#plt.title("Máscara Binaria")
#plt.axis('off')
#plt.show()

# Encontrar los contornos en la máscara binaria
contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Verificar el número de contornos encontrados
print("Número de contornos encontrados:", len(contours))

# Dibujar los contornos sobre la imagen original
contoured_image = image.copy()
cv2.drawContours(contoured_image, contours, -1, (0, 255, 255), 3)  # Contorno en color rojo (BGR) y grosor 2

# Mostrar la imagen original con los contornos
plt.imshow(contoured_image)
plt.title("Imagen analizada")
plt.axis('on')
# Agregar la etiqueta en el pie de la imagen
#plt.text(0, 330, '**Áreas de atención', color='blue', fontsize=12, ha='left')
# Crear un proxy para la leyenda
legend_elements = [
    #Line2D([0], [0], color='w', lw=0, label='Resultado: ' + resultado),
    Line2D([0], [0], color=(0/255, 255/255, 255/255), lw=2, label='Resultado: ' + resultado)
]
# Agregar la leyenda
plt.legend(handles=legend_elements, loc='lower left', fontsize=12)
plt.show()
"""