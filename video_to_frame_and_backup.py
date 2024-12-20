import httpx
import os
import shutil

from prefect import flow, task # Prefect flow and task decorators

import cv2
import numpy as np


# let's make the first part

# local
#   video
#   frame

@task
def backup_frame(source_directory):

    # the source_directory would look like .../<project-number>/frame/<index>/<cam-num>.jpg
    split_source_directory_list = source_directory.split("/")

    directory_list = split_source_directory_list[-4:]

    parent_directory = rf'/mnt/lab51/FS/LAB51/Scan_4D/Projects'

    dest_directory = os.path.join([parent_directory] + directory_list)

    shutil.copy2(source_directory, dest_directory)

@task
def video_to_frame(video_path, save_directory):

    print(video_path)
    video = cv2.VideoCapture(video_path)

    brightness = np.array([])

    frame_num = 0

    while video.isOpened():

        if frame_num > 500:
            break

        ret, frame = video.read()

        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        average_brightness = np.mean(gray_frame)

        brightness = np.append(brightness, average_brightness)

        frame_num += 1

    print(f"{video_path} analyzed finished!")

    video.release()

    max_brightness = np.max(brightness)

    adjusted_brightness = brightness / max_brightness
    adjusted_brightness = np.diff(adjusted_brightness)

    index = np.argmax(adjusted_brightness > 0.2)

    video = cv2.VideoCapture(video_path)

    frame_num = 0
    save_frame_num = 1

    while video.isOpened():

        ret, frame = video.read()

        if not ret:
            break

        if frame_num >= index:

            # make directory if it does not exist
            folder_directory = os.path.join(save_directory, str(save_frame_num+1))
            os.makedirs(folder_directory, exist_ok=True)

            # get camera file name
            file_name_ext = os.path.basename(video_path)
            file_name, ext = os.path.splitext(file_name_ext)

            total_path = os.path.join(folder_directory, f"{file_name}.jpg")

            # print(f"writing {total_path}")
            cv2.imwrite(total_path, frame)
            
            # non blocking
            backup_frame(total_path)

            save_frame_num += 1

            print(f"writing {frame_num} for {file_name}")

        frame_num += 1

    video.release()


@flow(log_prints=True)
def video_to_frame_and_backup(video_directory, dest_directory):

    # non blocking for copyting video
    backup_video(video_directory)

    # slice it into frames
    # video_directory = ...<project-number>/video/<cam-num>.MOV
    # dest_directory = ...<project-number>/frame

    video_directory_list = video_directory.split("/")

    video_to_frame(video_directory, os.path.join(video_directory_list[:-2] + ['frame']))

    # backup the frames
    backup_frame(dest_directory)

# Run the flow
if __name__ == "__main__":
    video_to_frame_and_backup()

