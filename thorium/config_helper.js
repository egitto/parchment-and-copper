var opn = require('opn')
var fs = require('fs')
var stdin = process.openStdin()
var authpath = "auth.thorium.json"
var auth = {}

function input1(){
  console.log("To configure Thorium, you will need to register a bot at https://discordapp.com/developers/applications/me")
  console.log("Once there, select 'create a new app'\n Give it a name and a description, then save changes and click 'create a new bot user.'\n Copy down your Client ID and your Bot's token.\n\nopen https://discordapp.com/developers/applications/me now? Y/n")
  stdin.once("data",(d)=>{
    if(d == "" || d == "Y" || d == "y" || d == "yes"){
      opn("https://discordapp.com/developers/applications/me")
      input2()
    }else if(d == "N" || d == "n" || d == "no"){
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
    auth.client_id = d
    auth.register_on_guild = "https://discordapp.com/oauth2/authorize?&client_id="+d+"&scope=bot&permissions=0"
    input3()
  })
}

function input3(){
  console.log("Enter your bot's token:")
  stdin.once("data",(d)=>{
    auth.auth_discord_thorium = d
    input4()
  })
}

function input4(){
  console.log("Create new authentication file using token and client id? Y/n")
  stdin.once("data",(d)=>{
    if(d == "" || d == "Y" || d == "y" || d == "yes"){
      fs.fileWriteSync(authpath, JSON.stringify(auth))
      input5()
    }else if(d == "N" || d == "n" || d == "no"){
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
    if(d == "" || d == "Y" || d == "y" || d == "yes"){
      opn(auth.register_on_guild)
      input6()
    }else if(d == "N" || d == "n" || d == "no"){
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