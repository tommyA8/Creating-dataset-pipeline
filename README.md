# Install labelme annotator repo.
Ref. https://github.com/labelmeai/labelme.git

```cli
conda create -n create-dataset python=3.10 labelme -c conda-forge
conda activate create-dataset
conda install pyqt
```

# Install video-cli lib. for hand on with Video
Ref. and useful command https://github.com/wkentaro/video-cli.git

```cli
pip install video-cli
```

# Install Labelme2YOLO

```cli
git clone https://github.com/rooneysh/Labelme2YOLO.git
cd Labelme2YOLO
pip install -r requirements.txt
```

# Install albumentations

```cli
pip install -U albumentations
```

# How to Creat a MRT Dataset

- Convert video to image 

    ```cli
    video-toimg <your_video_path> --per <number_of_frame_you_want_to_skip>

    # example
    video-toimg annotation/cut-video/footage3-cut.mp4 --per 500
    ```

- Pre-process data (Rename and resize image to 640x640)
    
    ```cli
    python data_pipeline.py \
    --source <your_images_folder> \
    --name <rename_here> \ 
    --destination <destination_folder_for_processed_images> \ 
    --width 640 \
    --height 640
    ```

3. Now, you can do annotation

    ```cli
    ls <your_processed_images_path>
    labelme <your_processed_images_path>
    ```

4. convert labelme JSON format to yoloformat 
   
    ```cli
    cd labelme2yolo

    python labelme2yolo.py \
    --json_dir <labeled_images_path> \
    --val_size 0.1
    ```

5. Perform Data Augmentation

    Example of usage of *albumentations*

    https://albumentations.ai/docs/examples/example/

    Augmentation only images

    ```python
    import albumentations as A
    import cv2

    transform = A.Compose([
        A.RandomCrop(width=256, height=256),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
    ])

    image = cv2.imread("/path/to/image.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    transformed = transform(image=image)
    # transform will return a dictionary with a single key image. Value at that key will contain an augmented image.   
    transformed_image = transformed["image"]
    # To augment the next image, you need to call transform again and pass a new image as the image argument:
    another_transformed_image = transform(image=another_image)["image"]
    ```

    ```python
    # another example
    transform = A.Compose([
        A.RandomBrightnessContrast(brightness_limit=1, contrast_limit=1, p=1.0),
    ])
    transformed_image_1 = transform(image=image)['image']
    transformed_image_2 = transform(image=image)['image']
    transformed_image_3 = transform(image=image)['image']
    ```

    Pass an image and bounding boxes to the augmentation pipeline
    
    ```python
    """
    ลูป enumerate image กับ labeled
    อ่าน bounding box จาก txt file แปลงเป็น list แล้วยัดเข้าฟังชันก์
    """
    bboxes = [
        [23, 74, 295, 388, 'dog'],
        [377, 294, 252, 161, 'cat'],
        [333, 421, 49, 49, 'sports ball'],
    ]
    transformed = transform(image=image, bboxes=bboxes)
    transformed_image = transformed['image']
    transformed_bboxes = transformed['bboxes']
    ```

#   C r e a t i n g - d a t a s e t - p i p e l i n e  
 