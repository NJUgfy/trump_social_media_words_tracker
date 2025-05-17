import tweepy
import time
import config
import os
import json
from qywx_sender import QywxSender

class TrumpTracker:
    def __init__(self):
        self.bearer_token = config.get_tweep_api_bearer_token()
        self.tweepy_client = []
        self.qywx_sender = QywxSender()
        for bearer_token in self.bearer_token:
            self.tweepy_client.append(tweepy.Client(bearer_token=bearer_token))
        self.tweepy_client_number = len(self.tweepy_client)
        self.tweepy_current_client_index = 0

        self.tweepy_target_user_id = config.get_tweep_api_target_user_id()

        if self.tweepy_target_user_id == None or self.tweepy_target_user_id == '':
            self.target_username = config.get_tweep_api_target_username()
            self.user = self.current_tweepy_client().get_user(username=self.target_username)
            self.tweepy_target_user_id = self.user.data.id

        self.state_file = config.get_tweep_state_file()
        self.state = self.load_state()

    def go_next_tweepy_client(self):
        self.tweepy_current_client_index = (self.tweepy_current_client_index + 1) % self.tweepy_client_number
    
    def current_tweepy_client(self):
        return self.tweepy_client[self.tweepy_current_client_index]
        
    def load_state(self):
        default_state = {"last_tweet_id": None, "processed_ids": []}
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    return default_state
                state = json.loads(content)
                if "last_tweet_id" in state and "processed_ids" in state:
                    return state
                return default_state
        return default_state

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def send_message_to_bot(self, tweet):
        print(tweet)
        self.qywx_sender.send_trump_msg_to_all_bot(tweet.text)

    def fetch_new_tweets(self):
        attempt_num = self.tweepy_client_number
        for attempt in range(attempt_num):
            try:
                tweets = self.current_tweepy_client().get_users_tweets(
                    id=self.tweepy_target_user_id,
                    since_id=self.state["last_tweet_id"],
                    exclude=["retweets", "replies"],
                    tweet_fields=["created_at"],
                    max_results=10
                )
                break
            except tweepy.errors.TooManyRequests as e:
                if attempt == attempt_num - 1:
                    raise e
                else:
                    self.go_next_tweepy_client()
                    continue

        if not tweets.data:
            return []
        
        new_tweets = [
            t for t in tweets.data 
            if t.id not in self.state["processed_ids"]
        ]
        
        return sorted(new_tweets, key=lambda x: x.id)

    def process_tweets(self):
        """处理新推文并更新状态"""
        new_tweets = self.fetch_new_tweets()
        new_count = len(new_tweets)

        if new_count == 0:
            return 0

        # 处理所有新推文
        for tweet in new_tweets:
            self.send_message_to_bot(tweet)  # 你的消息发送方法
            self.state["processed_ids"].append(tweet.id)

        # 更新最后处理的ID（使用最大的推文ID）
        self.state["last_tweet_id"] = max(t.id for t in new_tweets)

        # 保持已处理ID列表不超过500个（防止内存膨胀）
        self.state["processed_ids"] = self.state["processed_ids"][-500:]

        self.save_state()
        return new_count

if __name__ == "__main__":
    trumpTracker = TrumpTracker()
    new_count = trumpTracker.process_tweets()

