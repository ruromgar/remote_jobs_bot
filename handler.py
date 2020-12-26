from datetime import datetime, timezone, timedelta, date
import feedparser
import requests
import telegram
import time
import json
import os
import sys

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = 0 # Your chat ID goes here
TIMELIMIT = 90000 # Around 25 hours
TAGS = ['python', 'java']


def check_if_remoteokio_offer_is_valid(entry):
    # Not valid if older than TIMELIMIT
    now = datetime.timestamp(datetime.now(timezone.utc))
    parsed_date = entry.get('published', '1991-01-24T03:00:00-00:00')[:-6]
    entry_date = datetime.strptime(parsed_date, '%Y-%m-%dT%H:%M:%S').timestamp()

    if now - entry_date > TIMELIMIT:
        return False

    # Not valid if just for USA
    invalid_regions = ['USA', 'America']
    entry_region = entry.get('location', '')

    if entry_region in invalid_regions:
        return False

    # Not valid if the entry does not contain any of the tags
    tags = [t.replace('+', ' ').upper() for t in TAGS]
    entry_tags = [t.get('term', '').upper() for t in entry.get('tags', [])]

    if not any(t in entry_tags for t in tags):
        return False

    return True

def check_if_weworkremotely_offer_is_valid(entry):
    # Not valid if older than TIMELIMIT
    now = datetime.timestamp(datetime.now(timezone.utc))
    parsed_date = entry.get('published', 'Thu, 24 Jan 1991 03:00:00 +0000')
    entry_date = datetime.strptime(parsed_date, '%a, %d %b %Y %H:%M:%S %z').timestamp()

    if now - entry_date > TIMELIMIT:
        return False

    # Not valid if just for USA
    invalid_regions = ['USA Only', 'North America Only']
    entry_region = entry.get('region', '')

    if entry_region in invalid_regions:
        return False

    # Not valid if the summary does not contain any of the tags
    tags = [t.replace('+', ' ').upper() for t in TAGS]
    entry_summary = entry.get('summary', '').upper()

    if not any(t in entry_summary for t in tags):
        return False

    return True

def check_if_workingnomads_offer_is_valid(entry):
    # Not valid if older than TIMELIMIT
    now = datetime.timestamp(datetime.now(timezone.utc))
    parsed_date = entry.get('pub_date', '1991-01-24T03:00:00-00:00')[:19]
    entry_date = datetime.strptime(parsed_date, '%Y-%m-%dT%H:%M:%S').timestamp()

    if now - entry_date > TIMELIMIT:
        return False

    # Not valid if just for USA
    invalid_regions = ['USA', 'America']
    entry_region = entry.get('location', '')

    if entry_region in invalid_regions:
        return False

    # Not valid if the entry does not contain any of the tags
    tags = [t.replace('+', ' ').upper() for t in TAGS]
    entry_tags = entry.get('tags').upper()
    #print(entry_tags)

    if not any(t in entry_tags for t in tags):
        return False

    return True

def check_if_remoteio_offer_is_valid(entry):
    # Not valid if older than TIMELIMIT
    now = datetime.timestamp(datetime.now(timezone.utc))
    parsed_date = entry.get('published', '1991-01-24 03:00:00')
    entry_date = datetime.strptime(parsed_date, '%Y-%m-%d %H:%M:%S').timestamp()

    if now - entry_date > TIMELIMIT:
        return False

    # Not valid if no tags are in the summary or the title
    tags = [t.upper() for t in TAGS]
    entry_summary = entry.get('summary', '').upper()
    entry_title = entry.get('title', '').upper()

    if not any(t in entry_summary for t in tags) and not any(t in entry_title for t in tags):
        return False

    return True

def check_if_githubjobs_offer_is_valid(entry):
    # Not valid if older than TIMELIMIT
    now = datetime.timestamp(datetime.now(timezone.utc))
    parsed_date = entry.get('created_at', 'Thu Jan 24 03:00:00 UTC 1991')
    entry_date = datetime.strptime(parsed_date, '%a %b %d %H:%M:%S UTC %Y').timestamp()

    if now - entry_date > TIMELIMIT:
        return False

    return True


def get_remoteio_offers():
    print('Getting Remote.io offers...')
    rss = feedparser.parse('https://s3.remote.io/feed/rss.xml')
    entries = rss.entries

    offers = [e for e in entries if check_if_remoteio_offer_is_valid(e) is True]

    return [
        {
            'title': offer.get('title'),
            'company': offer.get('company'),
            'date': datetime.strptime(offer.get('published'), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'),
            'link': offer.get('link')
        }
    for offer in offers]

def get_workingnomads_offers():
    print('Getting Working Nomads offers...')
    session = requests.Session()
    session.headers['User-Agent'] = (
        f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, '
        f'like Gecko) Chrome/34.0.1847.131 Safari/537.36')

    response = session.get(f'https://www.workingnomads.co/api/exposed_jobs/')
    entries = json.loads(response.text)

    offers = [e for e in entries if check_if_workingnomads_offer_is_valid(e) is True]

    return [
        {
            'title': offer.get('title'),
            'company': offer.get('company_name'),
            'date': datetime.strptime(offer.get('pub_date')[:19], '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y'),
            'location': offer.get('location'),
            'link': offer.get('url')
        }
    for offer in offers]

def get_weworkremotely_offers():
    print('Getting We Work Remotely offers...')
    rss = feedparser.parse('https://weworkremotely.com/categories/remote-programming-jobs.rss')
    entries = rss.entries

    offers = [e for e in entries if check_if_weworkremotely_offer_is_valid(e) is True]

    return [
        {
            'title': offer.get('title'),
            'company': offer.get('company_name'),
            'date': datetime.strptime(offer.get('published'), '%a, %d %b %Y %H:%M:%S %z').strftime('%d-%m-%Y'),
            'location': offer.get('region'),
            'link': offer.get('link')
        }
    for offer in offers]

def get_remoteokio_offers():
    print('Getting RemoteOK.io offers...')
    rss = feedparser.parse('https://remoteok.io/remote-jobs.rss')
    entries = rss.entries

    offers = [e for e in entries if check_if_remoteokio_offer_is_valid(e) is True]

    return [
        {
            'title': offer.get('title'),
            'company': offer.get('company'),
            'date': datetime.strptime(offer.get('published')[:-6], '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y'),
            'link': offer.get('link')
        }
    for offer in offers]

def get_githubjobs_offers():
    print('Getting GitHub Jobs offers...')
    session = requests.Session()
    session.headers['User-Agent'] = (
        f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, '
        f'like Gecko) Chrome/34.0.1847.131 Safari/537.36')

    entries = []
    for tag in TAGS:
        response = session.get(f'https://jobs.github.com/positions.json?description={tag}&location=remote')
        entries.extend(json.loads(response.text))

    # Removing duplicates based on ID
    entries = list(dict((o['id'], o) for o in entries).values())

    # Extracting the useful info
    offers = [e for e in entries if check_if_githubjobs_offer_is_valid(e) is True]

    return [
        {
            'title': offer.get('title'),
            'company': offer.get('company'),
            'date': datetime.strptime(offer.get('created_at'), '%a %b %d %H:%M:%S UTC %Y').strftime('%d-%m-%Y'),
            'link': offer.get('url')
        }
    for offer in offers]


def main():
    remoteio = get_remoteio_offers()
    workingnomads = get_workingnomads_offers()
    weworkremotely = get_weworkremotely_offers()
    remoteokio = get_remoteokio_offers()
    githubjobs = get_githubjobs_offers()

    raw_offers = remoteio + workingnomads + weworkremotely + remoteokio + githubjobs

    offers = []
    for offer in raw_offers:
        offers.append(
            f'Role: *{offer.get("title")}* \n'
            f'Company: {offer.get("company")} \n'
            f'Date: {offer.get("date")} \n'
            f'Link: {offer.get("link")} \n'
            f'Location: {offer.get("location")}'
        )

    return offers

def publish_offers(event, context):
    bot = telegram.Bot(token=TOKEN)
    offers = main()

    if len(offers) == 0:
        bot.sendMessage(chat_id=CHAT_ID, text='No new offers.')
    else:
        for o in offers:
            bot.sendMessage(chat_id=CHAT_ID, text=o, parse_mode=telegram.ParseMode.MARKDOWN)        
            time.sleep(5)

    print(f'{len(offers[1:])} offers found and sent at {str(datetime.now().time())}')
