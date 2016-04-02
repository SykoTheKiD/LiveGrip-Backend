<?php
class Push{
    // push message title
    private $title;
     
    // push message payload
    private $message;
     
    // url indicating background task on push received
    private $tickerText;
     
    // url to indicate the type of notification
    private $url;
     
    function __construct() {
         
    }
     
    public function setTitle($title){
        $this->title = $title;
    }
     
    public function setMessage($message){
        $this->message = $message;
    }
     
    public function setTickerText($tickerText){
        $this->tickerText = $tickerText;
    }
     
    public function setUrl($url){
        $this->url = $url;
    }
     
    public function getPush(){
        $res = array();
        $res['title'] = $this->title;
        $res['tickerText'] = $this->tickerText;
        $res['url'] = $this->url;
        $res['message'] = $this->message;
         
        return $res;
    }
}