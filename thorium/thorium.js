const Discord = require('discord.js')
const client = new Discord.Client()
fs = require('fs')
curry = require('curry')

var variable_storage_path = 'thorium_variables.json'
var auth_discord_thorium = JSON.parse(fs.readFileSync('auth.thorium.json'))['auth_discord_thorium']
client.login(auth_discord_thorium)

// Set.prototype.toJSON = function toJSON() {return [...Set.prototype.values.call(this)]}


function set_globals_from_json(json){
  set_globals_from_json(json)
}

function set_globals_from_json(json){
  var x = JSON.parse(json)
  globals = x
  // globals.log_channel_name = x.log_channel_name
  // globals.threshold = x.threshold
  // globals.obey_forever_roles = x.obey_forever_roles
  globals.watched_emojii = new Set(x.watched_emojii)
  globals.obey_roles = new Set(x.obey_roles)
  globals.obey_roles.toJSON = globals.watched_emojii.toJSON = function toJSON() {return [...Set.prototype.values.call(this)]}
  console.log(json)
}

set_globals_from_json('' + fs.readFileSync(variable_storage_path))

function array_to_string(arr){
  return arr.reduce(function(accumulator,item){return accumulator + ', ' + item})
}

function set_to_pretty_string(set){
  return [...set].reduce(function(accumulator,item){return accumulator + ', ' + item})
}

var JSON_pretty = x => JSON.stringify(x,null,'  ')
var save_parameters = () => fs.writeFileSync(variable_storage_path,JSON_pretty(globals))

console.log(JSON.stringify(globals))
console.log('loading...')

client.on('ready', () => {
  console.log('I am ready!')
}) 

client.on('message', msg => {
  if (msg.content.match(/^[Tt]horium$/)) {
    reply(msg, 'I can serve. \nthreshold: ' + globals.threshold + '\nwatched emoji:  ' + set_to_pretty_string(globals.watched_emojii) + '\ncontrol roles: ' + set_to_pretty_string(globals.obey_roles) + '\nlog channel: ' + globals.log_channel_name)
    // console.log(msg.channel.guild)
  }
  x = /^topicis:? (.*)/
  if (msg.content.match(x)){
    // we don't want the bot to say 'topicis' because that interferes with users searching for that string
    var new_message = Object.create(msg)
    new_message.content = msg.content.replace(x,'topicis_bot: $1')
    log_message(new_message)
  }
  // console.log(msg.member.roles)
  var obey_this = !!(msg.member.roles.find(item => {return globals.obey_roles.has(item.name)}, true))
  console.log(obey_this + ' ' + msg.member.user.username + '/' + msg.member.nickname + '\n  ' + msg.content)
  if (obey_this &&(msg.content.match(/^[Tt]horium [^{}()\\]*$/))){
    reply(msg,parse_command_phrase(msg.content.replace(/^[Tt]horium /,'')))
    save_parameters()
  }
}) 

function parse_command_phrase_curried(phrase){
    // lmao this is even worse than before
    var parse = curry((new_parameter_regex,text_response_function,new_value_function,keyword_regex,parameter_name)=>{
      if (!phrase.match(keyword_regex)) {return}
      var x = phrase.match(new_parameter_regex)
      if (!x) {return}
      x = x[0]
      globals[parameter_name] = y = new_value_function(x,globals[parameter_name])
      return {val: y, text: text_response_function(y)}
    })
    globals.threshold = parse(/[\d]+$/)(x => {x})(x => {x})(/^threshold .*/)('threshold') || globals.threshold
    globals.log_channel_name = parse(/[^ ]*$/)(x => {x})(x => {x})(/^change log channel .*/)('log_channel_name') || globals.log_channel_name
    var new_parameter_regex_base = parse(/[^\b]*$/)
    var set_base = new_parameter_regex_base((x,new_value)=>set_to_pretty_string(new_value))
    var add_set = set_base((x,old_value)=>old_value.add(x))

    globals.watched_emojii = add_set(/^watch .*/)('watched_emojii') || globals.watched_emojii
    globals.obey_roles = add_set(/^obey .*/)('obey_roles') || globals.obey_roles

    var subtract_set = set_base((x,old_value)=>old_value.delete(x))
    globals.watched_emojii = subtract_set(/^watch .*/)('watched_emojii') || globals.watched_emojii
    globals.obey_roles = subtract_set(/^obey .*/)('obey_roles') || globals.obey_roles


}

function parse_command_phrase(phrase){
    // what follows is disgusting, avert your eyes.
    var x = /^threshold (\d+)$/
    if (phrase.match(x)) {
      globals.threshold = phrase.replace(x,'$1')
      return 'New threshold: ' + globals.threshold
    }
    var x = /^watch (.+)$/
    if (phrase.match(x)) {
      globals.watched_emojii.add(phrase.replace(x,'$1'))
      return 'New watched emoji: ' + set_to_pretty_string(globals.watched_emojii)
    }
    var x = /^unwatch (.+)$/
    if (phrase.match(x)) {
      globals.watched_emojii.delete(phrase.replace(x,'$1'))
      return 'New watched emoji: ' + set_to_pretty_string(globals.watched_emojii)
    }
    var x = /^obey (.+)$/
    if (phrase.match(x)) {
      globals.obey_roles.add(phrase.replace(x,'$1'))
      return 'New control roles: ' + set_to_pretty_string(globals.obey_roles)
    }
    var x = /^disobey (.+)$/
    if (phrase.match(x)) {
      globals.obey_roles.delete(phrase.replace(x,'$1'))
      globals.obey_forever_roles.map(owner => {globals.obey_roles.add(owner)})
      return 'New control roles: ' + set_to_pretty_string(globals.obey_roles)
    }
    var x = /^change log channel (.+)$/
    if (phrase.match(x)) {
      globals.log_channel_name = phrase.replace(x,'$1')
      return 'New channel: ' + globals.log_channel_name
    }
    if (phrase === 'dump parameters') {
      return '```'+JSON_pretty(globals)+'```'
    }
    if (phrase === 'shut down without confirmation') {
      throw 'shut down by command'
    }
    if (phrase.match(/^help/)) {
      return 'I can be controlled with these words: \nthreshold $number\nwatch $emoji\nunwatch $emoji\nobey $role\ndisobey $role\nchange log channel $channel\nhelp\ndump parameters\nshut down without confirmation'
    }
}

function reply(msg,content){
  msg.reply(content,{disableEveryone: true}) 
}

function log_channel(msg){
  return msg.guild.channels.find('name', globals.log_channel_name)
}

function report_error_on_servermeta(msg,errormessage){
  var metachannel = msg.guild.channels.find('name', 'servermeta')
  if (metachannel){
    metachannel.send(errormessage,{disableEveryone: true})
  }
}

function is_watched(emoji){
  return globals.watched_emojii.has(emoji)
  // return true
}

function isnt_logged_yet(msg){
  var logged_react = !!msg.reactions.find('me', true)
  console.log('already logged_react: '+ logged_react)
  return !logged_react
}

function log_message(msg,emoji_name){
    // msg = messageReaction.message
  console.log(emoji_name)
  emoji_name = emoji_name || globals.flag_logged_emoji
  var reply = emoji_name + ' at `' + msg.createdAt + '` in ' + msg.channel +', ' +msg.author + ' said:\n\n' + msg
  // console.log(msg)
  if (log_channel(msg)){
    msg.react(globals.flag_logged_emoji)
    log_channel(msg).send(reply,{disableEveryone: true}) 
    console.log('recorded ' + reply)
  }else{
    report_error_on_servermeta(msg,'log channel ' + globals.log_channel_name + ' not found')
  }
}

client.on('messageReactionAdd', messageReaction => {
  var emoji_name = messageReaction._emoji.name 
  var reacts = messageReaction.count
  console.log('reaction spotted: ' + emoji_name + ' in #' + messageReaction.message.channel.name)
  msg = messageReaction.message
  if(is_watched(emoji_name) && (reacts >= globals.threshold) && isnt_logged_yet(msg) && ('' + msg)){
    log_message(msg,emoji_name)
  }
}) 