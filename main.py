# -*- coding: utf-8 -*-
import os
from PIL import Image

from imageprocessing import align_image
from video import create_video
import multiprocessing
from multiprocessing import Process, Value, Array


# Folder with image
image_folder = "M31/"
video_filename = "M31.avi"
final_image = "m31.png"
title = "M31 - Androméde"
subtitle = ["2024-09-21", 'Vespera pro','983 images, 10 sec expo']
# Size of video
new_size = (800, 800)
fps = 20  # Framerate
image_selector_rate= [(50,1),(200,2),(800,4),(1200,8)]
initial_zoom=1.2
final_zoom=1

use_cache=True
cache_only=False


# Create chunks of image to process to distribute to all processor
def divide_chunks(data, n):
    # Répartir data en n sous-listes de taille presque égale
    for i in range(0, len(data), n):
        yield data[i:i + n]
        
# Aligning image 
def process_images(selected_images,ref_image, image_folder, use_cache, cache_only, image_to_process,image_treated):
    for img_name in selected_images:
        print("Managing image %i on %i (%i %%) " % (image_treated.value,image_to_process,int(100*image_treated.value/image_to_process)))
        with image_treated.get_lock():  
            image_treated.value+=1
        img_path = os.path.join(image_folder, img_name)
        if os.path.isfile('tmp/'+os.path.basename(img_name)) and use_cache:
            print("Using cache")
        else:
            if not cache_only:
                aligned_img = align_image(img_path, ref_image)

        


if __name__=='__main__':

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


    # Define multi processing parameters
    num_processes = multiprocessing.cpu_count()
    file_chunks = list(divide_chunks(selected_images, len(selected_images) // num_processes + 1))
    image_treated = Value('i', 0) 
    args = [(chunk, ref_image, image_folder, use_cache,  cache_only, image_to_process,image_treated) for chunk in file_chunks]

    # Run multi processor for image alignment 
    procs = []
    for arg in args:
        p = Process(target=process_images, args=(arg))
        procs.append(p)
        p.start()
    
    for proc in procs:
        proc.join()


    # Get processed images
    aligned_images=[]
    for f in selected_images:
        if os.path.isfile('tmp/'+f):
            aligned_images.append(f)

    aligned_images = sorted(aligned_images)
    print(f"Creating Video : {video_filename}")

    # Create the final video with aligned images
    create_video(aligned_images, images, image_folder, new_size, video_filename, fps, title, subtitle, (final_image,initial_zoom,final_zoom,100))
    print(f"Video has been successfully created: {video_filename}")

