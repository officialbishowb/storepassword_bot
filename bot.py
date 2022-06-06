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
                        
Just send me your credentials in the format <code>email:pass</code> and I'll save them for you.

For other commands, just send me /cmds.
                        """)
        
    else:
        await message.reply(f"""
Hey @<b>{message.from_user.username}</b>,
Please contact the owner @beanonymousofficial for any help.
                            """)
        
    
    
@dp.message_handler(commands=['save','get','latest','oldest','delete'])
async def database_actions(message: types.Message):
    
    if(message.text.startswith("/save")):
        
        credentials_to_save = message.text[6:]
        
        if(credentials_to_save == ""):
            await message.reply("Please send me your credentials in the format /save <code>email:pass</code>!")
        else:
            await message.reply("Saving your credentials...")
            email = credentials_to_save.split(":")[0]
            password = credentials_to_save.split(":")[1]
            if(db.insert_credentials(message.from_user.id, email, password)):
                await message.edit_text("<b>Your credentials have been saved!</b>\nType /get to see all of your stored credentials.")
            else:
                await message.edit_text("Something went wrong! Please try again.")
            
            
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