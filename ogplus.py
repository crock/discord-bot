import json
import discord
import asyncio
import string
import requests

fp = open('config.json', "r")
config = json.load(fp)
fp.close()

client = discord.Client()

# Commands
TEST_CMD = "!test"
CHECK_CMD = "!check"

def check_steam(name):
	from bs4 import BeautifulSoup
	link = "https://steamcommunity.com/id/%s" % name
	r = requests.get(link)
	page = r.content
	soup = BeautifulSoup(page, "html.parser")
	
	# Available
	match1 = soup.body.findAll(text='The specified profile could not be found.')
	# Taken
	match2 = soup.body.findAll(text='This profile is private.')
	match3 = soup.find('div', attrs={'class': 'profile_header'})
	
	matches = [match1, match2, match3]
	if matches != None:
		if matches[0] != []:
			return True

def check_twitter(name):
	link = "https://api.twitter.com/i/users/username_available.json?username=%s" % name
	r = requests.get(link)
	obj = r.json()
	if obj['valid'] is True:
		return True

async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	
@client.event
async def on_message(message):
	if message.content.startswith(TEST_CMD):
		await client.send_message(message.channel, "testing 123")
	if message.content.startswith(CHECK_CMD):
		name = message.content[len(CHECK_CMD):].strip()
		if check_steam(name):
			await client.send_message(message.channel, "`id/%s` is available on `Steam`" % name)
		else:
			await client.send_message(message.channel, "`id/%s` is taken on `Steam`" % name)
		if check_twitter(name):
			await client.send_message(message.channel, "`%s` is available on `Twitter`" % name)
		else:
			await client.send_message(message.channel, "`%s` is taken on `Twitter`" % name)

		

# @client.event
# async def on_reaction_add(reaction, user):
# 	if reaction.me:
# 		if reaction.custom_emoji:
# 			if reaction.emoji in emojis:
# 				if reaction.emoji.name != "ogplus":
# 						await client.send_message(reaction.message.channel, reaction.emoji.name)

@client.event
async def on_member_join(member):
	msg = "%s has joined the OG+ community!" % member.name
	await client.send_message(client.get_channel(config['join_log_channelID']), msg)

client.run(config['token'])