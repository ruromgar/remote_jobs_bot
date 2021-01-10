# Scheduled Telegram Bot

## Intro

This code schedules a bot to send a message everyday to a certain conversation. Follow [the tutorial in Medium.](https://medium.com/@unnonueve/automate-a-telegram-bot-to-send-daily-messages-in-less-than-40-lines-of-python-code-e81858d15854). I've now extended it to get remote job offers and sending them; [check out that tutorial, also in Medium](https://towardsdatascience.com/how-to-create-an-automated-remote-job-finder-with-python-7e20ee233e2b).

## Deploying

Install Serverless framework:

`npm install serverless`

Export credentials:

```
export AWS_ACCESS_KEY_ID=<Access key ID>
export AWS_SECRET_ACCESS_KEY=<Secret access key>
export TELEGRAM_TOKEN=<Your Telegram Token>
```

Install pip requirements:

`pip3 install -r requirements.txt -t . --system`

Deploy to AWS:

`serverless deploy`
