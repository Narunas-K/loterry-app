import time
from redis import StrictRedis

redisHost = "redis"
redisPort = 6379
redis = StrictRedis(host=redisHost, port=redisPort)

def main():
    # Subscrive to redis keyspace events
    pubsub = redis.pubsub()
    pubsub.psubscribe('__keyspace@0__:*')

    while True:
        message = pubsub.get_message()
        if message != None:
            print(message)
            try:
                if str(message["data"])=="b'set'":
                    messageList = (message["channel"].decode("utf-8")).split(":")

                    key = messageList[1]
                    print(redis.get(key))
                    print ("SET")
            except:
                print ("Exception")


if __name__== "__main__":
  main()