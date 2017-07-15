const Discord = require('discord.js')
const client = new Discord.Client()
fs = require('fs')
curry = require('curry')

var variable_storage_path = 'thorium_variables.json'
var auth_discord_thorium = JSON.parse(fs.readFileSync('auth.thorium.json'))['auth_discord_thorium']
client.login(auth_discord_thorium)

// Set.prototype.toJSON = function toJSON() {return [...Set.prototype.values.call(this)]}

x = '' + fs.readFileSync(variable_storage_path)
x = JSON.parse(x)

var watched_emojii = new Set(x.watched_emojii)
var obey_roles = new Set(x.obey_roles)
obey_roles.toJSON = watched_emojii.toJSON = function toJSON() {return [...Set.prototype.values.call(this)]}
var threshold = x.threshold
var log_channel_name = x.log_channel_name
var flag_logged_emoji = x.flag_logged_emoji
var obey_forever_roles = x.obey_forever_roles
var all_data = {watched_emojii: watched_emojii, log_channel_name: log_channel_name, threshold: threshold, obey_roles: obey_roles, flag_logged_emoji: flag_logged_emoji, obey_forever_roles: obey_forever_roles}

function set_log_channel_name(name){
	all_data.log_channel_name = log_channel_name = name
	console.log('log channel changed to ' + name)	
}

function set_threshold(value){
	threshold = all_data.threshold = value
	console.log('threshold changed to ' + value)
}

function array_to_string(arr){
	return arr.reduce(function(accumulator,item){return accumulator + ', ' + item})
}

function set_to_string(set){
	return [...set].reduce(function(accumulator,item){return accumulator + ', ' + item})
}

function save_parameters(){
	var JSON_pretty = x => JSON.stringify(x,null,'  ')
	fs.writeFileSync(variable_storage_path,JSON_pretty(all_data))
}

console.log(JSON.stringify(all_data))
console.log('loading...')

client.on('ready', () => {
  console.log('I am ready!')
}) 

client.on('message', msg => {
	if (msg.content.match(/^[Tt]horium$/)) {
    reply(msg, 'I can serve. \nthreshold: ' + threshold + '\nwatched emoji:  ' + set_to_string(watched_emojii) + '\ncontrol roles: ' + set_to_string(obey_roles) + '\nlog channel: ' + log_channel_name)
    // console.log(msg.channel.guild)
  }
  // console.log(msg.member.roles)
  var obey_this = !!(msg.member.roles.find(function(item){return obey_roles.has(item.name)}, true))
  console.log(obey_this + ' ' + msg.member.user.username + '/' + msg.member.nickname + '\n  ' + msg.content)
	if (obey_this &&(msg.content.match(/^[Tt]horium [^{}()\\]*$/))){
		reply(msg,parse_command_phrase(msg.content.replace(/^[Tt]horium /,'')))
		save_parameters()
	}
}) 

function parse_command_phrase_curried(phrase){
		// lmao this is even worse than before
		var parse = curry(function(new_parameter_regex,text_response_function,new_value_function,keyword_regex,parameter_name){
			if (!phrase.match(keyword_regex)) {return}
			if (! (x = phrase.match(new_parameter_regex))) {return}
			x = x[0]
			all_data[parameter_name] = y = new_value_function(x,all_data[parameter_name])
			return {val: y, text: text_response_function(y)}
		})
		threshold = parse(/[\d]+$/)(x => {x})(x => {x})(/^threshold .*/)('threshold') || threshold
		log_channel_name = parse(/[^ ]*$/)(x => {x})(x => {x})(/^change log channel .*/)('log_channel_name') || log_channel_name
		var new_parameter_regex_base = parse(/[^\b]*$/)
		var set_base = new_parameter_regex_base((x,new_value)=>set_to_string(new_value))
		var add_set = set_base((x,old_value)=>old_value.add(x))

		watched_emojii = add_set(/^watch .*/)('watched_emojii') || watched_emojii
		obey_roles = add_set(/^obey .*/)('obey_roles') || obey_roles

		var subtract_set = set_base((x,old_value)=>old_value.delete(x))
		watched_emojii = subtract_set(/^watch .*/)('watched_emojii') || watched_emojii
		obey_roles = subtract_set(/^obey .*/)('obey_roles') || obey_roles


}

function parse_command_phrase(phrase){
		// what follows is disgusting, avert your eyes.
	  var x = /^threshold (\d+)$/
		if (phrase.match(x)) {
			set_threshold(phrase.replace(x,'$1'))
			return 'New threshold: ' + threshold
		}
		var x = /^watch (.+)$/
		if (phrase.match(x)) {
			watched_emojii.add(phrase.replace(x,'$1'))
			return 'New trigger emoji: ' + set_to_string(watched_emojii)
		}
		var x = /^unwatch (.+)$/
		if (phrase.match(x)) {
			watched_emojii.delete(phrase.replace(x,'$1'))
			return 'New trigger emoji: ' + set_to_string(watched_emojii)
	  }
	  var x = /^obey (.+)$/
		if (phrase.match(x)) {
			obey_roles.add(phrase.replace(x,'$1'))
			return 'New control roles: ' + set_to_string(obey_roles)
	  }
	  var x = /^disobey (.+)$/
		if (phrase.match(x)) {
			obey_roles.delete(phrase.replace(x,'$1'))
			obey_forever_roles.map(function(owner){obey_roles.add(owner)})
			return 'New control roles: ' + set_to_string(obey_roles)
		}
	  var x = /^change log channel (.+)$/
		if (phrase.match(x)) {
			set_log_channel_name(phrase.replace(x,'$1'))
			return 'New channel: ' + log_channel_name
		}
		if (phrase.match(/^help/)) {
			return 'I can be controlled with these words: \nthreshold $number\nwatch $emoji\nunwatch $emoji\nobey $role\ndisobey $role\nchange log channel $channel\nhelp'
		}
}

function reply(msg,content){
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
	console.log('reaction spotted: ' + emoji_name + ' in #' + messageReaction.message.channel.name)
	msg = messageReaction.message
	if(is_watched(emoji_name) && (reacts >= threshold) && isnt_logged_yet(msg) && ('' + msg)){
		// msg = messageReaction.message
		console.log(emoji_name)
		var reply = emoji_name + ' at ' + msg.createdAt + ' in ' + msg.channel +', ' +msg.author + ' said:\n' + msg
		// console.log(msg)
		if (log_channel(msg)){
			msg.react(flag_logged_emoji)
			log_channel(msg).send(reply,{disableEveryone: true}) 
			console.log('recorded ' + reply)
		}else{
			report_error_on_servermeta(msg,'log channel ' + log_channel_name + ' not found')
		}
	}
}) 