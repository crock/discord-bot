import json
import discord
import asyncio
import random
import string
import requests

fp = open('config.json', "r")
config = json.load(fp)
fp.close()

client = discord.Client()

# Commands
TEST_CMD = "!test"
CHECK_CMD = "!check"

def generate_pw(size=16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

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

def check_instagram(name):
	url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
	s = requests.Session()
	r = s.get(url)
	cookie = r.cookies['csrftoken']

	headers = {
        "referer":"https://www.instagram.com",
        "x-csrftoken": cookie
    }

	payload = {
		"email":"no-reply@og.plus",
		"username": name,
		"password": generate_pw(),
		"first_name": name
    }

	response = s.post(url, data=payload, headers=headers, cookies=cookie)
	obj = response.json()
	if obj['dryrun_passed'] is True:
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
		name = message.content[len(CHECK_CMD):].strip().replace(' ', '')
		if check_steam(name):
			msg = "id/%s is available on Steam" % name
			await client.send_message(message.channel, embed=msg)
		else:
			msg = "id/%s is taken on Steam" % name
			await client.send_message(message.channel, embed=msg)
		if check_twitter(name):
			msg = "%s is available on Twitter" % name
			await client.send_message(message.channel, embed=msg)
		else:
			msg = "%s is taken on Twitter" % name
			await client.send_message(message.channel, embed=msg)
		if check_instagram(name):
			msg = "%s is available on Instagram" % name
			await client.send_message(message.channel, embed=msg)
		else:
			msg = "%s is taken on Instagram" % name
			await client.send_message(message.channel, embed=msg)

# @client.event
# async def on_reaction_add(reaction, user):
# 	if reaction.me:
# 		if reaction.custom_emoji:
# 			if reaction.emoji in emojis:
# 				if reaction.emoji.name != "ogplus":
# 						await client.send_message(reaction.message.channel, reaction.emoji.name)

client.run(config['token'])