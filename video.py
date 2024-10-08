from cv2 import VideoWriter_fourcc, VideoWriter, resize, imread, INTER_AREA
from transition import create_title, create_fade_sequence, resize_with_zoom_effect, zoom_image
from imageprocessing import add_progress_bar


    
def create_video(aligned_images, images, image_folder, new_size, video_filename, fps, title, subtitle,  final_parameters):
    total_image=len(images)

    final_image=None
    if final_parameters!=None:
        (final_image, initial_zoom, final_zoom, step) = final_parameters
    fourcc = VideoWriter_fourcc(*'XVID')  # Codec pour AVI
    video = VideoWriter(video_filename, fourcc, fps, new_size)

    # Texte à afficher


    img_title=create_title(new_size, title,subtitle)
    for _ in range(2*fps):
        video.write(img_title)
        last_img=None
        # Ajouter chaque image à la vidéo
    for img_name in aligned_images:
        img = resize(imread('tmp/'+img_name), new_size, interpolation=INTER_AREA)
        pos = images.index(img_name)
        img=add_progress_bar(img, pos, total_image)
        video.write(img)
        last_img=img

    for i in range(4*fps):
        video.write(last_img)
    for img in create_fade_sequence(last_img, 2*fps):
        video.write(img)
            
    # Libérer l'objet VideoWriter
    if (final_image):
        img_title=create_title(new_size, "Post processed",[])
        for _ in range(2*fps):
            video.write(img_title)
        final_image = imread(image_folder+'/'+final_image)
        for img in create_fade_sequence(final_image, 2*fps,False):
            video.write(resize(zoom_image(img,initial_zoom), new_size, interpolation=INTER_AREA))
        for img in resize_with_zoom_effect(final_image,initial_zoom, final_zoom, step):
            last_image=resize(img, new_size, interpolation=INTER_AREA)
            video.write(last_image)
        for _ in range(5*fps):
            video.write(last_image)

    video.release()