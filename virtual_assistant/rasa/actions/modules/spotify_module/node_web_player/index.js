const express = require('express');
require('dotenv').config();
const {readFile} = require('fs');
const axios = require('axios');

const app = express();
const port = process.env.PORT

var spotify_client_id = process.env.SPOTIFY_CLIENT_ID
var spotify_client_secret = process.env.SPOTIFY_CLIENT_SECRET


global.access_token = ''
global.refresh_token = ''

// Utility function
var generateRandomString = function (length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

// Allows the app to serve files in the 'public folder'
app.use(express.static('public'))

// Spotify authentication
app.get('/auth/login', (req, res) => {

    var scope = "streaming \
                    user-read-email \
                    user-read-private"

    var state = generateRandomString(16);

    var auth_query_parameters = new URLSearchParams({
        response_type: "code",
        client_id: spotify_client_id,
        scope: scope,
        redirect_uri: "http://localhost:3000/auth/callback",
        state: state
    })

    res.redirect('https://accounts.spotify.com/authorize/?' + auth_query_parameters.toString());
});

// Serve the Player HTML file if ready
app.get('/', (requests, response) => {
    readFile('./public/player.html', 'utf-8', (err, html) => {
        if(err) {
            response.status(500).send('An error has occured.')
        }

        response.send(html)
    });
});

// Callback to request for the access token with the code provided by Spotify (from /auth/login)
app.get('/auth/callback', (req, res) => {

  // Note: requests library has been deprecated. Using Axios instead.
    
  var code = req.query.code;

  var form = {
    code: code,
    redirect_uri: "http://localhost:3000/auth/callback",
    grant_type: 'authorization_code'
  }

  // Encoding the form parameters to work with Axios
  const data = Object.keys(form)
  .map((key) => `${key}=${encodeURIComponent(form[key])}`)
  .join('&');

  var authOptions = {
    method: 'POST',
    url: 'https://accounts.spotify.com/api/token',
    data,
    headers: {
      'Authorization': 'Basic ' + (Buffer.from(spotify_client_id + ':' + spotify_client_secret).toString('base64')),
      'Content-Type' : 'application/x-www-form-urlencoded'
    }
  };

  axios(authOptions).then(function(response) {
    if (response['status'] === 200) {
      access_token = response['data']['access_token'];
      refresh_token = response['data']['refresh_token'];
      res.redirect('/')
    }
  }).catch(function(error){
    console.log(error)
  });
});

// URL for the access token
app.get('/auth/token', (req, res) => {
    res.json(
       {
          access_token: access_token
       })
      
    // Automatically refreshes tokens
    // Note: requests library has been deprecated. Using Axios instead.

    var form = {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    }
  
    // Encoding the form parameters to work with Axios
    const data = Object.keys(form)
    .map((key) => `${key}=${encodeURIComponent(form[key])}`)
    .join('&');
  
    var authOptions = {
      method: 'POST',
      url: 'https://accounts.spotify.com/api/token',
      data,
      headers: {
        'Authorization': 'Basic ' + (Buffer.from(spotify_client_id + ':' + spotify_client_secret).toString('base64')),
        'Content-Type' : 'application/x-www-form-urlencoded'
      }
    };
  
    axios(authOptions).then(function(response) {
      if (response['status'] === 200) {
        access_token = response['data']['access_token'];
        refresh_token = response['data']['refresh_token'];
      }
    }).catch(function(error){
      console.log(error)
    });
  })

app.listen(port || 3000, () => console.log(`The app has started at http://localhost:${port}/auth/login`));