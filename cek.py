import requests
import json
import time
from datetime import datetime

# Global variable to store previous player count
previous_player_count = None

# Function to get the player count from the website
def get_player_count():
    url = "https://growtopiagame.com/detail/"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()  # Parse the JSON response
            player_count = data.get("online_user")  # Extract the player count
            if player_count is not None:
                return int(player_count)  # Convert to integer
            else:
                print("Could not find the player count in the JSON response.")
                return None
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return None
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None

# Function to send a message to the Discord webhook
def send_to_discord(message):
    webhook_url = "https://discord.com/api/webhooks/1266895866812432404/_UiUM48K_YE4MmpfrGDrEqgI3h6_CZe4Ymas7SzgVS83k6A9bGZr4E8cvJ-KqOFNMrJE" # Replace with your Discord webhook URL
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code}")

# Main loop to periodically check the player count and send to Discord
while True:
    player_count = get_player_count()
    if player_count is not None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if previous_player_count is not None:
            difference = player_count - previous_player_count
            print(f"Player count: {player_count}, Previous count: {previous_player_count}, Difference: {difference}, Time: {current_time}")  # Debug print
            
            if difference > 0:
                if difference > 15000:
                    change_message = f"{current_time} | There are currently  **{player_count}** online players! |  [__**+{difference}, server is up !**__ @everyone]"
                else:
                    change_message = f"{current_time} | There are currently **{player_count}** online players! | [__**+{difference}**__]"
            elif difference < 0:
                if difference < -1500:
                    change_message = f"{current_time} | There are currently **{player_count}** online players! | [__**{difference}, probably a banwave!**__ @everyone]"
                else:
                    change_message = f"{current_time} | There are currently **{player_count}** online players! | [__**{difference}**__]"
            else:
                change_message = f"{current_time} | There are currently **{player_count}** online players! |  @everyone"
            
            print(change_message)
            send_to_discord(change_message)
        
        # Update previous player count
        previous_player_count = player_count
    else:
        print("Failed to retrieve player count.")
    
    time.sleep(60)
