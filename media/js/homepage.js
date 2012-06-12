$(function() {
	$(".tweet").tweet({
          join_text: "auto",
          username: "mozilla",
          count: 1,
          auto_join_text_default: "we said,",
          auto_join_text_ed: "we",
          auto_join_text_ing: "we were",
          auto_join_text_reply: "we replied",
          auto_join_text_url: "we were checking out",
          loading_text: "loading tweets...",
          template: "<p>{text}</p>{time}"
     });
     $('.carousel').carousel({
          interval: false
     });
     $('input#email').focus(function() {
          $(this).next('div').slideDown();
     });
});