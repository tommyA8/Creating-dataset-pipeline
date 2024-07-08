import os
import argparse
import cv2    
import shutil        

"""
Before annotating
    1. video 2 images (video-cli Lib.)
    (on this file)
    2. rename
    3. resize

After annotating

    1. labelme2yolo
    2. augmentation
"""

def rename_raw_image(source, name):
    try:
        for filename in (os.listdir(source)):
            if not filename.endswith(".jpg"):
                continue
            re_name = f"{name}_{filename}"
            # print(filename, "=>", re_name)
            
            src =f"{source}/{filename}"  # foldername/filename, if .py file is outside folder
            dst =f"{source}/{re_name}" # raw_video/footage1/rename_footage1/footage1-00000.jpg
            # rename() function will
            # rename all the files
            # shutil.copyfile(src, dst)
            shutil.move(src, dst)

    except NameError:
        print("Please put the folder path")
                      
def resize_img(source, img_size, dst_folder):
    try: 
        for filename in os.listdir(source):
            if not filename.endswith(".jpg"):
                continue

            image = f"{source}/{filename}"
            im = cv2.imread(image)
            resized = cv2.resize(im, img_size, cv2.INTER_AREA)
            output_name = filename[:-4]+"_resized"+".jpg"
            
            dst = f"{dst_folder}/{output_name}"
            cv2.imwrite(dst, resized)
    except NameError:
        print("Please put the folder path")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Please put the folder path")
    
    parser.add_argument("--source",
                        type=str,
                        help="Source. Path to the input image. or folder")

    parser.add_argument("--name",
                        type=str,
                        help="rename")
        
    parser.add_argument("--destination",
                        type=str,
                        default="pre-processed-images",#"dataset/resized_raw_images",
                        help="destination path for results")
        
    parser.add_argument("--width",
                        type=int,
                        default=640,
                        help="example -width 640")
    
    parser.add_argument("--height",
                        type=int,
                        default=640,
                        help="example -height 640")
    
    args = parser.parse_args()

    
    if args.destination != "pre-processed-images":
        # rename
        rename_raw_image(args.source, args.name)
        # resize
        resize_img(args.source, (args.width, args.height), args.destination)
    else:
        os.makedirs(args.destination, exist_ok=True)
        rename_raw_image(args.source, args.name)
        # resize
        resize_img(args.source, (args.width, args.height), args.destination) 
            
