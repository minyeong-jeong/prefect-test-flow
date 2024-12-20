import httpx
import os

from prefect import flow, task # Prefect flow and task decorators


# let's make the first part

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

            save_frame_num += 1

            print(f"writing {frame_num} for {file_name}")

        frame_num += 1

    video.release()

def backup_frame():


# let's make the second part

def frame_to_obj():

def gcp_to_wrap_coords():


@flow(log_prints=True)
def write_text_file():
    # Define the path for the file
    file_path = rf'/mnt/c/Users/user/Desktop/example.txt'

    # Content to write into the file
    content = "Hello, this is a simple text file created by Python!"

    try:
        # Write the content to the file
        with open(file_path, 'w') as file:
            file.write(content)
        
        print(f"File successfully created at: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the flow
if __name__ == "__main__":
    write_text_file()

