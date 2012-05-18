window.webtrendsAsyncInit=function(){
    var dcs=new Webtrends.dcs().init({
        dcsid:"dcskwfzfcvz5bdn0s9jvut4xm_7u5b"
        ,domain:"statse.webtrendslive.com"
        ,timezone:-5
        ,offsite:true
        ,download:true
        ,downloadtypes:"xls,doc,pdf,txt,csv,zip,docx,xlsx,rar,gzip"
        ,onsitedoms:"webmaker.org"
        ,plugins:{
            //hm:{src:"//s.webtrends.com/js/webtrends.hm.js"}
        }
        }).track();
};
(function(){
    var s=document.createElement("script"); s.async=true; s.src="/media/js/webtrends.min.js";    
    var s2=document.getElementsByTagName("script")[0]; s2.parentNode.insertBefore(s,s2);
}());