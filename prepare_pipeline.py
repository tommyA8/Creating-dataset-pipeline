import subprocess
import os
    
def pre_process_pipe(raw_video_stuff_path, width:int=640, height:int=640, number_to_skip:int=500):
    for video in os.listdir(raw_video_stuff_path):
        subprocess.call(['video-toimg', f"{raw_video_stuff_path}/{video}", '--per', str(number_to_skip)], shell=True)
        
        print(f'Number of images from {video}: ', len(os.listdir(f"{raw_video_stuff_path}/{video[0:-4]}")))
        
        subprocess.run(['python', 
                        'data_pipeline.py', 
                        '--source', f"raw_video/{video[0:-4]}",# clip .mp4 out
                        '--name', str(video[0:-4]),
                        '--width', str(width),
                        '--height', str(height)
                        ])
    
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Please put the folder path")
    
    parser.add_argument("--source",
                        type=str,
                        help="Source. Path to the folder of images")
    
    parser.add_argument("--per",
                        type=int,
                        help="Number of frame that want to skip in the video")
        
    parser.add_argument("--width",
                        type=int,
                        default=640,
                        help="example --width 640")
    
    parser.add_argument("--height",
                        type=int,
                        default=640,
                        help="example --height 640")
    
    args = parser.parse_args()
    
    pre_process_pipe(args.source, 
                     args.per,
                     args.width,
                     args.height
                     )