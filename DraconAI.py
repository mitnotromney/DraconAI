# Import the required modules
import discord
import openai
from discord.ext import commands 
from dracodb import get_player_info, get_character_info, get_inventory_info  # Import the functions


openai.api_key = 'See Tim'

# Create a Discord client instance and set the command prefix
intents = discord.Intents.all()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# Set the confirmation message when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
# Set the commands for your bot
@bot.command()
async def greet(ctx):
    response = 'Hello, I am your discord bot'
    await ctx.send(response)

@bot.command()
async def createcharacter(ctx, *, character_details: str):
    try:
        # Basic parsing of character details
        # This example expects the format "Name, Class, Level"
        details = character_details.split(',')
        if len(details) != 3:
            await ctx.send("Please provide character details in the format: Name, Class, Level.")
            return

        name, char_class, level = [detail.strip() for detail in details]
        
        # Convert level to an integer
        try:
            level = int(level)
        except ValueError:
            await ctx.send("Level must be a number.")
            return
        
        # Generate character and inventory IDs (simplified approach)
        character_id = f"char_{len(dracodb) + 1}"
        inventory_id = f"inv_{len(dracodb) + 1}"
        
        # Check if this user already has a character, update if yes, or create a new entry if no
        user_id = str(ctx.author.id)
        player_info = get_player_info(user_id)
        
        if player_info:
            # Update existing character (simple approach, consider more complex logic for a real application)
            dracodb[player_info["character_id"]] = {'name': name, 'level': level, 'class': char_class, 'inventory_id': player_info["character_id"].replace("char_", "inv_")}
            await ctx.send(f"Character updated: {name} the {char_class}, Level {level}.")
        else:
            # Create new entries for the character and a default inventory
            dracodb[user_id] = {'character_id': character_id}
            dracodb[character_id] = {'name': name, 'level': level, 'class': char_class, 'inventory_id': inventory_id}
            dracodb[inventory_id] = ['starter pack']  # Default inventory, customize as needed
            
            await ctx.send(f"Character created: {name} the {char_class}, Level {level}.")
        
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command()
async def ask(ctx, *, question: str):
    try:
        user_id = str(ctx.author.id)

        player_info = get_player_info(user_id)
        if not player_info:
            await ctx.send("Player information not found.")
            return  # Exit the function if player_info is None

        character_info = get_character_info(player_info.get("character_id"))
        if not character_info:
            await ctx.send("Character information not found.")
            return  # Exit the function if character_info is None

        inventory_info = get_inventory_info(character_info.get("inventory_id"))
        if inventory_info is None:  # Assuming get_inventory_info returns None for not found
            inventory_info = "no items"  # Default message if inventory is empty or not found

        dnd_prompt = f"{character_info['name']} is a level {character_info['level']} {character_info['class']} with {inventory_info}. {question}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Dungeon Master assistant."},
                {"role": "user", "content": dnd_prompt},
            ]
        )
        
        answer = response["choices"][0]["message"]["content"]
        await ctx.send(answer)
    except Exception as e:
        print(f"Error fetching response from OpenAI or querying the database: {e}")
        await ctx.send("Sorry, I encountered an issue while processing your request.")



# Retrieve token from the .env file
bot.run('TOKEN')
