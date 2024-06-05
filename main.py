# This is very basic example 
import ollama
from ollama import generate

import glob
from PIL import Image

import os
from io import BytesIO
import cv2 
import pyttsx3
engine = pyttsx3.init()


cap = cv2.VideoCapture(1) 


def read_camera_frame():
    # Read and display each frame 
    ret, img = cap.read() 
    cv2.imshow('a', img) 
  
    # check for the key pressed 
    k = cv2.waitKey(125) 
    
    ret, img = cap.read() 
    # Display the clicked frame for 2  
    # sec.You can increase time in  
    # waitKey also 
    cv2.imshow('a', img) 

    # time for which image displayed 
    cv2.waitKey(2000) 

    # Save the frame 
    cv2.imwrite('camera.jpg', img) 


# processing the images 
def process_image(image_file):
    print(f"\nProcessing {image_file}\n")
    with Image.open(image_file) as img:
        with BytesIO() as buffer:
            img.save(buffer, format='JPEG')
            image_bytes = buffer.getvalue()

    full_response = ''
    # Generate a description of the image
    for response in generate(model='llava', 
                             prompt='describe this image and make sure to include anything notable about it. Be brief.', 
                             images=[image_bytes], 
                             stream=True):
        # Print the response to the console and add it to the full response
        print(response['response'], end='', flush=True)
        full_response += response['response']
    
    engine.say(full_response)
    engine.runAndWait() 


def main():
    while True:
        read_camera_frame()
        process_image("camera.jpg")    

main()