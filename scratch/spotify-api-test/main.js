var spotify = new (require('spotify-web-api-node'))()
var fs = require('fs')
var opn = require('opn')
var request = require('request')
var pathify = str=> str.replace(/^~(?=\/|$)/,process.env.HOME)
var read = x=> fs.readFileSync(pathify(x[0]))    // read`~/file`
var write = (x,y)=> fs.writeFileSync(pathify(x),y) // write('~/file',stuff)
var JSON_pretty = x => JSON.stringify(x,null,'  ')
var set_creds = () => spotify.setCredentials(JSON.parse(read`~/.auth/spotiman`))
var update_creds = new_creds =>{
	console.log('updating creds')
	var old = spotify.getCredentials()
	new_creds.access_token && (old.accessToken = new_creds.access_token)
	new_creds.refresh_token && (old.refreshToken = new_creds.refresh_token)
	spotify.setCredentials(old)
	write('~/.auth/spotiman',JSON_pretty(spotify.getCredentials()))
}
function get_url(url){request.get({url: url, headers: { 'Authorization': 'Bearer ' + spotify.getCredentials().accessToken }, json: true},x=>{return promise.resolve(x)})}
var depaginate = (href) => {
	console.log(href)
	return get_url(href).then(page=>{
		page = page.body
		if (!page.next) {return promise.resolve(page.items)}
		return depaginate(page.next,fetch).then(x=>promise.resolve(page.items.concat(x)))})
}
var do_spotify_stuff = () => {
	console.log('doing spotify stuff')
	spotify.getUserPlaylists().then(x=>x.body.items.slice(0,1).map(pl=>{
		var uri_regex = /^spotify:user:(\d+):\w+:([^:]+)$/
		var user = pl.uri.replace(uri_regex,'$1')
		var pl = pl.id
		spotify.getPlaylistTracks(user,pl, {limit: 5}).then(x=>{
			depaginate(x.body.href).then(x=>console.log(x))
			console.log(x.body)
		})
	}))
}
var a = process.argv
set_creds()
if (a[2] === 'auth'){
	opn(spotify.createAuthorizeURL(['playlist-read-private','playlist-read-collaborative','playlist-modify-public','playlist-modify-private','user-library-read','user-library-modify']))
}else if (a[2] === 'auth2') {
	spotify.authorizationCodeGrant(a[3]).then(x=>{
		console.log('authcodeblock')
		x = x.body
		update_creds(x)
	})
}else if (!a[2]){
	spotify.refreshAccessToken().then(x=>{
		x = x.body
		update_creds(x)
		do_spotify_stuff()
	})
}
