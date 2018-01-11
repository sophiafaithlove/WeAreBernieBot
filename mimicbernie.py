import tweepy  # https://github.com/tweepy/tweepy
import time
import csv
import json
import random

# Twitter API credentials
consumer_key = "zc5tMUaWOQclhSSE7BqSGMygl"
consumer_secret = "zc5tMUaWOQclhSSE7BqSGMygl"
access_token = "2293759616-GRk6MYT3WNrYWjAw704TUTE1EEzOQRo3aWWlYZb"
access_token_secret = "K8K5zzKQtg3hzYPvvMHqEIUUQ7Yah3uD13JIuBAvaWteZ"


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print ("grabing")
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))


    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass


def login_to_twitter():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    ret = {}
    ret['api'] = api
    ret['auth'] = auth
    return api


def retweet(api, tweet_id):
    success = False
    try:
        a = api.retweet(tweet_id)
        # Sleep for 2 seconds, Thanks Twitter
        print("Sleeping for 5 seconds")
        time.sleep(5)
        success = True
    except tweepy.TweepError as e:
        a = e.response.text
        b = json.loads(a)
        error_code = b['errors'][0]['code']

        if (error_code == 327):
            success = True

    return success


if __name__ == '__main__':
    # pass in the username of the account you want to download
    #get_all_tweets("SenSanders")

    retweet_id = ""
    api = login_to_twitter()
    did = True
    while(True):
        try:
            tweets = api.user_timeline(screen_name="senSanders",count=1)
            new_id = tweets[0].id_str
            if (retweet_id != new_id):
                done = retweet(api,new_id)
                did = done
                if done:
                    retweet_id = tweets[0].id_str
                    print("retweeting...")
            else:
                int = random.randint(1, 6488)
                with open('SenSanders_tweets.csv', 'r') as fd:
                    reader = csv.reader(fd)
                    rows = [r for r in reader]
                    if(int%2 == 1):
                        int += 1
                    text = rows[int]

                    t = ""
                    if(t.__contains__("today") or t.__contains__("time") or t.__contains__("meeting") or t.__contains__("going")):
                        did = False
                        print("again...")
                        continue
                    else:
                        print("tweeting...")
                        tweet_text = text[2][2:-1]+" #WeAreBernieBot"
                        api.update_status(status=tweet_text[2:-1])
                        did = True
            if did:
                time.sleep(60*30)
        except:
            print("error...")
            time.sleep(10*60)



