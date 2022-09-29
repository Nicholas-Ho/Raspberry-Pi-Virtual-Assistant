var device_id = 0;
var player = undefined;

// Get access token
async function getToken() {
    const response = await fetch('/auth/token');
    const json = await response.json();
    return json.access_token;
}

// Set device id
function setDeviceID(id) {
    device_id = id;
}

// Set player reference
function setPlayer(webPlayer) {
    player = webPlayer;
}

// Only return the first result
async function searchURI(track, artist) {

    return getToken().then(async (token) => {
        var url = 'https://api.spotify.com/v1/search?q=';

        url += track.trim().replace(' ', '%20');
        if(artist != undefined) { url += "%20artist:" +  artist.trim().replace(' ', '%20'); }
        url += '&type=track&limit=1&offset=0';

        var searchOptions = {
            method: 'GET',
            url: url,
            headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type' : 'application/json'
            }
        };

        return axios(searchOptions).then(function(response) {
            if (response['status'] === 200) {
                // What a mouthful.
                console.log(response['data']['tracks']['items']['0']['uri'])
                return response['data']['tracks']['items']['0']['uri'];
            }
        }).catch(function(error){
            console.log(error.response);
            return 0;
        });
    });
}

async function playSong(track, artist) {
    searchURI(track, artist).then(async (spotify_uri) => {
        console.log(spotify_uri);
        getToken().then((token) => {
            fetch(`https://api.spotify.com/v1/me/player/play?device_id=${device_id}`, {
                method: 'PUT',
                body: JSON.stringify({ uris: [spotify_uri] }),
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                },
            });
        });
    });
}

// Get the current state of the Web Player
async function getState() {
    return player.getCurrentState().then(state => {
        if (!state) {
        console.error('User is not playing music through the Web Playback SDK');
        return;
        }
    
        console.log(state);
        return state;
    });
}

// Find out if the player is currently paused
async function isPaused() {
    return getState().then(state => {
        console.log(state['paused']);
        return state['paused'];
    });
}

// Play music
async function play() {
    isPaused().then(paused => {
        if(paused) {
            player.togglePlay()
        }
    })
}

// Pause music
async function pause() {
    isPaused().then(paused => {
        if(!paused) {
            player.togglePlay()
        }
    })
}