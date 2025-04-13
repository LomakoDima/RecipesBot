import telebot
from config import TOKEN, DATABASE
from logic import DB_Manager

bot = telebot.TeleBot(TOKEN)
db = DB_Manager(DATABASE)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(msg.chat.id, "Welcome to the Recipe Bot! "
                                  "Use /add to add a recipe, "
                                  "/view to view recipes, and "
                                  "/list to list all recipes."
                                  "/find to find a recipe by title, "
                                  "/delete to delete a recipe.")

@bot.message_handler(commands=['add'])
def add_recipe(msg):
    bot.send_message(msg.chat.id, "Enter the recipe title:")
    bot.register_next_step_handler(msg, get_title)

def get_title(msg):
    title = msg.text
    bot.send_message(msg.chat.id, "Enter the ingredients (comma-separated):")
    bot.register_next_step_handler(msg, get_ingredients, title)


def get_ingredients(msg, title):
    ingredients = msg.text
    bot.send_message(msg.chat.id, "Enter the instructions:")
    bot.register_next_step_handler(msg, get_instructions, title, ingredients)


def get_instructions(msg, title, ingredients):
    instructions = msg.text
    bot.send_message(msg.chat.id, "Enter the category (optional):")
    bot.register_next_step_handler(msg, save_recipe, title, ingredients, instructions)

def save_recipe(msg, title, ingredients, instructions):
    category = msg.text
    request = '''INSERT INTO recipes 
    (title, ingredients, instructions, category) 
    VALUES (?, ?, ?, ?)
    '''
    db._DB_Manager__executemany(request, [(title, ingredients, instructions, category)])
    bot.send_message(msg.chat.id, f"Recipe {title} added successfully!")


@bot.message_handler(commands=['list'])
def list_recipes(msg):
    request = '''SELECT id, title FROM recipes'''
    recipes = db._DB_Manager__select_data(request)
    if recipes:
        message = "\n".join(f"{r[0]}. {r[1]}" for r in recipes)
    else:
        message = "No recipes found."
    bot.send_message(msg.chat.id, message)

bot.polling(non_stop=True)