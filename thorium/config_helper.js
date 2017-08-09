var opn = require('opn')
var fs = require('fs')
var stdin = process.openStdin()
var authpath = "auth.thorium.json"
var auth = {}

function is_yes(input) {return (input == "" || input == "Y" || input == "y" || input == "yes")}

function is_n(input) {return (input == "N" || input == "n" || input == "no")}

function input1(){
  console.log("To configure Thorium, you will need to:\n1) register a bot at https://discordapp.com/developers/applications/me")
  console.log("2) select 'create a new app'\n3) give it a name and a description, then save changes and click 'create a new bot user.'\n4) copy down your Client ID and your Bot's token.\n\nopen https://discordapp.com/developers/applications/me now? Y/n")
  stdin.once("data",(d)=>{
    var d = ''+d.slice(0,d.length-1)
    if(is_yes(d)){
      opn("https://discordapp.com/developers/applications/me")
      input2()
    }else if(is_n(d)){
      input2()
    }else{
      console.log('Unrecognized input.\nopen https://discordapp.com/developers/applications/me now? Y/n')
      input1()
    }
  })
}

function input2(){
  console.log("Enter your client id:")
  stdin.once("data",(d)=>{
    var d = ''+d.slice(0,d.length-1)
    auth.client_id = d
    auth.register_on_guild = "https://discordapp.com/oauth2/authorize?&client_id="+d+"&scope=bot&permissions=0"
    input3()
  })
}

function input3(){
  console.log("Enter your bot's token:")
  stdin.once("data",(d)=>{
    var d = ''+d.slice(0,d.length-1)
    auth.auth_discord_thorium = d
    input4()
  })
}

function input4(){
  console.log("Create new authentication file using token and client id? Y/n")
  stdin.once("data",(d)=>{
    var d = ''+d.slice(0,d.length-1)
    if(is_yes(d)){
      fs.writeFileSync(authpath, JSON.stringify(auth))
      input5()
    }else if(is_n(d)){
      input5()
    }else{
      console.log('Unrecognized input.')
      input4()
    }
  })
}

function input5(){
  console.log("Add bot to a guild/server? Requires you to have input client id. Y/n")
  stdin.once("data",(d)=>{
    var d = ''+d.slice(0,d.length-1)
    if(is_yes(d)){
      opn(auth.register_on_guild)
      input6()
    }else if(is_no(d)){
      input6()
    }else{
      console.log('Unrecognized input.')
      input5()
    }
  })
}

function input6(){
  console.log("Configuration complete! Run 'node thorium.js' to get started")
}

input1()