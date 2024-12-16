from copy import deepcopy
import cv2
import face_recognition
import os
import json
import argparse

def is_scene_change(frame1, frame2, threshold = 0.65):
    hist1 = cv2.calcHist([frame1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([frame2], [0], None, [256], [0, 256])

    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    print(similarity)

    return similarity < threshold

def save_clip_and_cropped(clip_number, frames, bounded_frames, bounding_boxes, output_dir, start_time, frame_count, frame_rate, metadata):
    clip_name = f"clip_{clip_number}.mp4"
    clips_file = os.path.join(output_dir, "clipped_videos", clip_name)
    cropped_file = os.path.join(output_dir, "cropped_videos", clip_name)

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    cropped_out = cv2.VideoWriter(cropped_file, fourcc, 30.0, (width, height))
    clipped_out = cv2.VideoWriter(clips_file, fourcc, 30.0, (width, height))


    for frame, bbox in zip(frames, bounding_boxes):
        top, right, bottom, left = bbox
        top, bottom = top // 2 * 2, bottom // 2 * 2
        left, right = left // 2 * 2, right // 2 * 2
        cropped_frame = frame[top:bottom, left:right]
        resized_frame = cv2.resize(cropped_frame, (width, height))
        cropped_out.write(resized_frame)
    
    for bounded_frame in bounded_frames:
        clipped_out.write(bounded_frame)
    
    cropped_out.release()
    clipped_out.release()

    if len(bounding_boxes) > 0:
        metadata['clips'].append({
            "filename": clip_name,
            "start_time": int(start_time),
            "end_time": int(frame_count/frame_rate),
            "bounding_boxes": bounding_boxes
        })


def process_video(video_path, reference_img_path, output_dir):
    reference_image = face_recognition.load_image_file(reference_img_path)
    reference_image_encoding = face_recognition.face_encodings(reference_image)[0]

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Error: Cannot open video file")
        return

    frame_rate = int(video.get(cv2.CAP_PROP_FPS))
    print("frame rate=", frame_rate)
    metadata = {"clips": []}
    frame_count = 0
    clip_number = 0
    start_time = -1
    current_clip_frames = []
    current_bounded_clip_frames = []
    current_bounding_boxes = []
    prev_frame = None
    ret = True

    # ret, prev_frame = video.read()
    
    while ret:
        ret, frame = video.read()
        if not ret:
            break

        frame_count += 1

       
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        target_location = None

        # cv2.imshow("Frame", frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # if prev_frame is not None:
        #     cv2.imshow("Prev Frame", prev_frame)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
        print("num locations = ", len(face_locations))
        bounded_frame = deepcopy(frame)
        for encoding, location in zip(face_encodings, face_locations):
            match = face_recognition.compare_faces([reference_image_encoding], encoding, tolerance = 0.6)

            top, right, bottom, left = location

            if match[0]:
                target_location = location
                color = (0, 255, 0)
                label = "Target"
            else:
                color = (255, 0, 0) 
                label = "Face"

            cv2.rectangle(bounded_frame, (left, top), (right, bottom), color, 2)
            cv2.putText(bounded_frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if prev_frame is not None and is_scene_change(prev_frame, frame) and current_clip_frames:
            print("saving due to scene change")
            save_clip_and_cropped(clip_number, current_clip_frames, current_bounded_clip_frames, current_bounding_boxes, output_dir, start_time, frame_count, frame_rate, metadata)
            clip_number += 1
            current_clip_frames = []
            current_bounded_clip_frames = []
            current_bounding_boxes = []
            start_time = -1

        if face_locations:
            current_clip_frames.append(frame)
            current_bounded_clip_frames.append(bounded_frame)
            if target_location is not None:
                current_bounding_boxes.append(target_location)
        
            prev_frame = frame  
            if start_time == -1:
                start_time = frame_count / frame_rate

    if current_clip_frames:
        print("saving since end of clip")
        save_clip_and_cropped(clip_number, current_clip_frames, current_bounded_clip_frames, current_bounding_boxes, output_dir, start_time, frame_count, frame_rate, metadata)
    
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, required=True, help="Path to the input video.")
    parser.add_argument("--reference", type=str, required=True, help="Path to the reference image.")

    args = parser.parse_args()

    output_dir = os.getcwd()
    output_dir = os.path.join(output_dir, "output")
    os.makedirs(os.path.join(output_dir, "cropped_videos"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "clipped_videos"), exist_ok=True)
    process_video(args.video, args.reference, output_dir)
