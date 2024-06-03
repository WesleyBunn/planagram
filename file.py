import sys
import os
import time
import logging
from datetime import datetime
from instabot import Bot
import schedule
import shutil
from requests.exceptions import HTTPError

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    caption = sys.argv[3]
    scheduleTime = sys.argv[4]

    print("Received inputs:")
    print("Username:", username)
    print("Password:", password)
    print("Caption:", caption)
    print("Schedule Time:", scheduleTime)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_insta_uploads():
    insta_path = os.path.join(os.getcwd(), "insta")  # Path to the "insta" directory
    uploads_path = os.path.join(insta_path, "uploads")  # Path to the "uploads" directory inside "insta"

    if os.path.exists(uploads_path):
        try:
            shutil.rmtree(uploads_path)  # Delete the "uploads" directory and all its contents
            logger.info("The 'uploads' directory and its contents have been successfully deleted.")
        except OSError as e:
            logger.error(f"Error deleting 'uploads' directory: {e}")
    else:
        logger.info("'uploads' directory not found inside 'insta'.")

def upload_media(bot, media_path, caption):
    try:
        if media_path.lower().endswith('.mp4'):
            bot.upload_video(media_path, caption=caption)
        else:
            bot.upload_photo(media_path, caption=caption)
        return True
    except HTTPError as e:
        logger.error(f"HTTP Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
    return False

def schedule_post(username, password, uploads_folder, caption, scheduleTime):
    bot = Bot()
    try:
        bot.login(username=username, password=password)
        logger.info("Logged in successfully.")
    except HTTPError as e:
        logger.error(f"HTTP Error: {e}")
        return
    except Exception as e:
        logger.error(f"Error: {e}")
        return

    # Ensure the uploads folder exists
    if not uploads_folder or not os.path.exists(uploads_folder):
        logger.error("Uploads folder not found.")
        return

    # Schedule the post
    schedule_time = datetime.strptime(scheduleTime, "%Y-%m-%d %H:%M:%S")
    logger.info(f"Scheduled post for {schedule_time}")



    # Process each file in the uploads folder
    for file_name in os.listdir(uploads_folder):
        file_path = os.path.join(uploads_folder, file_name)
        if upload_media(bot, file_path, caption):
            os.remove(file_path)
            logger.info(f"Uploaded and deleted: {file_path}")
        else:
            logger.error(f"Failed to upload: {file_path}")

    bot.logout()
    logger.info("Logged out successfully.")

    # Delete the uploads folder after completing the task
    delete_insta_uploads()
    return schedule_time




# Define the path to the "uploads" folder in the current directory
uploads_folder = os.path.join(os.getcwd(), "uploads")

date, times = scheduleTime.split(' ')
time_without_date = times

# Schedule the job function to run at the specified time
schedule.every().day.at(time_without_date).do(schedule_post, username, password, uploads_folder, caption, scheduleTime)

scheduleTime = datetime.strptime(scheduleTime, "%Y-%m-%d %H:%M:%S")
while True:
    # Check if the current time is past the scheduled time
    if datetime.now() >= scheduleTime:
        schedule.run_pending()
    time.sleep(1)


#schedule_post(username, password, uploads_folder, caption, scheduleTime)
