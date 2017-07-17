# Thorium: a reaction-logging bot for discord
=============================================
## To use the bot once it's running:
	Type 'thorium help' into a channel it can see.
	React to a message with one of its designated reactions, and hope other people will.
	The purpose of this is for organization; users can react to particularly useful/topical messages, and other users can see these logs and read the backlog if the topic of conversation sounded interesting. Alternately, users can react to funny messages and use this as a single-server content-aggregator, if they really want to. 
## What the bot will do:
	The bot will keep a cache of messages sent since it started running. When one of them gets more than the threshold number of a certain kind of reaction, it will post about it in the designated channel.
	The emoji it watches and the threshold number can be changed via text commands. The roles which are allowed to give these commands can be changed, unless they are listed in obey_forever_roles.
## To create a new, unaffiliated-with-me instance:
	Git clone or checkout or whatever to get all these files. 
	Navigate to that folder and run 'npm install'.
	Go to https://discordapp.com/developers/applications/me and create a new app. 
	Give it a name and a description, then save changes and create a new bot user. Copy down your Client ID and your Bot's token.
	In the following url, https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID&scope=bot&permissions=0 insert your client id, then go there and add the bot to your private test server.
	Rename auth.thorium.TEMPLATE.json to auth.thorium.json. Fill in your bot's token. And the clientID if you feel like it, but you don't have to. If you upload your token to git, get a new one.
	Edit thorium_variables.json. It's mostly self-explanatory; obey_forever_roles can't be removed from power unless you edit this file.
	None of thorium's variables are server-specific. If you want that, you'll need to implement it yourself, or else run multiple instances of the bot.
	Run 'node thorium.js'
## Known problems:
	Messages posted before the bot starts running won't be monitored for reactions.
	None of thorium's variables are server-specific.
	Thorium relies on role-names, which might not be that secure.