    var redis = require("redis");
    var client = redis.createClient('6379','redis');
    const { check, validationResult } = require('express-validator');
    const express = require('express');
    const zerorpc = require("zerorpc");
    const idLength = 10;
    const app = express();

//    const MQclient = new zerorpc.Client();
//    MQclient.connect("tcp://python:4242");
    function connectMQ(){
      const clientName = new zerorpc.Client();
      clientName.connect("tcp://python:4242");
      return clientName;
    }
    const MQclient = connectMQ();

    var bodyParser = require("body-parser");
    app.use(bodyParser.urlencoded({ extended: false }));
    app.use(express.static(__dirname + '/html-files/'));
    app.use(bodyParser.urlencoded({extend:true}));
    app.engine('html', require('ejs').renderFile);
    app.set('view engine', 'html');
    app.set('views', __dirname);

    function makeid(length) {
       var result           = '';
       var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
       var charactersLength = characters.length;
       for ( var i = 0; i < length; i++ ) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength));
       }
       return result;
    }

    function displayResults (ticketNumber, requestID, res){
                client.lrange(requestID, 0, 1, (error, rep)=> {
                console.log(rep);
                    if (rep[0] == "True"){
                          outcomeOfCheck = "Congratulations, your ticket was lucky! You have won: " + + rep[1] +"$";
                          res.render("html-files/results.html", {outcomeOfCheck:outcomeOfCheck, ticketNumber:ticketNumber});
                    }
                    else if (rep[0] == "Null" || rep[1] == "Null"){
                          res.render("html-files/results.html", {outcomeOfCheck:"The ticket does not exist..", ticketNumber:ticketNumber});
                    }
                    else{
                          res.render("html-files/results.html", {outcomeOfCheck:"Your ticket didn't win anything.. Please buy another ticket", ticketNumber:ticketNumber});
                    }
            });
        }

    function CheckTicket(req, res, ticketNumber) {
        var response = "";
        var requestID = makeid(idLength)+(Math.floor(new Date() / 1000));
        console.log('Was entered ' + ticketNumber );
        message = requestID+":"+ticketNumber;
        MQclient.invoke("checkTicket", message, function(error, resp, more) {
            console.log("Message " +message+ " sent: " + resp);
            if (resp=="ACK"){
                displayResults(ticketNumber, requestID, res);
            }
            else if (resp="undefined"){
                const MQclient = connectMQ();
            }
        });
   }

    function displayNewTicket (newTicketNumber, name, surname, res){
        console.log(newTicketNumber);
        console.log(name);
        console.log(surname);
        res.render("html-files/new-ticket.html", {name:name, surname:surname, newTicketNumber:newTicketNumber});
    }



    app.get('/', function (req, res) {
        res.sendFile('/usr/app/html-files/index.html');
    });

    app.post('/check-ticket', [check("ticketNumberForm").isLength({min: 7, max: 7})], (req, res) => {
        const errors = validationResult(req);
        var ticketNumber = req.body.ticketNumberForm;
        if (!errors.isEmpty()){
            res.sendFile("/usr/app/html-files/check-error.html")
            console.log("Wrong input:" + ticketNumber);
        }
        else{
            CheckTicket(req, res, ticketNumber);
        }
    });

    app.get('/check', function (req, res) {
        res.sendFile("/usr/app/html-files/check.html");
    });

    app.get('/buy', function (req, res) {
        res.sendFile("/usr/app/html-files/buy.html");
    });

    app.post('/buy-ticket', [
        check("buyerNameForm").isLength({min: 2}),
        check("buyerSurnameForm").isLength({min: 2}),
        check("buyerEmailForm").isEmail()
        ], (req, res) => {
        const errors = validationResult(req);
        var buyerName = req.body.buyerNameForm;
        var buyerSurname = req.body.buyerSurnameForm;
        var buyerEmail = req.body.buyerEmailForm;
        if (!errors.isEmpty()){
            res.sendFile("/usr/app/html-files/buy-error.html")
        }
        else{
            var newTicketNumber
            console.log(buyerName);
            console.log(buyerSurname);
            console.log(buyerEmail);
            message = buyerName + ";" + buyerSurname + ";" + buyerEmail;
            MQclient.invoke("buyTicket", message, function(error, resp, more) {
                console.log("Message " +message+ " sent: " + resp);
                newTicketNumber = resp;
                displayNewTicket (newTicketNumber, buyerName, buyerSurname, res);
        });
        }
    });

    app.get('/about', function (req, res) {
        res.sendFile("/usr/app/html-files/about.html");
    });

    app.listen(8080, () => {
      console.log('Listening on port 8080');

    });

