import zerorpc
import psycopg2
from redis import StrictRedis
import random

# Redis config vars
redisHost = "redis"
redisPort = 6379
redis = StrictRedis(host=redisHost, port=redisPort)

# Postgres config vars
dbname = "loterry"
user = "postgress"
host = "appdb"
password = "mysecretpassword"
checkResultsQuery = "SELECT win, ammount_of_win from results WHERE ticket_id="
newTicketInsertQuery = "INSERT INTO results (ticket_id, win, ammount_of_Win) VALUES"

def writeToRedis (requestId, win, ammountOfWin):
    redis = StrictRedis(host=redisHost, port=redisPort)
    resultsList = [str(win), str(ammountOfWin)]
    redis.rpush (str(requestId), *resultsList)
    print ("Wrote to redis")

def psqlGetData(ticketNumber):
    try:
        connect_str = "dbname='loterry' user='postgres' host='appdb' " + \
                      "password='mysecretpassword'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        # cursor.execute("""CREATE TABLE tutorials (name char(40));""")
        # run a SELECT statement - no data in there, but we can try it
        # cursor.execute("""SELECT * from results""")
        query = checkResultsQuery+"\'"+ticketNumber+"\'"+";"
        print (query)
        cursor.execute(query)
        conn.commit() # <--- makes sure the change is shown in the database
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("Can't connect. Invalid dbname, user or password?")
        print(e)

def psqlInsertData (ticketNumber, isWin, ammountOfWin):
    try:
        connect_str = "dbname='loterry' user='postgres' host='appdb' " + \
                      "password='mysecretpassword'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        # cursor.execute("""CREATE TABLE tutorials (name char(40));""")
        # run a SELECT statement - no data in there, but we can try it
        # cursor.execute("""SELECT * from results""")
        query = newTicketInsertQuery +"(\'"+ticketNumber+"\',"+isWin +","+ str(ammountOfWin) +");"
        print (query)
        cursor.execute(query)
        conn.commit() # <--- makes sure the change is shown in the database
        cursor.close()
        conn.close()
    except Exception as e:
        print("Can't connect. Invalid dbname, user or password?")
        print(e)

def parseMessage (rawMessage):
    print (len(rawMessage))
    if (len(rawMessage)==28):
        requestId = rawMessage.split(":")[0]
        ticketNumber = rawMessage.split(":")[1]
        ticketList = [requestId, ticketNumber]
        return ticketList
    else:
        print ("Corrupted message received")

def checkTicketInDb (ticketNumber):
    resultsFromDb = psqlGetData(ticketNumber)

    print (resultsFromDb)
    return resultsFromDb

def generateNewTicket():
    newTicketNumber = str(random.randint(1,9999999))
    #Check if new ticket number is number of 7 digits
    newTicketLength = len(newTicketNumber)
    lengthDifference = 7 - newTicketLength
    if (lengthDifference != 0):
        for i in range (lengthDifference):
            newTicketNumber = "0" + newTicketNumber
    return newTicketNumber

def determineLuckyTicket():
    randomNumber = random.randint(1,10)
    if randomNumber <= 3:
        isLucky = "TRUE"
    else:
        isLucky = "FALSE"
    return isLucky


def determineAmountOfWin():
    randomWin = random.randint(1,1000)
    return randomWin

def returnNewTicket ():
    newTicketNumber = generateNewTicket ()
    resultsFromDb = psqlGetData (newTicketNumber)
    print (resultsFromDb)
    #if the ticket number already exists, generate new one
    if (resultsFromDb != []):
        newTicketNumber = returnNewTicket ()
    isLucky = determineLuckyTicket()
    if isLucky == "TRUE":
        amountOfWin = determineAmountOfWin()
    else:
        amountOfWin = 0
    psqlInsertData(newTicketNumber, isLucky, amountOfWin)

    return newTicketNumber

class HelloRPC(object):
    def checkTicket(self, message):
        print ("Message received: " + message)
        parsedTicketList = parseMessage (message)
        requestId = parsedTicketList[0]
        ticketNumber = parsedTicketList[1]
        results = checkTicketInDb (ticketNumber)
        if results != []:
            didTicketWin = results[0][0]
            ammountOfWin = results[0][1]
            writeToRedis(requestId,didTicketWin, ammountOfWin)
        else:
            writeToRedis(requestId, "Null", "Null")

        return "ACK"

    def buyTicket (self, message):
        print ("Message received: " + message)
        newTicketNumber = returnNewTicket()
        return newTicketNumber

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
