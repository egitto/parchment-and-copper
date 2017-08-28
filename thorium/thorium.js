const Discord = require('discord.js')
const client = new Discord.Client()
fs = require('fs')

var variable_storage_path = 'thorium_variables.json'
var auth_discord_thorium = JSON.parse(fs.readFileSync('auth.thorium.json'))['auth_discord_thorium']
client.login(auth_discord_thorium).catch(err => {console.log('login_error'); throw err})

function set_globals_from_json(json){
  var x = JSON.parse(json)
  globals = x
  globals[guild.id].watched_emojii = new Set(x.watched_emojii)
  globals[guild.id].obey_roles = new Set(x.obey_roles)
  globals[guild.id].obey_roles.toJSON = globals[guild.id].watched_emojii.toJSON = function toJSON() {return [...Set.prototype.values.call(this)]}
}

function guild_variables_path(guild){
  return 'config/'+guild.id+'.json'
}

function set_globals_from_config_files(client){
  globals = {}
  client.guilds.array().map(guild => {
    try{read_guild_globals(guild)}
    catch(err){
      initialize_guild(guild)
    }
  })
}
  
function initialize_guild(guild){
  read_guild_globals({id: "TEMPLATE"}) // reads template config file into globals["TEMPLATE"]
  globals[guild.id] = globals["TEMPLATE"]
  save_guild_parameters(guild) // creates the config file
  globals["TEMPLATE"] = undefined 
  read_guild_globals(guild) // read from the config file; this puts the 'name' parameter in globals[guild.id]
  save_guild_parameters(guild) // save so that the guildname parameter is in the config file
}

function read_guild_globals(guild){
  var x = JSON.parse(''+fs.readFileSync(guild_variables_path(guild)))
  globals[guild.id] = x
  globals[guild.id].name = guild.name // for some semblance of human readability
  globals[guild.id].watched_emojii = new Set(x.watched_emojii)
  globals[guild.id].obey_roles = new Set(x.obey_roles)
  globals[guild.id].obey_roles.toJSON = globals[guild.id].watched_emojii.toJSON = function toJSON() {return [...Set.prototype.values.call(this)]}
}

function array_to_string(arr){
  return arr.reduce(function(accumulator,item){return accumulator + item + ', '},'').replace(/, $/,"")
}

function set_to_pretty_string(set){
  return array_to_string([...set])
}

var JSON_pretty = x => JSON.stringify(x,null,'  ')
var save_guild_parameters = guild => fs.writeFileSync(guild_variables_path(guild),JSON_pretty(globals[guild.id]))

console.log('loading...')

client.on('ready', () => {
  console.log('Connected, loading config...')
  set_globals_from_config_files(client)
  console.log('Ready!')
})

client.on('message', process_message) 

client.on('messageUpdate', (old_message,new_message) => process_message(new_message)) // respond to edited messages as if they were new

client.on('guildCreate', guild => initialize_guild(guild)) // called when client _joins_ a guild, despite name

client.on('messageReactionAdd', message_reaction => {
  respond_to_reaction(message_reaction)
}) 

function process_message(message) {
  var guild = message.guild
  if (!guild) return // don't process pms at all
  if (globals[guild.id] == undefined) initialize_guild(guild)
  var x = /^[Tt]opicis:? (.*)/
  if (message.content.match(x)){
    // we don't want the bot to say 'topicis' because that interferes with users searching for that string
    var new_message = Object.create(message)
    new_message.content = message.content.replace(x,'topicis_bot: $1')
    log_message(new_message)
  }
  var obey_this = obey_member(message.member,guild)
  // console.log(obey_this + ' ' + message.member.user.username + '/' + message.member.nickname + '\n  ' + message.content)
  if (message.content.match(/^[Tt]horium,? [^{}()\\]*$/)){
    if (message.channel === log_channel(guild)){
      message.content.split("\n").map(text_to_parse => parse_command(message,text_to_parse,obey_this))
      save_guild_parameters(message.guild)
    }
  }
}

function obey_member(member,guild){
  var obey = false
  obey = obey || !!(member.roles.find(item => {return globals[guild.id].obey_roles.has(item.name)}, true))
  obey = obey || member.hasPermission(['MANAGE_GUILD'],false,true,true)
  return obey
}

function respond_to_reaction(message_reaction){
  var guild = message_reaction.message.guild
  if (!guild) return // don't process pms at all
  var emoji_name = message_reaction._emoji.name 
  var reacts = message_reaction.count
  console.log('reaction spotted: ' + emoji_name + ' in #' + message_reaction.message.channel.name)
  message = message_reaction.message
  if(is_watched(emoji_name,guild) && (reacts >= globals[guild.id].threshold) && isnt_logged_yet(message) && ('' + message)){
    log_message(message,emoji_name)
  }
}

function parse_command(message,text_to_parse,privileged){
  var phrase = text_to_parse.replace(/^[Tt]horium,?( please)? (.+?)(,? please.?)?$/,'$2').toLowerCase()
  console.log(phrase)
  var user = message.member
  var guild = message.channel.guild
  var x
  if (phrase.match(x = /^$/)) {
    reply(message, 'I can serve. \nwatched emoji:  ' + set_to_pretty_string(globals[guild.id].watched_emojii) + '\ncontrol roles: ' + set_to_pretty_string(globals[guild.id].obey_roles) + '\nlog channel: ' + globals[guild.id].log_channel_name)
    list_managing(message)
  }
  if (phrase.match(x = /^(add|send|fly|drag) me to (.+?)$/)) {
    var y = phrase.replace(x,'$2')
    if (user.roles.find('name',y)) {reply(message,"You're already in "+y+", silly!")}
    if (!is_managing_role(y,guild)) {reply(message,"I'm not managing the role "+y); list_managing(message)}
    globals[guild.id].managed_roles.map(role => {if ((role.name === y) && !user.roles.has(role.id) && user.guild.roles.has(role.id)) {
      var forbidden
      if ((forbidden = forbidden_permissions_of(guild.roles.get(role.id))).length == 0){
        user.addRole(role.id).then(
        () => message.react("✅")).catch(err => reply(message,""+err))}
      else {reply(message,"that role has forbidden permission(s): "+array_to_string(forbidden))}
    }})
  }
  if (phrase.match(x = /^(remove|evacuate|kidnap|rescue|save) me from (.+?)$/)) {
    var y = phrase.replace(x,'$2')
    if (!is_managing_role(y,guild)) {reply(message,"I'm not managing the role "+y); list_managing(message)}      
    globals[guild.id].managed_roles.map(role => {if ((role.name === y) && user.roles.has(role.id)) {
      user.removeRole(role.id).then(
        () => message.react("✅")).catch(err => reply(message,""+err))}})
  }
  if (phrase.match(x = /^help$/)) {
    reply(message,"Help on what topic? roles, mod commands, mod roles, logging, permissions")
  }
  if (phrase.match(x = /^(help )?mod roles$/)) {
    reply(message,"I consider the following roles mods to obey: "+set_to_pretty_string(globals[guild.id].obey_roles))
  }
  if (phrase.match(x = /^(help )?logging$/)) {
    reply(message,"When at least "+globals[guild.id].threshold+" of any one of "+set_to_pretty_string(globals[guild.id].watched_emojii)
      +" reactions are added to a message, or when a message is prefaced by 'topicis', I will "
      +" log the message in #"+globals[guild.id].log_channel_name+".")
  }
  if (phrase.match(x = /^(help )?mod commands$/)) {
    reply(message,'Mods can control me with these commands: \nthreshold $number, watch $emoji, unwatch $emoji, obey $role, disobey $role, change log channel $channel, dump parameters, shut down without confirmation, manage $role, unmanage $role, change color $role $color, rename $role -> $newname, list permissions, forbid permission $permission, permit permission $permission')
  }
  if (phrase.match(x = /^(help )?permissions$/)) {
    reply(message,'I maintain a list of "forbidden" permissions as a minor security measure. I can not add people to roles that provide these permissions. Mods can view and edit this list with the following commands: list permissions, forbid permission $permission, permit permission $permission')
  }
  if (phrase.match(x = /^list roles$/)) {
    reply(message,"I can add or remove members of these roles: " 
    +array_to_string(globals[guild.id].managed_roles.map(r => {return r.name}).sort()))
  }
  if (phrase.match(x = /^help roles$/)) {
    reply(message,"Commands:\n  add me to $role, remove me from $role, list $role, list roles, change color $personal_role $color"
    +"\nMod commands:\n  manage $role, unmanage $role, force manage $role")
  }
  if (phrase.match(x = /^list (.+)$/)) {
    var y = phrase.replace(x,'$1')
    var members = role_members_names(message,y)
    if (members){
      console.log('managing this role')
      var response = array_to_string(members)
      reply(message,'members of '+y+': '+response)
    }
  }
  if (phrase.match(x = /^change color ([^ ]+) ([^ ]+)$/)) {
    var success = change_role_colors(privileged,message,phrase.replace(x,'$1'),phrase.replace(x,'$2'))
    reply(message,'role color changed: '+success)
  }
  if (!privileged) {return}
  var response = null
  if (phrase.match(x = /^threshold (\d+)$/)) {
    globals[guild.id].threshold = phrase.replace(x,'$1')
    response = 'New threshold: ' + globals[guild.id].threshold
  }
  if (phrase.match(x = /^watch (.+)$/)) {
    globals[guild.id].watched_emojii.add(phrase.replace(x,'$1'))
    response = 'New watched emoji: ' + set_to_pretty_string(globals[guild.id].watched_emojii)
  }
  if (phrase.match(x = /^unwatch (.+)$/)) {
    globals[guild.id].watched_emojii.delete(phrase.replace(x,'$1'))
    response = 'New watched emoji: ' + set_to_pretty_string(globals[guild.id].watched_emojii)
  }
  if (phrase.match(x = /^obey (.+)$/)) {
    var y = phrase.replace(x,'$1')
    if (!is_managing_role(y,guild)){
      globals[guild.id].obey_roles.add(y)
      reply(message,'New control roles: ' + set_to_pretty_string(globals[guild.id].obey_roles))
    }else{reply(message,'Unable to assign control role: currently managing role '+y)}
  }
  if (phrase.match(x = /^disobey (.+)$/)) {
    globals[guild.id].obey_roles.delete(phrase.replace(x,'$1'))
    globals[guild.id].obey_forever_roles.map(owner => {globals[guild.id].obey_roles.add(owner)})
    response = 'New control roles: ' + set_to_pretty_string(globals[guild.id].obey_roles)
  }
  if (phrase.match(x = /^force manage (.+)$/)) {
    var y = phrase.replace(x,'$1')
    manage_role(y,message,true)
  }        
  if (phrase.match(x = /^manage (.+)$/)) {
    var y = phrase.replace(x,'$1')
    manage_role(y,message,false)
  }    
  if (phrase.match(x = /^rename (.+?) ?-> ?(.+)$/)) {
    var y = phrase.replace(x,'$1')
    var z = phrase.replace(x,'$2')
    rename_role(y,z,message)
  } 
  if (phrase.match(x = /^unmanage (.+)$/)) {
    var y = phrase.replace(x,'$1')
    unmanage_role(y,message) 
  }
  if (phrase.match(x = /^change log channel (.+)$/)) {
    globals[guild.id].log_channel_name = phrase.replace(x,'$1')
    response = 'New channel: ' + globals[guild.id].log_channel_name
  }
  if (phrase.match(x = /^list permissions$/)) {
    response = 'Forbidden permissions: '+array_to_string(globals[guild.id].dangerous_permissions)
    response += '\n\nAll permissions: '+array_to_string(Object.keys(user.permissionsIn(message.channel).serialize()))
  }
  if (phrase.match(x = /^forbid permission (.+)$/)) {
    var y = phrase.replace(x,'$1').toUpperCase()
    globals[guild.id].dangerous_permissions.push(y)
    response = 'Forbid permission "'+y+'"'
  }
  if (phrase.match(x = /^permit permission (.+)$/)) {
    var y = phrase.replace(x,'$1').toUpperCase()
    globals[guild.id].dangerous_permissions = globals[guild.id].dangerous_permissions.filter(x => {return x !== y})
    response = 'Permitted permission "'+y+'"'
  }
  if (phrase === 'dump parameters') {
    response = '```'+JSON_pretty(globals)+'```'
  }
  if (phrase === 'shut down without confirmation') {
    throw 'shut down by command'
  }
  if (response) {reply(message,response)}
  console.log('Command finished')
}

function change_role_colors(privileged,message,role_name,color){
  console.log('changing',role_name,color)
  var role = message.guild.roles.filterArray(x => {return x.name.toLowerCase() === role_name})[0]
  if (!role) {console.log('role '+role_name+' does not exist'); return false}
  var only_member = (role.members.array().length === 1 && role.members.array()[0].user.id === message.author.id)
  if (privileged || only_member){
    role.setColor(color).catch(err => console.log(err))
    console.log('color actually changed')
    return true
  } return false
}

function rename_role(initial,final,message){
  console.log("renaming "+initial+" to "+final)
  var guild = message.guild
  var initial_roles = message.channel.guild.roles.findAll('name',initial)
  var final_roles = message.channel.guild.roles.findAll('name',final)
  if(!is_managing_role(initial,guild)){
    reply(message,"Not managing role "+initial)
  }else if (globals[guild.id].obey_roles.has(final)){
    reply(message,"Can't rename to an obeyed role")
  }else if (initial_roles.length !== 1){
    reply(message,"Is not exactly one role called "+initial)
  }else if (final_roles.length !== 0){
    reply(message,"Already exist role(s) called "+final)
  }else{
    initial_roles[0].setName(final).then(role => {
      globals[guild.id].managed_roles.push({id: role.id, name: role.name.toLowerCase()})
      reply(message,"Role renamed.")
      unmanage_role(initial, message)
    }).catch(err => reply(message,"Error: "+err))
  }
}

function manage_role(y,message,force){
  var named_roles = message.channel.guild.roles.filterArray(x => {return y === x.name.toLowerCase()})
  var guild = message.guild
  if (globals[guild.id].obey_roles.has(y)){
    reply(message,"Can't manage an obeyed role")
  }else if(is_managing_role(y,guild)){
    reply(message,"Already managing a role by that name")
  }else if (named_roles.length > 0){
    reply(message,"Already exist role(s) with that name; force?")
    if (force && named_roles.length == 1){
      var role = named_roles[0]
      globals[guild.id].managed_roles.push({id: role.id, name: role.name.toLowerCase()})
      reply(message,"Forcing management anyway")
    }
  }else{
    message.channel.guild.createRole({name: y, mentionable: true}).then(role => {
      globals[guild.id].managed_roles.push({id: role.id, name: role.name.toLowerCase()})
      reply(message,"New role \""+y+"\" created")
    }).catch(err => reply(message,"Error: "+err))
  }list_managing(message)
}

function unmanage_role(role_name,message){
  var guild = message.guild
  globals[guild.id].managed_roles = globals[guild.id].managed_roles.filter(role => {return role.name.toLowerCase() !== role_name})
  list_managing(message)
}

function list_managing(message){
  var guild = message.guild
  var g = globals[guild.id].managed_roles.map(role => {return role.name}).sort()
  reply(message,"currently managing: "+array_to_string(g))
}

function is_managing_role(role_name,guild){
  return !globals[guild.id].managed_roles.every(role => {return role.name !== role_name})
}

function role_members_names(message,role_name){
  var role = message.channel.guild.roles.find('name',role_name)
  if (role) {return role.members.array().map(member => {return member.displayName})}
}

function reply(message,content){
  var guild = message.guild
  if (log_channel(guild)){
    return log_channel(guild).send(''+message.member+', '+content,{disableEveryone: true})
  }else{ 
    report_error_on_servermeta(message,globals[guild.id].log_channel_name+' not found; run change log channel $channel to fix')
  }
  // return reply(message,content,{disableEveryone: true}) 
}

function forbidden_permissions_of(role){
  var role_permissions = role.serialize()
  return globals[role.guild.id].dangerous_permissions.filter(permission => {return role_permissions[permission]})
}

function log_channel(guild){
  return guild.channels.find('name', globals[guild.id].log_channel_name)
}

function report_error_on_servermeta(message,errormessage){
  var metachannel = message.guild.channels.find('name', 'servermeta')
  if (metachannel){
    metachannel.send(errormessage,{disableEveryone: true})
  }
}

function is_watched(emoji,guild){
  return globals[guild.id].watched_emojii.has(emoji)
  // return true
}

function isnt_logged_yet(message){
  var logged_react = !!message.reactions.find('me', true)
  console.log('already logged_react: '+ logged_react)
  return !logged_react
}

function log_message(message,emoji_name){
    // message = messageReaction.message
  var guild = message.guild
  console.log(emoji_name)
  var emoji_name = emoji_name || globals[guild.id].flag_logged_emoji
  var reply = emoji_name + ' at `' + message.createdAt + '` in ' + message.channel +', ' +message.author + ' said:\n\n' + message
  // console.log(message)
  if (log_channel(guild)){
    message.react(globals[guild.id].flag_logged_emoji)
    log_channel(guild).send(reply,{disableEveryone: true}) 
    console.log('recorded ' + reply)
  }else{
    report_error_on_servermeta(message,'channel \'' + globals[guild.id].log_channel_name + '\' not found. use `change log channel $channelname` to fix.')
  }
}
