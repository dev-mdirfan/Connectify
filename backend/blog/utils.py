from django.core.files import File
from pathlib import Path
from PIL import Image
from io import BytesIO

image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}

def image_resize(image, width, height):
    # Open the image using Pillow
    img = Image.open(image)
    
    # Calculate the aspect ratio
    aspect_ratio = width / height
    
    # Calculate the new dimensions for a 3:2 aspect ratio
    new_width = int(img.height * aspect_ratio)
    
    # Resize the image to the new dimensions
    img = img.resize((new_width, img.height))
    
    # Find the file name of the image
    img_filename = Path(image.file.name).name
    
    # Spilt the filename on “.” to get the file extension only
    img_suffix = Path(image.file.name).name.split(".")[-1]
    
    # Use the file extension to determine the file type from the image_types dictionary
    img_format = image_types[img_suffix]
    
    # Save the resized image into the buffer, noting the correct file type
    buffer = BytesIO()
    img.save(buffer, format=img_format)
    
    # Wrap the buffer in File object
    file_object = File(buffer)
    
    # Save the new resized file as usual
    image.save(img_filename, file_object)
