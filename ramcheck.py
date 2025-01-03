from instagrapi import Client
import os
import pickle
import psutil
import time
import threading

# Path to store cookies
COOKIES_PATH = 'insta_cookies.pkl'


# Login to Instagram
def login_instagram(username, password):
    cl = Client()

    # Load cookies if they exist
    if os.path.exists(COOKIES_PATH):
        try:
            cl.load_settings(COOKIES_PATH)
            cl.login(username, password)  # Verify the login using the saved cookies
            print("Loaded cookies successfully.")
        except Exception as e:
            print("Error loading cookies, logging in again:", e)
            cl.login(username, password)  # If cookies are invalid, log in normally
    else:
        cl.login(username, password)

    # Save cookies after successful login
    cl.dump_settings(COOKIES_PATH)
    return cl


# Like posts from a given username
def like_posts_from_user(client, username, post_count=5):
    try:
        user_id = client.user_id_from_username(username)
        posts = client.user_medias(user_id, post_count)
        for post in posts:
            client.media_like(post.id)
            print(f"Liked post: {post.caption_text}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to check and display real-time CPU and RAM usage
def check_system_usage():
    process = psutil.Process(os.getpid())  # Get current process ID
    while True:
        # Get CPU usage as the percentage of time the process is using the CPU
        cpu_times = process.cpu_times()
        cpu_usage = cpu_times.user + cpu_times.system  # CPU time in seconds

        # Get memory usage in bytes and convert it to MB
        memory_info = process.memory_info()
        ram_usage = memory_info.rss / (1024 * 1024)  # Convert to MB

        # Print current usage
        print(f"\nCPU Usage: {cpu_usage:.2f} seconds")
        print(f"RAM Usage: {ram_usage:.2f} MB")

        time.sleep(1)  # Update every second


# Function to monitor system usage in a separate thread
def start_system_monitor():
    monitor_thread = threading.Thread(target=check_system_usage, daemon=True)
    monitor_thread.start()


if __name__ == "__main__":
    # Replace with your Instagram credentials
    IG_USERNAME = "funwithnikhi72"
    IG_PASSWORD = "wecanshape@98"
    TARGET_USERNAME = "readers.wave"  # Replace with the username whose posts you want to like

    # Start monitoring system usage
    start_system_monitor()

    try:
        client = login_instagram(IG_USERNAME, IG_PASSWORD)
        like_posts_from_user(client, TARGET_USERNAME, post_count=5)
    except Exception as e:
        print(f"Failed to login or like posts: {e}")
