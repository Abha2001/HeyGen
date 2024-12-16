
# Target Face Tracking

Given a video and the reference image of a person, this code detects all faces and identifies the target person in the clip and tracks them across the video. It also generates clips with the target and faces identified. If there is a change in scene in frames, separate clips are generated. The cropped video clips with just the target face is also generated.

## Sample Input

The `inputs/` folder contains some sample videos and reference images.

## Sample Output

The `outputs/` folder contains the generated output for one of the input videos.

This folder contains two types of video clips:

1. `clipped_videos` - The clips from the original video with a bounding box around all faces - green for target and blue for others.

2. `cropped_videos` - The clips from the original video with the target face cropped.

It also has the `metadata.json` file with details of each clip. including:
1. The start and end timestamps of each clip in the original video.
2. The filenames of the cropped/clipped video which is saved in the `output/cropped_videos` and `output/clipped_videos` folders respectively.
3. The bounding box coordinates of the target face in each frame of the clip.

## Source Code
The source code is present in the `src/` folder in `face_tracking.py`.

## Dependencies
```
1. click==8.1.7
2. cmake==3.31.2
3. dlib==19.24.6
4. face-recognition==1.3.0
5. face-recognition-models==0.3.0
6. numpy==2.2.0
7. opencv-python==4.10.0.84
8. pillow==11.0.0
```

To install, run - `pip intall -r requirements.txt`


## Run the code

1. cd into the `HeyGen` directory: `cd HeyGen`

2. Install the requirements: `pip intall -r requirements.txt`

3. Run the script - `python3 src/face_tracking.py --video ./inputs/RebelClips.mov --reference ./inputs/RebelImage.png`

    To change the video and reference image run - `python3 src/face_tracking.py --video <path to video> --reference <path to reference image>`

## Limitations of the approach

1. The `face_recognition` library is used which is not able to detect faces in side profile. For example, when run with the `RossClip6.mov` and `RossImage.png` video and image, it detects only 2-3 faces in a group of 6-7 people seated around a round table.
2. In the `RebelClips.mov` and `RebelImage.png` video and image, the target (the woman) is identified correctly but the other person's (the man's) face is not detected all the time. This is possibly due to the presence of sunglasses on the man.
