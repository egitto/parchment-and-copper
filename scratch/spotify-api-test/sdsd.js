var spotify = new (require('spotify-web-api-node'))()
var fs = require('fs')
var opn = require('opn')
var pathify = str=> str.replace(/^~(?=\/|$)/,process.env.HOME)
var read = x=> fs.readFileSync(pathify(x[0]))    // read`~/file`
var write = (x,y)=> fs.writeFileSync(pathify(x),y) // write('~/file',stuff)
var JSON_pretty = x => JSON.stringify(x,null,'  ')
var set_creds = () => spotify.setCredentials(JSON.parse(read`~/.auth/spotiman`))
var update_creds = new_creds =>{
	var old = spotify.getCredentials()
	new_creds.access_token && (old.accessToken = new_creds.access_token)
	new_creds.refresh_token && (old.refreshToken = new_creds.refresh_token)
	spotify.setCredentials(old)
	write('~/.auth/spotiman',JSON_pretty(spotify.getCredentials()))
}
var a = process.argv
if (a[2] === 'auth'){
	opn(spotify.createAuthorizeURL(['playlist-read-private','playlist-read-collaborative','playlist-modify-public','playlist-modify-private','user-library-read','user-library-modify']))
}else if (a[2] === 'auth2') {
	spotify.authorizationCodeGrant(a[3]).then(x=>{
		x = x.body
		update_creds(x)
	}).done()
}else if (!a[2]){
	spotify.refreshAccessToken().then(x=>{x = x.body; update_creds(x)
		do_spotify_stuff()
	}).done()
}