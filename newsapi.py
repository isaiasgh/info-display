import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

class NEWSAPI:
    def __init__(self, type='tech', max_req_per_day=100, no_late_night=True):
        load_dotenv()
        self.api_key = os.getenv("NEWS_API")
        self.type = type
        self.max_req_per_day = max_req_per_day
        self.no_late_night = no_late_night
        self.url = self._get_url()
        self.eastern_tz = timezone(timedelta(hours=-5))
        self.data = []
        self.last_fetch_time = None
        self.rotation = 0 #we pull 10 stories and rotate between 5 and 5

    def _get_url(self):
        base_url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'country': 'us',
            'pageSize': 10,
            'apiKey': self.api_key
        }
        if self.type == 'tech':
            params['category'] = 'technology'
        return f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def _is_late_night(self):
        now = datetime.now(self.eastern_tz)
        return now.hour >= 22 or now.hour <= 4

    def _should_fetch(self):
        if not self.last_fetch_time:
            return True
        now = datetime.now(self.eastern_tz)
        time_since_last_fetch = now - self.last_fetch_time
        if self.no_late_night:
            if self._is_late_night():
                return False
            return time_since_last_fetch > timedelta(hours=18) / (self.max_req_per_day - 10)
        return time_since_last_fetch > timedelta(hours=24) / (self.max_req_per_day - 10)

    def _fetch_stories(self):
        response = requests.get(self.url)
        data = response.json()
        new_stories = []
        for story in data["articles"]:
            dt = datetime.fromisoformat(story['publishedAt'][:-1]).replace(tzinfo=timezone.utc)
            local_time = dt.astimezone(self.eastern_tz)
            new_stories.append({
                "source": story["source"]["name"],
                "headline": story["title"][:-3-len(story["source"]["name"])],
                "time": local_time.strftime('%Y-%m-%d %I:%M %p'),
                "body": story["description"]
            })
        self.data = new_stories
        self.last_fetch_time = datetime.now(self.eastern_tz)

    def get_stories(self):
        if self._should_fetch():
            self._fetch_stories()

        if self.rotation == 0:
            self.rotation = 1
            return self.data[:len(self.data)//2]
        else:
            self.rotation = 0
            return self.data[len(self.data)//2:]