from config import discord
from discord.ext import commands

class HelpEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
        self.set_footer(text=text)
        self.color = discord.Color.blurple()

class Help(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        '''triggers when a `!help` is called'''
        ctx = self.context
        #create an embed
        createdEmbed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        createdEmbed.set_thumbnail(url=f"{ctx.me.display_avatar}")

        for cog, commands in mapping.items():#mapping is a dictionnary
            filtered = await self.filter_commands(commands) #filter the commands the user can't use
            command_signatures = [self.get_command_signature(cmd).split(' ', 1)[0] for cmd in filtered]
        for cmd in range(len(command_signatures)):
            createdEmbed.add_field(name="{}".format(command_signatures[cmd]), value=f"{commands[cmd].help}", inline=False)
        dest_channel = self.get_destination()
        await dest_channel.send(embed=createdEmbed)

    async def send_command_help(self, command):
        '''triggers when !help [command] is invoked'''
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Description", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Alias", value=", ".join(command.aliases), inline=False)
        dest_channel = self.get_destination()
        await dest_channel.send(embed=embed)

    '''
    HelpCommand.send_error_message is called when an error occur.
    Error is a string that will contain the error message.
    All we have to do is to display the message.

    We can also use a local error handler. But first, we need to raise the errors manually in send_bot_help
    and declare a function named on_help_command_error to handle this particular error as follows:
        https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96
    '''
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)