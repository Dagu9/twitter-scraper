var express = require('express');
var app = express();

function escapeRegExp(text) {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
}

//TODO: Use a config file for port etc.
var port = 3000;

var db_name = 'TwitterScraper';
var coll = 'tweets';

var MongoClient = require('mongodb').MongoClient;
var db;

//Initialize a mongodb connection and start the server
MongoClient.connect('mongodb://localhost:27017/', { useUnifiedTopology: true }, function(err, database) {
  if(err) throw err;

  db = database.db(db_name);

  app.listen(port, () => {
    console.log(`[*] Listening on http://localhost:${port}`);
  });

});


// Returns all tweets from a user
app.get('/users/:user/tweets', function(req,res){
    var user = req.params.user;

    db.collection(coll).find({'user':user}).toArray((err, result) => {
        if (err) throw err;
        
        if(result)
            res.json(result);
        else 
            res.end(); 
    });

});

// Return all tweets from a user matching a keyword
app.get('/users/:user/tweets/:keyword', function(req,res){
    var user = req.params.user;
    var keyword = req.params.keyword;
    var re = RegExp(escapeRegExp(keyword));

    db.collection(coll).find({'user':user}).toArray((err, result) => {
        if (err) throw err;
        
        var finalRes = [];
        
        if(result){
            for (var tweet of result){
                if(re.test(tweet["text"])){
                    finalRes.push(tweet);
                }
            }
        } 

        res.json(finalRes);
     
    });
});

// Returns all tweets in db
app.get('/tweets', function(req, res){

    db.collection(coll).find({}).toArray((err, result) => {
        if (err) throw err;
        
        if(result)
            res.json(result);
        else 
            res.end();        
    });
}); 

// Returns all tweets matching a keyword
app.get('/tweets/:keyword', function(req, res){
    var keyword = req.params.keyword;
    var re = RegExp(escapeRegExp(keyword));

    db.collection(coll).find({}).toArray((err, result) => {
        var finalRes = [];
          
        if(result){
            for(var tweet of result){
                if(re.test(tweet["text"])){
                    finalRes.push(tweet);
                }
            }
        }

        res.json(finalRes);
      
    });
});
