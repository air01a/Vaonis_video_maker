import cv2
import numpy as np


def create_title(size, title, subtitle):
    # Paramètres pour l'image d'en-tête
    (header_width,header_height) = size  # Largeur de l'image d'en-tête

    # Créer une image d'en-tête blanche
    header_img = np.zeros((header_height, header_width, 3), dtype=np.uint8) * 255  # Image blanche


    # Taille et position du texte
    title_scale = 3  # Pourcentage de la hauteur de l'image pour le titre (ici environ 30 %)
    subtitle_scale = 1  # Pourcentage de la hauteur de l'image pour le texte (ici environ 10 %)

    # Couleur du texte (noir)
    title_text_color = (255, 172, 102)
    subtitle_text_color = (255, 255, 255)  
    # Ajouter le titre
    font = cv2.FONT_HERSHEY_SIMPLEX
    title_thickness = 3

    # Calculer la position du titre pour le centrer
    title_size = cv2.getTextSize(title, font, title_scale, title_thickness)[0]
    title_x = (header_width - title_size[0]) // 2  # Centrer en largeur
    title_y = int(header_height * 0.4)  # Position verticale (environ 40 % de la hauteur de l'image)

    cv2.putText(header_img, title, (title_x, title_y), font, title_scale, title_text_color, title_thickness, cv2.LINE_AA)


    for i,str in enumerate(subtitle):
    # Ajouter le sous-titre (date)
        print(str)
        subtitle_thickness = 2
        subtitle_size = cv2.getTextSize(str, font, subtitle_scale, subtitle_thickness)[0]
        subtitle_x = title_x    # Décalage à gauche
        subtitle_y = title_y + 50 +i*40  # Juste en dessous du titre

        cv2.putText(header_img, str, (subtitle_x, subtitle_y), font, subtitle_scale, subtitle_text_color, subtitle_thickness, cv2.LINE_AA)
    return header_img

def create_fade_sequence(image, num_images, out=True):
    # Charger l'image source avec OpenCV
    
    # Obtenir les dimensions de l'image source
    height, width, _ = image.shape
    
    # Créer une image noire de la même taille
    black_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Liste pour stocker les images de la séquence
    sequence_images = []
    
    # Générer la séquence d'images
    for i in range(num_images):
        # Calculer le poids de l'image source et de l'image noire
        alpha = 1 - (i / (num_images - 1))  # Le poids de l'image source diminue progressivement
        beta = 1 - alpha  # Le poids de l'image noire augmente progressivement
        
        # Mélanger les deux images
        blended_image = cv2.addWeighted(image, alpha, black_image, beta, 0)
        
        # Ajouter l'image à la séquence
        sequence_images.append(blended_image)
    
    if not out:
        sequence_images=sequence_images[::-1]
    return sequence_images


def zoom_image(image, zoom):
    if zoom==1:
        return image
    height, width = image.shape[:2]

    if (zoom>1):
        new_width = int(width/zoom)
        new_height = int(height/zoom)
        x_start = (width-new_width ) // 2
        y_start = (height-new_height) // 2
        cropped_image = image[y_start:y_start+height, x_start:x_start+width]
    else:
        new_width = int(width*zoom)
        new_height = int(height*zoom)
        x_start = (width-new_width) // 2
        y_start = (height-new_height) // 2
        cropped_image = np.zeros_like(image)
        cropped_image[y_start:y_start+new_height, x_start:x_start+new_width] = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return cropped_image

def resize_with_zoom_effect(image, initial_zoom=1.2, final_zoom=1.0, steps=100):
    # Obtenir les dimensions de l'image
    height, width = image.shape[:2]
    
    # Boucle pour chaque étape de zoom
    for step in range(steps):
        # Calculer le facteur de zoom à cette étape
        zoom_factor = initial_zoom - (initial_zoom - final_zoom) * (step / steps)
        
        cropped_image = zoom_image(image, zoom_factor)
        
        yield cropped_image  # Retourne chaque image dézoomée