
# Target Face Tracking

Given a video and the reference image of a person, this code detects all faces and identifies the target person in the clip and tracks them across the video. It also generates clips with the target and faces identified. If there is a change in scene in frames, separate clips are generated. The cropped video clips with just the target face is also generated.

## Sample Input

The `inputs/` folder contains some sample videos and reference images.

## Sample Output

The `outputs/` folder contains the generated output for one of the input videos.

This folder contains two types of video clips:

1. `clipped_videos` - The clips from the original video with a bounding box around all faces - green for target and blue for others.

2. `cropped_videos` - The clips from the original video with the target face cropped.

It also has the `metadata.json` file with details of each clip.

## Source Code
The source code is present in the `src/` folder in `face_tracking.py`.

## Run the code

1. cd into the `HeyGen` directory: `cd HeyGen`

2. Install the requirements: `pip intall -r requirements.txt`

3. Run the script - `python3 src/face_tracking.py --video ./inputs/RebelClips.mov --reference ./inputs/RebelImage.png`

    To change the video and reference image run - `python3 src/face_tracking.py --video <path to video> --reference <path to reference image>`

## Limitations of the approach

1. The `face_recognition` library is used which is not able to detect faces in side profile. For example, when run with the `RossClip6.mov` and `RossImage.png` video and image, it detects only 2-3 faces in a group of 6-7 people seated around a round table.
2. In the `RebelClips.mov` and `RebelImage.png` video and image, the target (the woman) is identified correctly but the other person's (the man's) face is not detected all the time. This is possibly due to the presence of sunglasses on the man.



