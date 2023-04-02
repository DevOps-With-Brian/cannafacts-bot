from twitchio.ext import commands
import os
import requests
import re
import time


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(
            token=os.getenv("TOKEN"),
            client_id=os.getenv("CLIENT_ID"),
            prefix=os.getenv("BOT_PREFIX"),
            initial_channels=os.getenv("CHANNEL").split(","),
        )

        self.api_url = os.getenv("API_URL")
        print(os.getenv("CHANNEL").split(","))

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
                await ctx.send(
                    f"{os.getenv('BOT_PREFIX')} {command.name} - {help_text}"
                )
            else:
                await ctx.send(f"Command '{command_name}' not found.")
        # Otherwise, list all available commands
        else:
            command_list = ["Available commands:"]
            for command in self.commands.values():
                if command.name != "help":
                    # Get the help text from the command object
                    help_text = getattr(command, "help", "No help text available.")
                    command_list.append(
                        f"{os.getenv('BOT_PREFIX')} {command.name} - {help_text}"
                    )
            # Send the list of available commands to the chat
            await ctx.send("\n".join(command_list))

    @commands.command(name="strain")
    async def strain_command(self, ctx: commands.Context, *, message):
        # Set the help text for the strain command
        self.commands["strain"].help = "Get information about a specific strain."

        await ctx.send("Sure just one sec while I look that up...")
        time.sleep(1)

        # Define a regular expression that matches any non-printable characters or escape sequences
        non_printable_regex = r"[\x00-\x1f\x7f-\xff\u2028\u2029]"

        # Remove any non-printable characters or escape sequences from the input string
        sanitized_message = re.sub(non_printable_regex, "", message)

        # Make api call to get strain information
        strain_name = sanitized_message

        print("Currently being asked about strain: {}".format(strain_name))

        # Make api call to get strain information
        url = self.api_url + "/strains/" + strain_name
        response = requests.get(url)
        data = response.json()

        if "detail" in data:
            # Respond to the cannafacts strain command
            await ctx.send(data["detail"])
        elif data['name']:
            strain_name = data["name"]
            thc_level = data["thc_level"]
            strain_type = data["strain_type"]
            flavors = data["flavors"]
            feelings = data["feelings"]
            helps_with = data["helps_with"]

            # Write up our own response from the data
            result = "{0} is a {1} strain with a thc level of {2}. It has the following flavors: {3}.  Some known feelings are: {4}.  It has been known to help with: {5}".format(
                strain_name, strain_type, thc_level, flavors, feelings, helps_with
            )
            # Respond to the cannafacts strain command
            await ctx.send(result)
        else:
            print("Not sure what hits here...")

    @commands.command(name="strain_type")
    async def strain_type_command(self, ctx: commands.Context, *, message):
        # Set the help text for the strain command
        self.commands[
            "strain_type"
        ].help = "Get the type of strain for a specific strain."

        # Make api call to get strain information
        strain_name = message
        url = self.api_url + "/strains/" + strain_name
        response = requests.get(url)
        data = response.json()


        if "detail" in data:
            # Respond to the cannafacts strain_type command
            await ctx.send(data["detail"])
        elif "strain_type" in data:
            # Respond to the cannafacts strain_type command
            await ctx.send(data["strain_type"])
        else:
            print("Not sure what hits here...")

    @commands.command(name="thc")
    async def thc_level_command(self, ctx: commands.Context, *, message):
        # Set the help text for the strain command
        self.commands["thc"].help = "Get the thc percentage for a given strain name."

        # Make api call to get strain thc level
        strain_name = message
        url = self.api_url + "/strains/" + strain_name
        response = requests.get(url)
        data = response.json()

        if "detail" in data:
            # Respond to the cannafacts thc command
            await ctx.send(data["detail"])
        elif "thc_level" in data:
            # Respond to the cannafacts thc command
            print(data["thc_level"])
            await ctx.send(
                "Strain: {0} has a thc level of {1}".format(
                    strain_name, data["thc_level"]
                )
            )
        else:
            print("Not sure what hits here...")

    @commands.command(name="flavors")
    async def flavors_command(self, ctx: commands.Context, *, message):
        # Set the help text for the strain command
        self.commands[
            "flavors"
        ].help = "Get the flavor information for a given strain name."

        # Make api call to get strain flavors info
        strain_name = message
        url = self.api_url + "/strains/" + strain_name
        response = requests.get(url)
        data = response.json()

        if "detail" in data:
            # Respond to the cannafacts flavors command when not found
            await ctx.send(data["detail"])
        elif "flavors" in data:
            # Respond to the cannafacts flavors command
            print(data["flavors"])
            await ctx.send(
                "Strain: {0} has the follow flavors {1}".format(
                    strain_name, data["flavors"]
                )
            )
        else:
            print("Not sure what hits here...")

    @commands.command(name="helps_with")
    async def helps_with_command(self, ctx: commands.Context, *, message):
        # Set the help text for the helps_with command
        self.commands[
            "helps_with"
        ].help = "Get the things it can help with/treat for a given strain name."

        # Make api call to get strain helps_with info
        strain_name = message
        url = self.api_url + "/strains/" + strain_name
        response = requests.get(url)
        data = response.json()

        if "detail" in data:
            # Respond to the cannafacts helps_with command when not found
            await ctx.send(data["detail"])
        elif "helps_with" in data:
            # Respond to the cannafacts helps_with command
            print(data["helps_with"])
            await ctx.send(
                "Strain: {0} has the following things it can help with/alleviate {1}".format(
                    strain_name, data["helps_with"]
                )
            )
        else:
            print("Not sure what hits here...")

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # If a command is not found, send help message to chat
            await ctx.send("You can run !cannafacts help to get a list of commands.")


bot = Bot()
bot.run()
