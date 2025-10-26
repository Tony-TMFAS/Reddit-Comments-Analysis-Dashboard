# Reddit Product Recommendation Analysis Dashboard


## Project Overview
This project implements a complete data analysis pipeline for extracting product recommendations from Reddit comments in consumer-focused subreddits such as r/BuyItForLife, r/SkincareAddiction, and r/ProductReviews. By combining natural language processing and machine learning techniques, the system identifies product and brand mentions, evaluates sentiment, and measures enthusiasm to uncover high-value recommendations based on community feedback.
The pipeline processes over 53,000 comments, revealing key patterns: 61% positive sentiment, dominant mentions like "skin" (1,850 occurrences) and "phone" (1,341 occurrences), and low average enthusiasm (0.03), indicating moderate rather than fervent endorsements. An interactive Streamlit dashboard enables users to filter results by subreddit, sentiment, and enthusiasm threshold, facilitating targeted exploration for business or research applications.
🚀 What This Project Does
The system segments Reddit comments to surface actionable insights, including:

Sentiment Trends: Classifies comments as positive (61%), negative (21%), or neutral (18%) using lexicon-based analysis.
Product Mentions: Extracts brands (e.g., "Apple") and products (e.g., "skin care") via keyword matching.
Enthusiasm Scoring: Quantifies hype (0-1 scale) based on positive language indicators.
Subreddit Patterns: Identifies high-engagement communities like r/ProductReviews (average enthusiasm 0.06).

Users interact via a Streamlit app, which queries the processed data and displays Plotly visualizations (mention bars, enthusiasm by subreddit) and filtered samples. For deployment, it integrates with Supabase for scalable querying.

## 🛠️ Tools & Technologies

Pandas
VADER Sentiment
ParidFuzz
Supabase
Streamlit
PLotly
PRAW
Numpy


## 📦 Folder Structure
text.
├── scrape_reddit.py         # Reddit API scraping script
├── analyze.py               # Sentiment & feature extraction
├── dedupe.py                # Deduplication logic
├── export_supabase.py       # Supabase upload
├── dashboard.py             # Streamlit app
├── requirements.txt         # Required Python libraries
├── README.md                # This file
├── .env                     # Environment secrets (not committed)
├── clean_comments.parquet   # Raw scraped data (53k rows)
├── simple_analysis.parquet  # Analyzed data with sentiment/mentions
├── deduped_analysis.parquet # Deduplicated data (~53k unique)
└── supabase_config/         # Optional DB setup scripts (not in repo)

## 📊 Step-by-Step Breakdown
1. Data Acquisition
Comments are scraped using the Reddit API (PRAW) from selected subreddits, targeting top posts and full threads. Preprocessing includes lowercasing and basic stopword removal to standardize text.
Process:

Fetch 100 top posts per subreddit.
Expand "more comments" for complete threads.
Store as Parquet for efficiency.

Output: clean_comments.parquet (53,310 rows: comment_id, subreddit, cleaned).
2. Feature Engineering: Sentiment & Mentions
Sentiment is computed using VADER, a rule-based model optimized for social media. Mentions are identified via regex keyword matching for brands and products. Enthusiasm is derived from a normalized count of positive indicators (e.g., "love", "great").
Process:

VADER compound score (-1 to 1) labeled as negative/neutral/positive.
Keyword dictionaries for brands/products (expandable).
Enthusiasm: Positive word frequency scaled to [0,1].

Output: simple_analysis.parquet (added sentiment_label, enthusiasm, mentions).
3. Deduplication
Exact deduplication uses MD5 hashing to remove identical comments. Fuzzy deduplication samples 10,000 rows with RapidFuzz (90% similarity threshold) to eliminate near-duplicates.
Process:

Hash cleaned text for exact matches (120 dropped).
Sample fuzzy scoring for efficiency (0.1% estimated reduction).
Assign dedupe_score (0-100) for quality assessment.

Output: deduped_analysis.parquet (53,190 unique rows, dedupe_score).
4. Database Export
Processed data is upserted to Supabase PostgreSQL in 1,000-row batches, with mentions serialized to JSONB for querying.
Process:

Cast types (e.g., dedupe_score to int).
Serialize mentions dict to JSONB.
Upsert on comment_id to avoid duplicates.

Output: 53,129 rows in 'comments' table. Verified via SQL queries (e.g., positives in r/SkincareAddiction).
5. Interactive Dashboard
A Streamlit app provides filtering by subreddit, sentiment, and enthusiasm, with Plotly visualizations for mentions and subreddit trends.
Process:

Load from Parquet (local) or Supabase (live).
Apply filters on-the-fly.
Render metrics, bars, and sample tables.

Top Mentions Bar: Horizontal bar chart of mention frequencies (e.g., "skin" at 1,850).
Enthusiasm by Subreddit: Bar chart highlighting r/ProductReviews (0.06 avg).
Sample Comments: Filtered table for qualitative review (e.g., positives with "love" mentions).

## 🌐 Deployment Steps

textpip install -r requirements.txt
streamlit run dashboard.py

## Cloud Deployment:

Push to GitHub repo.
Connect to Streamlit Cloud (share.streamlit.io > New app > Select repo > dashboard.py as main file).
Add secrets (SUPABASE_URL/KEY) in Settings > Secrets for live DB.
Deploy: Auto-builds in 2 minutes.


## Supabase Setup:

Create project at supabase.com (free tier).
Run table creation SQL in SQL Editor (see Step 4).
Run export_supabase.py for upload.


## 🧠 What You Learn

Transforming raw social media text into structured insights (sentiment, mentions).
Building scalable pipelines with deduplication and database integration.
Creating interactive ML products using Streamlit and Supabase.
Combining NLP (VADER) with heuristics for enthusiasm in a full data-to-dashboard workflow.

## 🌐 Live App
👉 Dashboard Link: https://reddit-comments-analysis-dashboard.streamlit.app/
