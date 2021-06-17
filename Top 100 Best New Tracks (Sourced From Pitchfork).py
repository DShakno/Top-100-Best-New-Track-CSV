import requests
import pandas as pd
from bs4 import BeautifulSoup

url_pitchfork = 'https://pitchfork.com/reviews/best/tracks/'
# Enter Spotify API Key
spot_api_key = ''

def get_url(url):
    
    # returns the html in text from the url provided 
    return requests.get(url).text


# get html of each set of songs
html_str_pitchfork = get_url(url_pitchfork)

# cleans the specified page on pitchfork website
def clean_pitchfork(text):
    soup = BeautifulSoup(text)
    
    # set up list for the artist column
    temp_artist = soup.find_all('ul', class_ = "artist-list")
    
    # set up list for the song name column
    temp_song_name = soup.find_all('h2')
    
    # set up ticker for the for loop
    # this will always remain valid because every artist added to list
    # needs to have a song name accompanied with it 
    loop_ticker = len(soup.find_all('ul', class_ = "artist-list"))
    
    # create empty list
    song_list = []
    
    for i in range(loop_ticker):
        # create temporary dictionary
        song_dict = dict()
        
        # add artist name to dictionary
        song_dict['artist'] = temp_artist[i].li.text
        
        # add source name to dictionary
        song_dict['source'] = "pitchfork"
        
        # get track name and remove "" surrounding surrounding it
        temp_track_name = temp_song_name[i].text.split("“ ”")[0]
        temp_track_name = temp_track_name.replace("“", "")
        temp_track_name = temp_track_name.replace("”", "")
        # add track name to dictionary
        song_dict['track'] = temp_track_name
        
        # append dictionary to the list
        song_list.append(song_dict)
    
    # create dataframe from the list
    df_song = pd.DataFrame(song_list)
    return df_song

# web scrape tracks from html of pages
df_pitchfork = clean_pitchfork(html_str_pitchfork)

# record source of each track
df_pitchfork['source'] = 'pitchfork'

# create dataframe for first page
html_str = get_url('https://pitchfork.com/reviews/best/tracks/?page=1')
df_top_100_tracks = clean_pitchfork(html_str)

# loop through pages 2 through 10
for i in range(2,17):
    # update url for each page
    url = f'https://pitchfork.com/reviews/best/tracks/?page={i}'
    temp_str = get_url(url)
    
    # create dataframe for each page
    df_temp = clean_pitchfork(temp_str)
    
    # update original dataframe by concatonating temporary dataframe with the original
    df_top_100_tracks = pd.concat([df_pitch_10page, df_temp], ignore_index=True)

df_top_100_tracks.to_csv('BestNewTop100TracksPitchfork')
