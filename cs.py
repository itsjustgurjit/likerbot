from instagrapi import Client
import os
import psutil
import time
import threading
import random

# Constants
COOKIES_PATH = 'insta_cookies.pkl'
HASHTAGS = [
    "books","book","quote","lesson","student"
]

COMMENTS = [
    "Great shot! 📸",
    "Amazing! ✨",
    "Love this! 🙌",
    "Wonderful capture 😊",
    "Beautiful moment ❤️",
    "Fantastic! 👏",
    "This is incredible! 🌟"
]

def login_instagram(username, password):
    cl = Client()
    if os.path.exists(COOKIES_PATH):
        try:
            cl.load_settings(COOKIES_PATH)
            cl.login(username, password)
            print("Loaded cookies successfully.")
        except Exception as e:
            print("Error loading cookies, logging in again:", e)
            cl.login(username, password)
    else:
        cl.login(username, password)
    cl.dump_settings(COOKIES_PATH)
    print("Logged in successfully.")
    return cl

def check_system_usage():
    process = psutil.Process(os.getpid())
    while True:
        cpu_times = process.cpu_times()
        cpu_usage = cpu_times.user + cpu_times.system
        memory_info = process.memory_info()
        ram_usage = memory_info.rss / (1024 * 1024)
        print(f"\nCPU Usage: {cpu_usage:.2f} seconds")
        print(f"RAM Usage: {ram_usage:.2f} MB")
        time.sleep(60)

def start_system_monitor():
    monitor_thread = threading.Thread(target=check_system_usage, daemon=True)
    monitor_thread.start()

def view_post():
    time.sleep(random.uniform(2, 5))  # Simulate viewing time

def engage_with_hashtag(client, hashtag, post_count):
    try:
        print(f"\nFetching posts for #{hashtag}")
        medias = client.hashtag_medias_top(hashtag, amount=25)  # Fetch fewer posts
        print(f"Fetched {len(medias)} posts for #{hashtag}")

        if not medias:
            print(f"No posts found for #{hashtag}")
            return 0

        selected_posts = random.sample(medias, min(post_count, len(medias)))
        engagement_count = 0

        for post in selected_posts:
            try:
                time.sleep(random.uniform(3, 10))  # Random sleep before engagement

                # Simulate viewing the post
                view_post()

                action_choice = random.random()
                if action_choice < 0.7:  # 70% chance to like
                    client.media_like(post.id)
                    print(f"Liked post from #{hashtag}")
                    engagement_count += 1
                elif action_choice < 0.9:  # 20% chance to comment
                    comment = random.choice(COMMENTS)
                    client.media_comment(post.id, comment)
                    print(f"Commented: {comment}")
                    engagement_count += 1
                else:
                    print(f"Skipped post (ID: {post.id}) without engagement.")

            except Exception as e:
                print(f"Error engaging with post (ID: {post.id}): {e}")
                continue

        return engagement_count

    except Exception as e:
        print(f"Error processing hashtag {hashtag}: {e}")
        return 0

def run_engagement_cycle(client):
    posts_to_engage = random.randint(6, 12)  # Increase range for engagement
    hashtag = random.choice(HASHTAGS)

    print(f"\n=== Starting New Engagement Cycle ===")
    print(f"Target: {posts_to_engage} posts from #{hashtag}")

    engaged_posts = engage_with_hashtag(client, hashtag, posts_to_engage)
    print(f"Successfully engaged with {engaged_posts} posts")

    return engaged_posts

def main_loop():
    IG_USERNAME = "your_username"  # Replace with your Instagram username
    IG_PASSWORD = "your_password"  # Replace with your Instagram password

    start_system_monitor()

    try:
        client = login_instagram(IG_USERNAME, IG_PASSWORD)

        while True:
            cycle_count = random.randint(8, 21)
            print(f"\n=== Starting New Major Cycle ({cycle_count} sub-cycles) ===")

            for i in range(cycle_count):
                print(f"\nSub-cycle {i + 1}/{cycle_count}")
                run_engagement_cycle(client)

                if i < cycle_count - 1:
                    sleep_minutes = random.uniform(13, 54)
                    print(f"\nSleeping for {sleep_minutes:.2f} minutes...")
                    time.sleep(sleep_minutes * 60)

            sleep_hours = random.uniform(8, 13)
            print(f"\n=== Completed Major Cycle ===")
            print(f"Taking a long rest for {sleep_hours:.2f} hours...")
            time.sleep(sleep_hours * 3600)

    except Exception as e:
        print(f"Critical error: {e}")
        time.sleep(300)
        main_loop()

if __name__ == "__main__":
    main_loop()