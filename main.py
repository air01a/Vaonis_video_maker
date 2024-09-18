import cv2
import os
from PIL import Image

from imageprocessing import align_image
from video import create_video


# Folder with image
image_folder = "2024-09-13 - NGC6992/"
video_filename = "sequence_astro.avi"
final_image = "ngc6992.png"
title = "NGC6992"
subtitle = ["2024-09-19", 'Vespera pro','470 images, 10 sec expo']
# Size of video
new_size = (800, 800)
fps = 10  # Framerate


use_cache=True
cache_only=False


image_selector_rate= [(50,1),(200,2),(400,4),(800,8)]


# List all files
images = sorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])
total_image = len(images)


# Image selection
(last_index,rate) = image_selector_rate[0]
selected_images = images[:last_index]
for (index,rate) in image_selector_rate:
    selected_images+=images[last_index:index:rate]
    last_index=index+1

image_to_process=len(selected_images)


# load reference image
ref_image_path = os.path.join(image_folder, selected_images[int(len(selected_images)/2)])  # Choisis l'image de référence vers le milieu
ref_image = Image.open(ref_image_path)

# List of aligned images
aligned_images = []

i=1
# Aligning image
for img_name in selected_images:
    print("Managing image %i on %i (%i %%) " % (i,image_to_process,int(100*i/image_to_process)))
    img_path = os.path.join(image_folder, img_name)
    if os.path.isfile('tmp/'+os.path.basename(img_name)) and use_cache:
        print("Using cache")
        aligned_images.append(os.path.basename(img_name))
    else:
        if not cache_only:
            aligned_img = align_image(img_path, ref_image)
            if aligned_img is not None:        
                aligned_images.append(aligned_img)
    i+=1


create_video(aligned_images, images, image_folder, new_size, video_filename, fps, title, subtitle, final_image)
print(f"Vidéo créée avec succès : {video_filename}")

