import json
import asyncio
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from typing import Final
from telegram.ext import Application, CommandHandler, MessageHandler, filters , ContextTypes , CallbackQueryHandler

TOKEN: Final = 'TOKEN HERE'  # Replace with your bot's token
BOT_USERNAME: Final = 'Bot Username'  # Replace with your bot's username

JSON_FILE = 'Path/to/your/user_data.json'

#Commands
#async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("Hello there")

def load_user_data():
    try:
        with open(JSON_FILE,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {} # Return an empty dictionary if the file does not exist

# Function to save JSON data
def save_user_data(data):
    with open(JSON_FILE,'w') as file:
        json.dump(data, file, indent = 4)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("you can chat by these sentences: \n Hello There \n Hello \n How are you?")
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom")
    
async def show_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        keyboard = [
            [InlineKeyboardButton("button 1", callback_data='1'),
            InlineKeyboardButton("button 2", callback_data='2')],
         [InlineKeyboardButton("Next page", callback_data='page_2')],
         [InlineKeyboardButton("Free Chat", callback_data='free')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('you are on Page 1: \n Choose an option:', reply_markup=reply_markup)
    
    elif update.callback_query:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("button 1", callback_data='1'),
            InlineKeyboardButton("button 2", callback_data='2')],
         [InlineKeyboardButton("Next page", callback_data='page_2')],
         [InlineKeyboardButton("Free Chat", callback_data='free')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('now you are on Page 1: \n Choose an option:', reply_markup=reply_markup)

async def show_second_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Go to page 1", callback_data='page_1')],
        [InlineKeyboardButton("button 3", callback_data='3')],
        [InlineKeyboardButton("Go to Page 3", callback_data='page_3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text='You are on Page 2:', reply_markup=reply_markup)

async def show_third_buttons(update: Update, context):
    query = update.callback_query
    await query.answer()  # Acknowledge the button click

    keyboard = [
        [InlineKeyboardButton("Back to Page 2", callback_data='page_2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Edit the message to show the new set of buttons
    await query.edit_message_text(text="You are on Page 3:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == '1':
        await query.message.reply_text(text=f"Button {query.data} was clicked")

    elif query.data == '2':
        await query.message.reply_text(text=f"Button {query.data} was clicked")

    elif query.data == 'page_1':
        await show_buttons(update, context)

    elif query.data == 'page_2':
        await show_second_buttons(update, context)

    elif query.data == 'page_3':
        await show_third_buttons(update, context)

    elif query.data == '3':
        await query.message.reply_text(text=f"Button {query.data} was clicked")
    
    elif query.data == 'free':
        await query.edit_message_text(text="Free chat is available.\n You can also use /help for more options.")


#Responses
def handle_response(text: str) -> str :
    processed: str = text.lower()

    if "hello there" in processed:
        return "general kenobi"
    if "hello" in processed:
        return "Hi"
    if "how are you?" in processed:
        return "I'm good thanks"
    return"speak clearly... or if you can't use /help"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    # Load existing data
    user_data = load_user_data()
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    
    # Get user ID and message text
    user_id = str(update.message.from_user.id)
    message_text = update.message.text
    bot_response: str = handle_response(text)
    #bot_text = bot_response
    
    
    # Check if the user already exists in the JSON
    if user_id not in user_data:
        user_data[user_id] = {
            'username': update.message.from_user.username,
            'messages' : [],
            'Bots response' : []
        }

    # Append the user's message to their history
    user_data[user_id]['messages'].append(message_text)
    user_data[user_id]['Bots response'].append(bot_response)

    # Save the updated data
    save_user_data(user_data)
    
    print('Bot:', response)
    await update.message.reply_text(response)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')
    

if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    

    #Commands
    app.add_handler(CommandHandler('start', show_buttons))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    


    #messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_click))

    #Error
    app.add_error_handler(error)

    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)