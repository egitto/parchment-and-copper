const Discord = require('discord.js')
const client = new Discord.Client()
fs = require('fs')
curry = require('curry')

var variable_storage_path = 'thorium_variables.json'
var auth_discord_thorium = JSON.parse(fs.readFileSync('auth.thorium.json'))['auth_discord_thorium']
client.login(auth_discord_thorium).catch((err)=>{throw err})

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
  return arr.reduce(function(accumulator,item){return accumulator + item + ', '},'').replace(/, $/,"")
}

function set_to_pretty_string(set){
  return array_to_string([...set])
}
var JSON_pretty = x => JSON.stringify(x,null,'  ')
var save_parameters = () => fs.writeFileSync(variable_storage_path,JSON_pretty(globals))

console.log(JSON.stringify(globals))
console.log('loading...')

client.on('ready', () => {
  console.log('I am ready!')
}) 

client.on('message', message => {
  if (message.content.match(/^[Tt]horium$/)) {
    reply(message, 'I can serve. \nthreshold: ' + globals.threshold + '\nwatched emoji:  ' + set_to_pretty_string(globals.watched_emojii) + '\ncontrol roles: ' + set_to_pretty_string(globals.obey_roles) + '\nlog channel: ' + globals.log_channel_name)
    list_managing(message)
    // console.log(message.channel.guild)
  }
  x = /^topicis:? (.*)/
  if (message.content.match(x)){
    // we don't want the bot to say 'topicis' because that interferes with users searching for that string
    var new_message = Object.create(message)
    new_message.content = message.content.replace(x,'topicis_bot: $1')
    log_message(new_message)
  }
  // console.log(message.member.roles)
  var obey_this = !!(message.member.roles.find(item => {return globals.obey_roles.has(item.name)}, true))
  console.log(obey_this + ' ' + message.member.user.username + '/' + message.member.nickname + '\n  ' + message.content)
  if (message.content.match(/^[Tt]horium [^{}()\\]*$/)){
    parse_unprivileged_command(message)
    if (obey_this){
      parse_command_phrase(message)
      save_parameters()
    }
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

function parse_unprivileged_command(message){
    var phrase = message.content.replace(/^[Tt]horium /,'')
    var user = message.member
    var guild = message.channel.guild
    var x = /^add me to (.+)$/
    if (phrase.match(x)) {
      var y = phrase.replace(x,'$1')
      if (!is_managing_role(y)) {reply(message,"I'm not managing the role "+y); list_managing(message)}
      // else if (!user.guild.roles.has(role.id)) {reply(message,"Error: role does not exist on this server")}
      globals.managed_roles.map((role) => {if ((role.name === y)&& !user.roles.has(role.id) &&user.guild.roles.has(role.id)) {
        user.addRole(role.id).then(()=>
          reply(message,"role "+role.name+" added to you")
        ).catch((err)=>reply(message,""+err))}})
    }
    var x = /^remove me from (.+)$/
    if (phrase.match(x)) {
      var y = phrase.replace(x,'$1')
      if (!is_managing_role(y)) {reply(message,"I'm not managing the role "+y); list_managing(message)}      
      globals.managed_roles.map((role) => {if ((role.name === y)&& user.roles.has(role.id)) {
        user.removeRole(role.id).then(()=>
          reply(message,"role "+role.name+" removed from you")
        ).catch((err)=>reply(message,""+err))}})
    }
    var x = /^(roles? help)|(list roles)|(help)$/
    if (phrase.match(x)) {
      message.reply("I can add or remove members of these roles: " 
      +array_to_string(globals.managed_roles.map(r=>{return r.name}))
      +"\nRequests:\n  add me to $role, remove me from $role, list $role, list roles"
      +"\nCommands (mod only):\n  manage $role, unmanage $role, force manage $role")
    }
    var x = /^list (.+)$/
    if (phrase.match(x)) {
      var y = phrase.replace(x,'$1')
      var response = role_members_usernames(message,y)
      if (response) {reply(message,'members of '+y+': '+response)}
    }
}

function parse_command_phrase(message){
    // what follows is disgusting, avert your eyes.
    var phrase = message.content.replace(/^[Tt]horium /,'')
    var response = null
    var x = /^threshold (\d+)$/
    if (phrase.match(x)) {
      globals.threshold = phrase.replace(x,'$1')
      response = 'New threshold: ' + globals.threshold
    }
    var x = /^watch (.+)$/
    if (phrase.match(x)) {
      globals.watched_emojii.add(phrase.replace(x,'$1'))
      response = 'New watched emoji: ' + set_to_pretty_string(globals.watched_emojii)
    }
    var x = /^unwatch (.+)$/
    if (phrase.match(x)) {
      globals.watched_emojii.delete(phrase.replace(x,'$1'))
      response = 'New watched emoji: ' + set_to_pretty_string(globals.watched_emojii)
    }
    var x = /^obey (.+)$/
    if (phrase.match(x)) {
      var y = phrase.replace(x,'$1')
      if (!is_managing_role(y)){
        globals.obey_roles.add(y)
        reply(message,'New control roles: ' + set_to_pretty_string(globals.obey_roles))
      }else{reply(message,'Unable to assign control role: currently managing role '+y)}
    }
    var x = /^disobey (.+)$/
    if (phrase.match(x)) {
      globals.obey_roles.delete(phrase.replace(x,'$1'))
      globals.obey_forever_roles.map(owner => {globals.obey_roles.add(owner)})
      response = 'New control roles: ' + set_to_pretty_string(globals.obey_roles)
    }
    var x = /^force manage (.+)$/
    if (phrase.match(x)) {
      y = phrase.replace(x,'$1')
      manage_role(y,message,true)
    }        
    var x = /^manage (.+)$/
    if (phrase.match(x)) {
      y = phrase.replace(x,'$1')
      manage_role(y,message,false)
    }    
    var x = /^unmanage (.+)$/
    if (phrase.match(x)) {
      y = phrase.replace(x,'$1')
      unmanage_role(y,message) 
    }
    var x = /^change log channel (.+)$/
    if (phrase.match(x)) {
      globals.log_channel_name = phrase.replace(x,'$1')
      response = 'New channel: ' + globals.log_channel_name
    }
    if (phrase === 'dump parameters') {
      response = '```'+JSON_pretty(globals)+'```'
    }
    if (phrase === 'shut down without confirmation') {
      throw 'shut down by command'
    }
    if (phrase.match(/^help/)) {
      response = 'I can be controlled with these words: \nthreshold $number\nwatch $emoji\nunwatch $emoji\nobey $role\ndisobey $role\nchange log channel $channel\nhelp\nroles help\ndump parameters\nshut down without confirmation'
    }
    if (response) {reply(message,response)}
}

function manage_role(y,message,force){
  var named_roles = message.channel.guild.roles.findAll('name',y)
    if (globals.obey_roles.has(y)){
      reply(message,"Can't manage an obeyed role")
    }else if(is_managing_role(y)){
      reply(message,"Already managing a role by that name")
    }else if (named_roles.length > 0){
      reply(message,"Already exist role(s) with that name; force?")
      if (force && named_roles.length == 1){
        var role = named_roles[0]
        globals.managed_roles.push({id: role.id, name: role.name})
        reply(message,"Forcing management anyway")
      }
    }else{
      message.channel.guild.createRole({name: y, mentionable: true}).then((role) => {
        globals.managed_roles.push({id: role.id, name: role.name})
        reply(message,"New role \""+y+"\" created")
      }).catch((err)=>reply(message,"Error: "+err))
    }
  list_managing(message)
}

function unmanage_role(role_name,message){
  globals.managed_roles = globals.managed_roles.filter(role=>{return role.name !== role_name})
  list_managing(message)
}

function list_managing(message){
  var g = globals.managed_roles.map(role=>{return role.name})
  reply(message,"currently managing: "+array_to_string(g))
}

function is_managing_role(role_name){
  return !globals.managed_roles.every(role=>{return role.name !== role_name})
}

function role_members_usernames(message,role_name){
  var role = message.channel.guild.roles.find('name',role_name)
  if (role) {return array_to_string(role.members.array().map(member=>{return member.user.username}))}
}

function reply(message,content){
  return log_channel(message).send(''+message.member+', '+content,{disableEveryone: true})
  // return message.reply(content,{disableEveryone: true}) 
}

function log_channel(message){
  return message.guild.channels.find('name', globals.log_channel_name)
}

function report_error_on_servermeta(message,errormessage){
  var metachannel = message.guild.channels.find('name', 'servermeta')
  if (metachannel){
    metachannel.send(errormessage,{disableEveryone: true})
  }
}

function is_watched(emoji){
  return globals.watched_emojii.has(emoji)
  // return true
}

function isnt_logged_yet(message){
  var logged_react = !!message.reactions.find('me', true)
  console.log('already logged_react: '+ logged_react)
  return !logged_react
}

function log_message(message,emoji_name){
    // message = messageReaction.message
  console.log(emoji_name)
  emoji_name = emoji_name || globals.flag_logged_emoji
  var reply = emoji_name + ' at `' + message.createdAt + '` in ' + message.channel +', ' +message.author + ' said:\n\n' + message
  // console.log(message)
  if (log_channel(message)){
    message.react(globals.flag_logged_emoji)
    log_channel(message).send(reply,{disableEveryone: true}) 
    console.log('recorded ' + reply)
  }else{
    report_error_on_servermeta(message,'log channel ' + globals.log_channel_name + ' not found')
  }
}

client.on('messageReactionAdd', messageReaction => {
  var emoji_name = messageReaction._emoji.name 
  var reacts = messageReaction.count
  console.log('reaction spotted: ' + emoji_name + ' in #' + messageReaction.message.channel.name)
  message = messageReaction.message
  if(is_watched(emoji_name) && (reacts >= globals.threshold) && isnt_logged_yet(message) && ('' + message)){
    log_message(message,emoji_name)
  }
}) 