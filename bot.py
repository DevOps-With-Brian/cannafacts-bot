from twitchio.ext import commands
import os
import requests


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(
            token=os.getenv("TOKEN"),
            client_id=os.getenv("CLIENT_ID"),
            prefix=os.getenv("BOT_PREFIX"),
            initial_channels=[os.getenv("CHANNEL")],
        )

        self.api_url = os.getenv("API_URL")

        # Set the default help text
        self.default_help = f"Usage: {os.getenv('BOT_PREFIX')} help [command]"
        # Set the help text for the strain command
        self.commands["strain"].help = "Get information about a specific strain."


    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        # Ignore messages sent by the bot
        if message.echo:
            return

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message) 


    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context, *args):
        # If there are arguments, assume they are requesting help for a specific command
        if args:
            command_name = args[0].lower()
            command = self.get_command(command_name)
            if command:
                # Get the help text for the command
                help_text = getattr(command, "help", "No help text available.")
                await ctx.send(f"{os.getenv('BOT_PREFIX')} {command.name} - {help_text}")
            else:
                await ctx.send(f"Command '{command_name}' not found.")
        # Otherwise, list all available commands
        else:
            command_list = ["Available commands:"]
            for command in self.commands.values():
                if command.name != "help":
                    # Get the help text from the command object
                    help_text = getattr(command, "help", "No help text available.")
                    command_list.append(f"{os.getenv('BOT_PREFIX')} {command.name} - {help_text}")
            # Send the list of available commands to the chat
            await ctx.send("\n".join(command_list))


    @commands.command(name="strain")
    async def strain_command(self, ctx: commands.Context, *, message):
        # Set the help text for the strain command
        self.commands["strain"].help = "Get information about a specific strain."

        # Make api call to get strain information
        strain_name = message
        url =  self.api_url + "/strains/" + strain_name
        print(url)
        response = requests.get(url)
        data = response.json()
        print(data)

        if 'detail' in data:
            print("Made it to line 77... {}".format(data['detail']))
            # Respond to the cannafacts strain command
            await ctx.send(data['detail'])
        elif 'description' in data:
            print("Made it to line 81... {}".format(data['description']))
            # Respond to the cannafacts strain command
            await ctx.send(data['description'])
        else:
            print("Not sure what hits here...")

    
    @commands.command(name="strain_type")
    async def strain_type_command(self, ctx: commands.Context, *, message):
        # Set the help text for the strain command
        self.commands["strain_type"].help = "Get the type of strain for a specific strain."

        # Make api call to get strain information
        strain_name = message
        url =  self.api_url + "/strains/" + strain_name
        print(url)
        response = requests.get(url)
        data = response.json()
        print(data)

        if 'detail' in data:
            print("Made it to line 77... {}".format(data['detail']))
            # Respond to the cannafacts strain_type command
            await ctx.send(data['detail'])
        elif 'strain_type' in data:
            # Respond to the cannafacts strain_type command
            await ctx.send(data['strain_type'])
        else:
            print("Not sure what hits here...")

       

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # If a command is not found, send help message to chat
            await ctx.send("You can run !cannafacts help to get a list of commands.")


bot = Bot()
bot.run()
