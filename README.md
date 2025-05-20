# trump_social_media_words_tracker
实时抓取特朗普言论，推送到企业微信机器人
catch trump's words in twitter/x, and push those words to qywx bot.

# quick start 快速使用
wget trump_social_media_words_tracker <br>
vim trump_social_media_words_tracker/config.ini (use your own config) <br>
crontab -e <br>
*/20 * * * * {path}/trump_social_media_words_tracker/run.sh <br>

# what does the config means? 这些配置都代表什么
[TWEEPY]
ACCOUNT_NUMBER -> how many tweepy api account do you have. <br>
BEARER_TOKEN_{} -> each of your tweepy bearer token in your accounts, {} means the number, from 1, 2 ... to {ACCOUNT_NUMBER}, if you only have one account, just use BEARER_TOKEN_1 <br>
TARGET_USER_ID -> the target user's id, for trump, it's 25073877 <br>
TARGET_USERNAME -> the target user's username, for trump, it's RealDonaldTrump <br>
STATE_FILE -> tweet_state.json , file name for storage use, you can use the default value "tweet_state.json"
[QYWX]
QYWX_WEBHOOK_NUMBER -> how many qywx webhooks do you have. <br>
QYWX_WEBHOOK_{} -> each of your webhooks you have, {} means the number from 1, 2... to {QYWX_WEBHOOK_NUMBER}

# 效果预览
![image](https://github.com/user-attachments/assets/a7de4aef-874e-4f82-8f28-17396c420b4a)
