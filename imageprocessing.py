from cv2 import rectangle, putText, FONT_HERSHEY_SIMPLEX, fillPoly, LINE_AA
from numpy import uint8, array as np_array
from PIL import Image
import astroalign as aa
from os import path

def add_progress_bar(image, current_index, total_images):
    # Créer une copie de l'image pour ne pas modifier l'originale
    image_copy = image.copy()

    # Dimensions de la barre
    bar_x = 30  # Position X de la barre
    bar_y_start = 20  # Position Y de départ
    bar_height = 100  # Hauteur de la barre
    bar_width = 5  # Largeur de la barre

    # Couleurs (BGR)
    bar_color = (255, 255, 255)  # Blanc
    triangle_color = (0, 0, 255)  # Rouge
    text_color = (255, 255, 255)  # Blanc

    # Ajouter la barre verticale
    rectangle(image_copy, (bar_x, bar_y_start), (bar_x + bar_width, bar_y_start + bar_height), bar_color, -1)

    # Ajouter le texte '0' en dessous
    font = FONT_HERSHEY_SIMPLEX
    putText(image_copy, '0', (bar_x, bar_y_start + bar_height + 15), font, 0.5, text_color, 1, LINE_AA)

    # Ajouter le texte du nombre total d'images en haut
    putText(image_copy, str(total_images), (bar_x, bar_y_start - 5), font, 0.5, text_color, 1, LINE_AA)

    # Calculer la position du triangle pour indiquer la position actuelle
    relative_position = 1-current_index / (total_images - 1)
    triangle_y = int(bar_y_start + relative_position * bar_height)

    # Dessiner le triangle
    triangle_size = 10
    points = np_array([
        [bar_x, triangle_y],
        [bar_x-triangle_size, triangle_y - triangle_size // 2],
        [bar_x-triangle_size, triangle_y + triangle_size // 2]
    ])
    fillPoly(image_copy, [points], triangle_color)

    return image_copy



# Fonction pour aligner une image sur l'image de référence avec Astroalign
def align_image(image_path, ref_image):
    img = Image.open(image_path)
    # Aligner l'image avec astroalign
    try:
        aligned_img, footprint = aa.register(img, ref_image)
    except Exception as e:
        print(f"Erreur lors de l'alignement de {image_path} : {e}")
        return None
    image_temp=Image.fromarray(uint8(aligned_img)).convert('RGB')
    base_name = path.basename(image_path)
    image_temp.save('tmp/'+base_name)
    # Redimensionner l'image alignée
    return base_name