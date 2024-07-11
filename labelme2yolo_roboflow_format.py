import os
import shutil
import glob
import subprocess
import argparse
import sys

def labelme2yolo(json_dir, val_size):
    os.chdir("Labelme2YOLO")
    subprocess.run(['python', 'labelme2yolo.py',
                    '--val_size', str(val_size),
                    '--json_dir', json_dir])
    os.chdir("..")
    
def change_folder_format(labelme2yolo_folder, new_folder_path, ):
        
    for task in ['train', 'val']:
        # create new folder
        image_path = f"{new_folder_path}/{task}/images"
        label_path = f"{new_folder_path}/{task}/labels"
        os.makedirs(image_path, exist_ok=True)
        os.makedirs(label_path, exist_ok=True)
        
        # move orginal to new folder
        for image in glob.glob(f"{labelme2yolo_folder}/images/{task}/*"):
            # print(f"Copying image from {image} to {image_path}")
            shutil.copyfile(image, os.path.join(image_path, os.path.basename(image)))
        
        for label in glob.glob(f"{labelme2yolo_folder}/labels/{task}/*"):
            shutil.copyfile(label, os.path.join(label_path, os.path.basename(label)))


    if len(glob.glob(f"{image_path}/*")) != len(glob.glob(f"{label_path}/*")):
        print("images and label is not maching")
          
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--json_dir',type=str,
                        help='Please input the path of the labelme json files.')
    parser.add_argument('--val_size',type=float, nargs='?', default=0.1,
                        help='Please input the validation dataset size, for example 0.1 ')
    parser.add_argument('--output_dir',type=str,
                        help='Please name for the output path. ')
    
    args = parser.parse_args(sys.argv[1:])
    
    
    # change labelme format to YOLO format
    labelme2yolo(json_dir=args.json_dir, val_size=args.val_size)
    # renew folder path to roboflow style
    change_folder_format(labelme2yolo_folder=f"{args.json_dir}/YOLODataset",
                         new_folder_path=args.output_dir)
    
    print("Original number of dataset: ", len(glob.glob(f"{args.json_dir}/*")))
    print("Number of images in YOLO format: ", 
          len(glob.glob(f"{args.output_dir}/train/images/*")) \
        + len(glob.glob(f"{args.output_dir}/val/images/*")) )
    print("Number of labels in YOLO format: ", 
          len(glob.glob(f"{args.output_dir}/train/labels/*")) \
        + len(glob.glob(f"{args.output_dir}/val/labels/*")) )