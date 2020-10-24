var express = require('express');
var app = express();

//TODO: Use a config file for port etc.
var port = 3000;

//TODO: create a class for db communication
var mongoClient = require('mongodb').MongoClient;
var db_url = "mongodb://localhost:27017/";

app.get('/', function(req, res){
    mongoClient.connect(db_url, function(err, dbs){
        
        if (err) throw err;

        var db = dbs.db('TwitterScraper');
        db.collection('tweets').find({}).toArray( function(err, result){
            if(err) throw err;
            res.send(result);
            dbs.close();
        });
    });
});

app.listen(port, function(){
    console.log(`[*] Running on http://localhost:${port}/`);
});