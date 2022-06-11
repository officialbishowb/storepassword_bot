from pickle import TRUE
from site import USER_BASE
from tkinter import N
import assets.functions as func
import assets.db as db
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import time


load_dotenv() # For ENV variables

# GET ADMIN IDS
USER_ADMIN = os.getenv('ADMIN_IDS')
USER_ADMIN = [id for id in USER_ADMIN if id != ""]

API_TOKEN = os.getenv('BOT_TOKEN')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN,parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start', 'help','cmds'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    if message.text.startswith('/start'):
        
        if(not db.master_key_exist(message.from_user.id)):
            key = func.generate_key()
            db.save_master_password(message.from_user.id, key)
            
        await message.reply(f"""
Hey  @<b>{message.from_user.username}</b>, \nI'm a bot that can help you save your account credentials.
                        
Just send me your credentials in the format <code>service name</code> and <code>email:pass</code> and I'll save them for you.
Example: <code>/save gmail testes@gmail.com:mypassword</code>

For other commands, just send me /cmds.
                        """)
        
    elif(message.text.startswith('/help')):
        await message.reply(f"""
Hey @<b>{message.from_user.username}</b>,
Please contact the owner @beanonymousofficial for any help.
                            """)
    
    else:
        await message.reply(f"""
All available commands:

/save <code>‹service name› ‹email:pass›</code> - Save your credentials
/get - Get all saved credentials  
/latest - Get the latest saved credentials
/oldest - Get the oldest saved credentials
/delete <code>‹number› or '<code>all</code>' </code> - Delete (a) saved credential(s)
""")
        
    
################################ USER + ADMIN COMMANDS ################################
@dp.message_handler(commands=['save','get','latest','oldest','delete'])
async def database_actions(message: types.Message):
    
    
    ## Main START ##
    if(message.text.startswith("/save")):
        
        credentials_to_save = message.text[6:]
        
        if(credentials_to_save == ""):
            await message.reply("Please send me your credentials in the format /save <code>email:pass</code>!")
        else:
            await message.reply("Saving your credentials...")
            time.sleep(1)
            
            # Get service name and credentials to save
            user_input = message.text[5:].split(" ")
            user_input = [value for value in user_input if value != ""]
            service_name = ' '.join([service_name for service_name in user_input if ":" not in service_name])
            email = ''.join([email.split(":")[0] for email in user_input if ":" in email])
            password = bytes(''.join([password.split(":")[1] for password in user_input if ":" in password]), 'utf-8') # Convert to bytes
            password = func.encrypt(password,db.get_master_key(message.from_user.id))
            
            ## Save the data in the database
            if(db.insert_credentials(message.from_user.id, service_name, email, password)):
                await bot.edit_message_text("<b>Your credentials have been saved!</b>\nType /get to see all of your stored credentials.",message.chat.id,message.message_id+1)
            else:
                await bot.edit_message_text("<b>Something went wrong! Please try again.</b>",message.chat.id,message.message_id+1)
            
            
    ## /get COMMAND ##
    elif(message.text.startswith("/get")):
        all_datas = db.get_credentials(message.from_user.id)
        if (not all_datas):
            await message.reply("<b>No credentials found!</b>")
        else:
            output = "<b>Your saved credentials:</b>\n"
            for i in range(len(all_datas)):
                service_name = all_datas[i][0]
                email = all_datas[i][1]
                password = bytes(func.decrypt(all_datas[i][2],db.get_master_key(message.from_user.id))).decode('utf-8') # Get the  decrypted password
                output += f"[<code>{i+1}</code>]: <code>{service_name}</code> - <code>{email}</code>:<code>{password}</code>\n"
            await message.reply(output)
    
    
    ## /latest COMMAND ##
    elif(message.text.startswith("/latest")):
        latest = db.get_credential(message.from_user.id,ASC=False)
        if (not latest):
            await message.reply("<b>No credentials found!</b>")
        else:
            output = "<b>Your latest saved credentials:</b>\n"
            password = bytes(func.decrypt(latest[2],db.get_master_key(message.from_user.id))).decode('utf-8') # Get the  decrypted password
            output += f"[<code>1</code>]: <code>{latest[0]}</code> - <code>{latest[1]}</code>:<code>{password}</code>\n"
            await message.reply(output)
    
    
    ## /oldest COMMAND ##
    elif(message.text.startswith("/oldest")):
        oldest = db.get_credential(message.from_user.id,ASC=True)
        if (not oldest):
            await message.reply("<b>No credentials found!</b>")
        else:
            output = "<b>Your oldest saved credentials:</b>\n"
            password = bytes(func.decrypt(oldest[2],db.get_master_key(message.from_user.id))).decode('utf-8') # Get the  decrypted password
            output += f"[<code>1</code>]: <code>{oldest[0]}</code> - <code>{oldest[1]}</code>:<code>{password}</code>\n"
            await message.reply(output)
    
    
    ## /delete COMMAND ##
    else:
        get_user_choice = message.text[8:].replace(" ","")
        
        try:
            get_user_choice = int(get_user_choice)
        except:
            pass
        
        if(get_user_choice == ""):
            await message.reply("<b>I could delete all your credentials. But I won't but please give me a choice (<code>number</code>(do /get) or '<code>all</code>') </b>")
        else:
            if(db.delete_credentials(message.from_user.id,get_user_choice)):
                await message.reply("<b>Your credential(s) has(have) been deleted!</b>\nType /get to your updated credentials.")
                
                
    
################################ ADMIN COMMANDS ################################
@dp.message_handler(commands=['getlogs','clearlogs'])
def admin_msg_handler(message: types.Message):
    
    if(message.text.startswith("/getlogs")):
      
    else:
        
    
    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)