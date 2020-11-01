function showTweets(){
    if(window.XMLHttpRequest){
        xhttp = new XMLHttpRequest();
    } else if(window.ActiveXObject){
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var data = this.response

            var tweets = JSON.parse(data);

            var html = "";
            for(var tweet of tweets){
                html += "<h5>User: "+tweet["user"]+" <br>date: "+new Date(tweet["creation_date"])+" <br>text: "+tweet["text"]+"</h5><br>";
            }

            $("#rootContainer").fadeOut(100, function(){
                $(this).empty();
                $(this).html(html);
            }).fadeIn(500);
        }
    }


    xhttp.open("GET", "/tweets", true);
    xhttp.send();
}
