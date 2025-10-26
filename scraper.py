import os
import time
import csv  # Unused but in your snippet; kept for legacy
import praw
from datetime import datetime, timezone
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

SUBREDDITS = ["BuyItForLife", "ProductReviews", "headphones",
              "MechanicalKeyboards", "CampingandHiking", "SkincareAddiction", "frugalmalefashion", "frugal", "gadgets"]


def fetch_from_subreddit(sub, submissions_limit=30):
    rows = []
    sr = reddit.subreddit(sub)
    for submission in sr.search("best OR recommendation OR favorites", sort="top", limit=submissions_limit):
        if submission.num_comments < 5:
            continue
        submission.comments.replace_more(limit=0)
        for c in submission.comments.list():
            if str(c.author) == "[deleted]":  # Basic bot/deleted filter
                continue
            rows.append({
                "submission_id": submission.id,
                "submission_title": submission.title,
                "submission_url": f"https://reddit.com{submission.permalink}",
                "subreddit": sub,
                "comment_id": c.id,
                "comment_body": c.body,
                "author": str(c.author),
                "created_utc": datetime.fromtimestamp(c.created_utc, tz=timezone.utc).isoformat(),
                "score": c.score,
                "permalink": f"https://reddit.com{c.permalink}"
            })
        time.sleep(1)  # Throttle for politeness
    return rows


if __name__ == "__main__":
    all_rows = []
    for s in SUBREDDITS:
        print(f"Fetching from {s}...")
        all_rows.extend(fetch_from_subreddit(s, submissions_limit=30))
    df = pd.DataFrame(all_rows)
    os.makedirs("data", exist_ok=True)
    df.to_parquet("raw_reddit_comments.parquet", index=False)
    print(f"Saved {len(df)} comments")
