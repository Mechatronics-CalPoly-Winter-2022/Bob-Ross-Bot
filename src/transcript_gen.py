"""!
@file transcript_gen.py
@brief This file gets the transcripts for all the Joy of Painting Episodes on 
YouTube.

@author Kyle Jennings, Zarek Lazowski, William Dorosk
@date 2020-Feb-22
"""

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import os

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
API_KEY = "AIzaSyBNi-0rUTTiOWQOOYIvKzISnwnxO_D_NsE"


# fix the path for the os
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))

def main():
    # get all the video id's from the playlist
    api_service_name = "youtube"
    api_version = "v3"

    youtube = build(api_service_name, api_version, developerKey=API_KEY)

    next_page_token = ""

    while True:
        # start the loop until we have no more pages (5 at a time)
        
        # request the first five playlist items
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId="PLAEQD0ULngi67rwmhrkNjMZKvyCReqDV4",
            pageToken=next_page_token
        )
        response = request.execute()
        next_page_token = response["nextPageToken"]

        # isolate the video id's and titles
        items = response["items"]
        titles = [items['snippet']['title'].replace(" ", "_") for items in items]
        ids = [items['snippet']['resourceId']['videoId'] for items in items]

        # get the transcript for each video
        for id, title in zip(ids, titles):
            try:
                transcript = YouTubeTranscriptApi.get_transcript(id)
            except TranscriptsDisabled:
                continue
            text_list = [x['text'] for x in transcript]
            text = ' '.join(text_list).encode('ascii', 'ignore').decode()
            
            # write the transcript to a file
            with open(fixpath(f"data/transcripts/{title}.txt"), "w") as f:
                f.write(text)

        # if there is no next page, break the loop
        if not next_page_token:
            break

if __name__ == "__main__":
    main()