/**
 * This is an example of a basic node.js script that performs
 * the Authorization Code oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#authorization_code_flow
 */

const express = require('express') // Express web server framework
const request = require('request') // "Request" library
const querystring = require('querystring')
const cookieParser = require('cookie-parser')
const _ = require('underscore')
const fs = require('fs')
const depaginate = require('depaginate')

var scope = 'user-read-email playlist-read-private playlist-read-collaborative user-follow-read user-library-read'
var auths = JSON.parse(fs.readFileSync(process.env.HOME+'/.auth/spotify.json'))
var client_id = auths.client_id
console.log(auths)
var client_secret = auths.client_secret
var redirect_uri = auths.redirect_uri // Your redirect uri

/**
 * Generates a random string containing numbers and letters
 * @param  {number} length The length of the string
 * @return {string} The generated string
 */
var generateRandomString = function(length) {
  var accum = '';  var p = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  for (var i = 0; i < length; i++) {accum += p.charAt(Math.floor(Math.random() * p.length))}
  return accum
}

var stateKey = 'spotify_auth_state'

var app = express()

app.use(express.static(__dirname + '/public'))
   .use(cookieParser())

app.get('/login', function(req, res) {

  var state = generateRandomString(16)
  res.cookie(stateKey, state)

  // your application requests authorization
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }))
})

app.get('/callback', function(req, res) {

  // your application requests refresh and access tokens
  // after checking the state parameter
  console.log('/callback')

  var code = req.query.code || null
  var state = req.query.state || null
  var storedState = req.cookies ? req.cookies[stateKey] : null

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      querystring.stringify({
        error: 'state_mismatch'
      }))
  } else {
    res.clearCookie(stateKey)
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code'
      },
      headers: {
        'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
      },
      json: true
    }

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {

        access_token = auths.access_token = body.access_token,
        refresh_token = auths.refresh_token = body.refresh_token

        var options = {
          url: 'https://api.spotify.com/v1/me',
          headers: { 'Authorization': 'Bearer ' + access_token },
          json: true
        }
        console.log('access_token in request.post: '+access_token)
        // use the access token to access the Spotify Web API
        request.get(options, function(error, response, body) {
          console.log(body)
          console.log(options.headers)
        })
        log_playlists(options,'https://api.spotify.com/v1/me/')
        // we can also pass the token to the browser to make requests from there
        res.redirect('/#' +
          querystring.stringify({
            access_token: access_token,
            refresh_token: refresh_token
          }))
      } else {
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }))
      }
    })
  }
})

function get_url(url,callback_function){request.get({url: url, headers: { 'Authorization': 'Bearer ' + access_token }, json: true},callback_function)}
function inspect_object(x) {console.log(_.pairs(x))}
function get_hrefs_to_multiple_tracklists(playlists) {return playlists.items.map(playlist => playlist['tracks']['href'])}

function get_trackvalues_in_tracklist(tracks,list_of_properties) {
  return tracks['items'].map(track => {return list_of_properties.map(property => {return track['track'][property]})})
}

function log_playlists(options,url_prefix){
  var url = url_prefix+'playlists'
  get_url(url,function(error,response,body){
    // console.log(body)
    // console.log(body.items[0])
    body.items.map(item=>{  
      depaginate(get_url(item['tracks']['href'],(error,response,body)=>{
        console.log('=============================\nPlaylist: '+item['name']) //
        console.log(get_trackvalues_in_tracklist(body,['name','id']))
      })
    })
  })
}

app.get('/refresh_token', function(req, res) {

  // requesting access token from refresh token
  var refresh_token = req.query.refresh_token
  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: { 'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64')) },
    form: {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    },
    json: true
  }

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      var access_token = body.access_token
      res.send({
        'access_token': access_token
      })
    }
  })
})

console.log('Listening on 8888')
app.listen(8888)
