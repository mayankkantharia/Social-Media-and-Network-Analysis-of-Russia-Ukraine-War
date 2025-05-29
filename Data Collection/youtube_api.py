import json
import time
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = "AIzaSyCN6wQYBpsjSEYtkbVWhCSNnuWQOJo2NQY"
REGION_CODE = "US" 
SEARCH_QUERY = "Russia Ukraine war"
MAX_RESULTS  = 100
CSV_OUTPUT    = "D:\\Data Science\\Semester 3\\Social Media and Networks\\Assignment 2\\Social-Media-A2\\youtube_comments.csv"
JSON_OUTPUT   = "D:\\Data Science\\Semester 3\\Social Media and Networks\\Assignment 2\\Social-Media-A2\\youtube_comments.json"

def search_videos(youtube, query, max_results):
    req = youtube.search().list(
        part="id,snippet",
        q=query,
        type="video",
        order="date",
        maxResults=max_results,
    )
    res = req.execute()
    video_ids = [
        item["id"]["videoId"]
        for item in res.get("items", [])
        if item["snippet"].get("liveBroadcastContent") == "none"
    ]
    return video_ids

def fetch_video_metadata(youtube, video_ids):
    meta = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        resp = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(batch)
        ).execute()
        for item in resp.get("items", []):
            vid = item["id"]
            sn  = item["snippet"]
            st  = item.get("statistics", {})
            meta[vid] = {
                "title":            sn.get("title"),
                "description":      sn.get("description"),
                "channelTitle":     sn.get("channelTitle"),
                "videoPublishedAt": sn.get("publishedAt"),
                "tags":             ";".join(sn.get("tags", [])),
                "viewCount":        st.get("viewCount"),
                "videoLikeCount":   st.get("likeCount"),
                "videoCommentCount":st.get("commentCount")
            }
    return meta

def get_comments(youtube, video_id):
    comments = []
    try:
        req = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100
        )
        while req:
            resp = req.execute()
            for item in resp.get("items", []):
                sn = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "comment_id":         item["id"],
                    "author":             sn.get("authorDisplayName"),
                    "text":               sn.get("textDisplay"),
                    "commentLikeCount":   sn.get("likeCount"),
                    "commentPublishedAt": sn.get("publishedAt"),
                })
            req = youtube.commentThreads().list_next(req, resp)
            time.sleep(1)
    except HttpError as e:
        if e.status == 403 and "commentsDisabled" in str(e):
            print(f"  ⚠️ Skipping {video_id}: comments disabled")
            return []
        else:
            raise
    return comments

def collect_comments():
    yt = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    vids = search_videos(yt, SEARCH_QUERY, MAX_RESULTS)
    print(f"Found {len(vids)} videos for '{SEARCH_QUERY}'")

    meta = fetch_video_metadata(yt, vids)

    records = []
    for vid in vids:
        print(f"Processing {vid} …")
        comms = get_comments(yt, vid)
        if not comms:
            continue
        for c in comms:
            rec = {"video_id": vid, **meta.get(vid, {}), **c}
            records.append(rec)
        time.sleep(1)

    with open(JSON_OUTPUT, "w", encoding="utf-8") as jf:
        json.dump(records, jf, ensure_ascii=False, indent=2)

    fields = [
        "video_id","title","description","channelTitle","videoPublishedAt",
        "tags","viewCount","videoLikeCount","videoCommentCount",
        "comment_id","author","text","commentLikeCount","commentPublishedAt"
    ]
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fields)
        writer.writeheader()
        for r in records:
            writer.writerow(r)

    print(f"Saved {len(records)} records to {JSON_OUTPUT} and {CSV_OUTPUT}")

if __name__ == "__main__":
    collect_comments()