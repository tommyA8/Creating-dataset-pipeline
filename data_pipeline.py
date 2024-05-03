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
        # source = raw_video/footage1
        new_folder = source + "/" + "rename_" + name
        
        for filename in (os.listdir(source)):
            if not filename.endswith(".jpg"):
                continue
            re_name = f"{name}-{filename}"
            print(filename, "=>", re_name)
            
            src =f"{source}/{filename}"  # foldername/filename, if .py file is outside folder

            try:
                os.mkdir(new_folder) # raw_video/footage1/rename_footage1
                # print(error)        
                dst =f"{new_folder}/{re_name}" # raw_video/footage1/rename_footage1/footage1-00000.jpg
                # rename() function will
                # rename all the files
                shutil.copy(src, dst)
                # os.rename(src, dst)
            except OSError as error:
                # print(error)        
                dst =f"{new_folder}/{re_name}" # raw_video/footage1/rename_footage1/footage1-00000.jpg
                # rename() function will
                # rename all the files
                shutil.copy(src, dst)
                # os.rename(src, dst)
        
        return new_folder

    except NameError:
        print("Please put the folder path")
                      
def resize_img(source, img_size, dst_folder):
    try: 
        for filename in os.listdir(source):
            if not filename.endswith(".jpg"):
                continue
            # file_path = f"{source}/{filename}"
            image = f"{source}/{filename}"
            # print(image)
            im = cv2.imread(image)
            resized = cv2.resize(im, img_size) # (width, height)
            output_name = filename[:-4]+"_resized"+".jpg"
            
            dst = f"{dst_folder}/{output_name}"
            cv2.imwrite(dst, resized)

    except NameError:
        # im = cv2.imread(source)
        # resized = cv2.resize(im, img_size)
        # output_name = source[:-4]+"_resized"+".jpg"
        # cv2.imwrite(output_name, resized)
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
                        default="pre-processed_images",#"dataset/resized_raw_images",
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

    
    if args.destination != "pre-processed_images":
        # rename
        rename_path = rename_raw_image(args.source, args.name)
        # resize
        resize_img(rename_path, (args.width, args.height), args.destination)
    else:
        try:
            os.mkdir(args.destination)
            rename_path = rename_raw_image(args.source, args.name)
            # resize
            resize_img(rename_path, (args.width, args.height), args.destination) 
            
        except OSError as error:
            print(error) 
            rename_path = rename_raw_image(args.source, args.name)
            # resize
            resize_img(rename_path, (args.width, args.height), args.destination)
        
