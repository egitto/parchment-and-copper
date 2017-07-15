const Discord = require('discord.js')
const client = new Discord.Client()
fs = require('fs')

var variable_storage_path = 'thorium_variables.json'
var auth_discord_thorium = JSON.parse(fs.readFileSync('auth.thorium.json'))['auth_discord_thorium']
client.login(auth_discord_thorium)
var default_parameters = {"watched_emojii":["🗒","🤖","📓","📔"],"log_channel_name":"topicis-logs","threshold":2,"obey_roles":["consuls","conifer","mods","moderators"],"flag_logged_emoji":"🗒"}
var unchangeable_owners = ["consuls","conifer"]

Set.prototype.toJSON = function toJSON() {return [...Set.prototype.values.call(this)]}

x = ''+fs.readFileSync(variable_storage_path)
if (!x){
	x = default_parameters
	console.log('using defaults...')
}else{
	x = JSON.parse(x)
}

client.on('ready', () => {
  console.log('I am ready!')
}) 

var watched_emojii = new Set(x.watched_emojii)
var obey_roles = new Set(x.obey_roles)
var threshold = x.threshold
var log_channel_name = x.log_channel_name
var flag_logged_emoji = x.flag_logged_emoji
var all_data = {watched_emojii: watched_emojii, log_channel_name: log_channel_name, threshold: threshold, obey_roles: obey_roles, flag_logged_emoji: flag_logged_emoji}

function set_log_channel_name(name){
	all_data.log_channel_name = log_channel_name = name
	console.log('log channel changed to '+name)	
}

function change_threshold(value){
	threshold = all_data.threshold = value
	console.log('threshold changed to '+value)
}

function save_parameters(){
	fs.writeFile(variable_storage_path,JSON.stringify(all_data))
}

console.log(JSON.stringify(all_data))
console.log('loading...')

client.on('message', msg => {
	if (msg.content.match(/^[Tt]horium$/)) {
    safe_reply(msg, 'I can serve. \nthreshold: '+threshold+'\nwatched emoji:  '+[...watched_emojii]+'\ncontrol roles: '+[...obey_roles]+'\nlog channel: '+log_channel_name)
    // console.log(msg.channel.guild)
  }
  // console.log(msg.member.roles)
  var obey_this = !!(msg.member.roles.find(function(item){return obey_roles.has(item.name)}, true))
  console.log(obey_this+' '+msg.member.user.username+'/'+msg.member.nickname+'\n  '+msg.content)
	if (obey_this &&(msg.content.match(/^[Tt]horium [^{}()\\]*$/))){
		safe_reply(msg,parse_command_phrase(msg.content.replace(/^[Tt]horium /,'')))
		save_parameters()
	}
}) 

function parse_command_phrase(phrase){
		// what follows is disgusting, avert your eyes.
	  var x = /^threshold (\d+)$/
		if (phrase.match(x)) {
			change_threshold(phrase.replace(x,'$1'))
			return ('New threshold: '+threshold)
		}
		var x = /^watch (.+)$/
		if (phrase.match(x)) {
			watched_emojii.add(phrase.replace(x,'$1'))
			return ('New trigger emoji: '+[...watched_emojii])
		}
		var x = /^unwatch (.+)$/
		if (phrase.match(x)) {
			watched_emojii.delete(phrase.replace(x,'$1'))
			return ('New trigger emoji: '+[...watched_emojii])
	  }
	  var x = /^obey (.+)$/
		if (phrase.match(x)) {
			obey_roles.add(phrase.replace(x,'$1'))
			return ('New control roles: '+[...obey_roles])
	  }
	  var x = /^disobey (.+)$/
		if (phrase.match(x)) {
			obey_roles.delete(phrase.replace(x,'$1'))
			unchangeable_owners.map(function(owner){obey_roles.add(owner)})
			return ('New control roles: '+[...obey_roles])
		}
	  var x = /^change log channel (.+)$/
		if (phrase.match(x)) {
			set_log_channel_name(phrase.replace(x,'$1'))
			return ('New channel: '+log_channel_name)
		}
		if (phrase.match(/^help/)) {
			return ('I can be controlled with these words: \nthreshold $number\nwatch $emoji\nunwatch $emoji\nobey $role\ndisobey $role\nchange log channel $channel\nhelp')
		}
}

function safe_reply(msg,content){
	msg.reply(content,{disableEveryone: true}) 
}

function log_channel(msg){
	return msg.guild.channels.find('name', log_channel_name)
}

function report_error_on_servermeta(msg,errormessage){
	var metachannel = msg.guild.channels.find('name', 'servermeta')
	if (metachannel){
		metachannel.send(errormessage,{disableEveryone: true})
	}
}

function is_watched(emoji){
	return watched_emojii.has(emoji)
	// return true
}

function isnt_logged_yet(msg){
	var logged_react = !!msg.reactions.find('me', true)
	console.log('already logged_react: '+ logged_react)
	return !logged_react
}

client.on('messageReactionAdd', messageReaction => {
	var emoji_name = messageReaction._emoji.name 
	var reacts = messageReaction.count
	console.log('reaction spotted: '+emoji_name+' in #'+messageReaction.message.channel.name)
	msg = messageReaction.message
	if(is_watched(emoji_name) && (reacts >= threshold) && isnt_logged_yet(msg) && (''+msg)){
		// msg = messageReaction.message
		console.log(emoji_name)
		var reply = emoji_name+' at '+msg.createdAt+' in '+msg.channel +', ' +msg.author+' said:\n'+msg
		// console.log(msg)
		if (log_channel(msg)){
			msg.react(flag_logged_emoji)
			log_channel(msg).send(reply,{disableEveryone: true}) 
			console.log('recorded '+reply)
		}else{
			report_error_on_servermeta(msg,'log channel '+log_channel_name+' not found')
		}
	}
}) 