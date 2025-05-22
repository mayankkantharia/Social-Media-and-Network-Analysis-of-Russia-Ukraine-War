from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import csv

# --- CONFIG ---
YOUTUBE_API_KEY = "AIzaSyCN6wQYBpsjSEYtkbVWhCSNnuWQOJo2NQY"
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# --- 1. Search Videos ---
def search_videos(query, max_results=50):
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        regionCode='US',
        order='relevance',
        maxResults=max_results
    ).execute()
    return [item['id']['videoId'] for item in search_response['items']]

# --- 2. Get Video Details ---
def get_video_details(video_ids):
    videos_data = []
    for i in range(0, len(video_ids), 50):  
        response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=','.join(video_ids[i:i+50])
        ).execute()

        for video in response['items']:
            sn = video['snippet']
            st = video['statistics']
            comment_count = int(st.get("commentCount", 0))

            if comment_count >= 10:
                video_info = {
                    "videoId":           video['id'],
                    "title":             sn.get("title"),
                    "description":       sn.get("description"),
                    "channelTitle":      sn.get("channelTitle"),
                    "videoPublishedAt":  sn.get("publishedAt"),
                    "tags":              ";".join(sn.get("tags", [])),
                    "viewCount":         st.get("viewCount"),
                    "videoLikeCount":    st.get("likeCount"),
                    "videoCommentCount": st.get("commentCount")
                }
                videos_data.append(video_info)
    return videos_data

# --- 3. Get Comments ---
def get_comments(video_id):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        )
        while request:
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'likeCount': comment['likeCount'],
                    'publishedAt': comment['publishedAt']
                })
            request = youtube.commentThreads().list_next(request, response)
    except Exception as e:
        print(f"Error for video {video_id}: {e}")
    return comments

# --- 4. Save CSV ---
def save_to_csv(video_data, file_name="youtube_video_war_data.csv"):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=video_data[0].keys())
        writer.writeheader()
        for row in video_data:
            writer.writerow(row)

# --- 5. Main Execution ---
if __name__ == "__main__":
    query = "RussiaVsUkraine"
    video_ids = search_videos(query, max_results=50)
    filtered_videos = get_video_details(video_ids)

    # Save metadata
    save_to_csv(filtered_videos)

    # Save comments
    all_comments = {}
    for vid in filtered_videos:
        print(f"Fetching comments for: {vid['videoId']}")
        vid_comments = get_comments(vid['videoId'])
        all_comments[vid['videoId']] = vid_comments

    with open("youtube_war_comments.json", "w", encoding='utf-8') as f:
        json.dump(all_comments, f, indent=4)
