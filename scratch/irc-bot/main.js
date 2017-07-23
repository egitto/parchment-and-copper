irc = require('irc')
fs = require('fs')
discord = require('discord.js')

console.log('creating irc client')
irc_auth = JSON.parse(fs.fileReadSync('irc_auth'))
iclient = new irc.Client(irc_auth.server,irc_auth.nickname,{channels: irc_auth.channels})

console.log('creating discord client')
discord_auth = JSON.parse(fs.readFileSync('discord_auth'))['token']
dclient = new discord.Client()
dclient.login(discord_auth).catch((err)=>{console.log('discord login error'); throw err})

console.log('reading connection config')
connections_path = 'irc_discord_connections'
connections = JSON.parse(fs.fileReadSync(connections_path))
// {irc_server: 'something.net', irc_channel: '#rational', discord_guild: '234827', discord_channel: '273872'}
var JSON_pretty = x => JSON.stringify(x,null,'  ')
var write_connections = () => fs.fileWriteSync(connections_path, JSON_pretty(connections))
var add_connection = (json_string) => {
	if json_string.match(/^\{\s*"irc_server":\s*"[\w]+\.[\w]+\",\s*"irc_channel":\s*"#[\w0-9]+",\s*"discord_guild":\s*"\d+",\s*"discord_channel":\s*"\d+"\s*\}$/){
		connections.push(JSON.parse(json_string))
		write_connections()
	}
}

console.log('setting irc listeners')
irc_auth.channels.map(channel=>{
	iclient.addListener('message'+channel, function(from,to,message){
		console.log(channel+': '+from+' => '+to+': '+message)
		on_irc_message(channel,from,to,message)
})}
iclient.addListener('pm', function(from,message){
	console.log(from+' => irc-bot 'message)
	on_irc_pm(from,message)
})

console.log('setting discord listeners')
dclient.on('ready', () => {
  console.log('discord logged in')
})
dclient.on('message', message => {

}


function on_irc_message(channel,from,to,message){
	var on_irc_message_channel
	switch(channel){
		case channel === '#lw': on_irc_message_channel = on_irc_message_lw
		case channel === '#rational': on_irc_message_channel = on_irc_message_rational
	}
	on_irc_message_channel && on_irc_message_channel(from,to,message)
}
function on_irc_message_lw(from,to,message){

}
function on_irc_message_rational(from,to,message){
}
function check_blocked_from_discord_server(from){
	
}
function send_irc_to_discords(channel,from,to,message){
	var targets = connections.filter(x=>x.irc_channel === channel)
	targets.map(x=>{
		var g = dclient.guilds.get(x.discord_guild)
		if (g){
			var c = g.channels.get(x.discord_channel)
			// TODO: implement a system to check if user has been blocked from this channel/guild
			if (c){
				c.send('\n'+channel+': '+from+': '+message,{disableEveryone: true})
			}
		}
	})
}
function send_discord_to_ircs(message){
	var targets = connections.filter(x=>(x.discord_guild === message.channel.guild.id && x.discord_channel === message.channel.id))
	targets.map(x=>{
		var 
	}
}