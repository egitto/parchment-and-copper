spotify = new (require('spotify-web-api-node'))()
fs = require('fs')
opn = require('opn')

const read = x=> fs.readFileSync((x[0].replace(/^~(?=\/|$)/,process.env.HOME)))    // read`~/file`
const write = (x,y)=> fs.writeFileSync(x.replace(/^~(?=\/|$)/,process.env.HOME),y) // write('~/file',stuff)
const JSON_pretty = x => JSON.stringify(x,null,'  ')

var set_creds = () => spotify.setCredentials(JSON.parse(read`~/.auth/spotiman`))

var update_creds = new_creds =>{
	old = spotify.getCredentials()
	new_creds.access_token && (old.accessToken = new_creds.access_token)
	new_creds.refresh_token && (old.refreshToken = new_creds.refresh_token)
	spotify.setCredentials(old)
	write('~/.auth/spotiman',JSON_pretty(spotify.getCredentials()))
}

a = process.argv
if (a[2] == 'auth'){
	opn( spotify.createAuthorizeURL(['playlist-read-private','playlist-read-collaborative','playlist-modify-public','playlist-modify-private','user-library-read','user-library-modify']) )
}else if (a[2] == 'auth2') {
	spotify.authorizationCodeGrant(a[3]).then(x=>{
		x = x.body
		update_creds(x)
	}).done()
}else if (!a[2]){
	spotify.refreshAccessToken().then(x=>{x = x.body; update_creds(x)
		do_spotify_stuff()
	}).done()
}