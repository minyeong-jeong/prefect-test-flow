import httpx
import os

from prefect import flow, task # Prefect flow and task decorators

# let's make the first part

def video_to_frame():

def backup_video():

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

