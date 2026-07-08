import os
import json
import feedparser
import requests
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_TARGET_ID = os.getenv("LINE_TARGET_ID")

# Initialize Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using Gemini Pro for maximum compatibility across all regions
    model = genai.GenerativeModel('gemini-pro')
else:
    print("Warning: GEMINI_API_KEY not found. AI summary will be skipped.")
    model = None

def fetch_rss_feeds(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return []

    articles = []
    max_items = config.get("max_items_per_feed", 3)

    for feed in config.get("feeds", []):
        print(f"Fetching {feed['name']}...")
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries[:max_items]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "source": feed["name"]
            })
    return articles

def summarize_with_ai(articles):
    if not model or not articles:
        return "No articles to summarize or Gemini API key missing."
    
    prompt = "สรุปข่าวเทคโนโลยี/AI ประจำวัน จากหัวข้อและเนื้อหาต่อไปนี้ ให้กระชับ เข้าใจง่าย และบอกผลกระทบที่อาจเกิดขึ้น (ถ้ามี) เขียนเป็นภาษาไทยแบบเป็นกันเอง อ่านง่าย:\n\n"
    for i, art in enumerate(articles):
        prompt += f"{i+1}. [{art['source']}] {art['title']}\n"
        # We limit the summary text to avoid token limits just in case
        prompt += f"เนื้อหา: {art['summary'][:500]}...\n"
        prompt += f"Link: {art['link']}\n\n"
        
    prompt += "\nจัดรูปแบบผลลัพธ์เป็น Markdown"

    print("Generating AI summary...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return f"Error generating summary: {e}"

def save_to_markdown(content):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"vault/inbox/{date_str}-digest.md"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    header = f"---\ndate: {date_str}\ntype: daily-digest\n---\n\n# 🗞️ Daily Briefing - {date_str}\n\n"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header + content)
        
    print(f"Saved digest to {filename}")
    return filename

def send_line_message(message):
    if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_TARGET_ID:
        print("Warning: LINE credentials not found. Notification skipped.")
        return
        
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "to": LINE_TARGET_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("Successfully sent LINE notification")
    except Exception as e:
        print(f"Error sending LINE notification: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")

def main():
    print("Starting Learning OS daily sweep...")
    
    # 1. Fetch data
    articles = fetch_rss_feeds()
    print(f"Fetched {len(articles)} articles.")
    
    # 2. Summarize
    ai_summary = summarize_with_ai(articles)
    
    # 3. Save to Markdown
    saved_file = save_to_markdown(ai_summary)
    
    # 4. Generate LINE summary from titles
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    dashboard_url = "https://newton-denny-ebook.incomeinclick.in.th/learning-os/"
    
    notify_msg = f"✅ สรุปข่าวประจำวันมาแล้วครับ! ({len(articles)} เรื่อง)\n\n"
    for i, art in enumerate(articles):
        notify_msg += f"🔹 {art['title']}\n"
    
    notify_msg += f"\n👉 อ่านข่าวเต็มๆ ในหน้า Dashboard สวยๆ ได้ที่:\n{dashboard_url}"
        
    # 5. Notify LINE
    send_line_message(notify_msg)
    
    print("Sweep complete!")

if __name__ == "__main__":
    main()
