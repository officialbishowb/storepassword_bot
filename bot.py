import assets.functions as func
import assets.db as db
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os


load_dotenv() # For ENV variables

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
/get <code>‹data_id (optional)›</code> - Get your credentials  
/latest - Get the latest saved credentials
/oldest - Get the oldest saved credentials
/delete <code>‹data_id›</code> - Delete a saved credential
""")
        
    
    
@dp.message_handler(commands=['save','get','latest','oldest','delete'])
async def database_actions(message: types.Message):
    
    if(message.text.startswith("/save")):
        
        credentials_to_save = message.text[6:]
        
        if(credentials_to_save == ""):
            await message.reply("Please send me your credentials in the format /save <code>email:pass</code>!")
        else:
            await message.reply("Saving your credentials...")
            
            # Get service name and credentials to save
            user_input = message.text[5:].split(" ")
            user_input = [value for value in user_input if value != ""]
            service_name = ' '.join([service_name for service_name in user_input if ":" not in service_name])
            email = ''.join([email.split(":")[0] for email in user_input if ":" in email])
            password = ''.join([password.split(":")[1] for password in user_input if ":" in password])
            
            if(db.insert_credentials(message.from_user.id, service_name, email, password)):
                await bot.edit_message_text("<b>Your credentials have been saved!</b>\nType /get to see all of your stored credentials.",message.chat.id,message.message_id+1)
            else:
                await bot.edit_message_text("<b>Something went wrong! Please try again.</b>",message.chat.id,message.message_id+1)
            

    elif(message.text.startswith("/get")):
        return "s"
        
    elif(message.text.startswith("/latest")):
        return "s"
    
    elif(message.text.startswith("/oldest")):
        return "s"
    
    else:
        return "s"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)