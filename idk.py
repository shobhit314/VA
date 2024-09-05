import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotcred import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change to 0 for male voice

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}\n")
    except Exception as e:
        print("Sorry, I did not get that.")
        return None
    return command.lower()

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
     client_secret=SPOTIFY_CLIENT_SECRET,
     redirect_uri=SPOTIFY_REDIRECT_URI,
     scope="user-library-read user-modify-playback-state user-read-playback-state"))

def play_liked_song(song_name):
    try:
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            if song_name.lower() in track['name'].lower():
                sp.start_playback(uris=[track['uri']])
                talk(f'Playing {track["name"]} by {track["artists"][0]["name"]} from your liked songs on Spotify')
                return
        talk('Song not found in your liked songs.')
    except Exception as e:
        print(f"An error occurred while searching for the song: {e}")
        talk('There was an error playing the song from your liked songs on Spotify.')

def run_assistant():
    command = take_command()
    if command:
        if 'play' in command and 'from liked songs' in command:
            song = command.replace('play', '').replace('from liked songs', '').strip()
            play_liked_song(song)
        else:
            talk('I can only play songs from your liked songs on Spotify.')

if __name__ == "__main__":
    while True:
        run_assistant()
