$(window).ready(function() {
	if (jQuery.browser.msie) {
		$(".msie-only").show();
		return;
	}

	var DEFAULT_BROWSER = "firefox";
	var DEFAULT_PLATFORM = "MacIntel";
	var BASE_URL = "http://videos-cdn.mozilla.net/serv/labs/hackasaurus/";
	var videos = {
		MacIntel: {
			chrome: "ToolBar-MacOS-Chrome15.webm",
			firefox: "ToolBar-MacOS-FF7.webm",
			opera: "ToolBar-MacOS-Opera11.52.webm",
			safari: "ToolBar-MacOS-Safari5.1.m4v"
		},
		WinXP: {
			chrome: "ToolBar-XP-Chrome15.webm",
			firefox: "ToolBar-XP-FF7.webm",
			opera: "ToolBar-XP-Opera11.52.webm",
			safari: "ToolBar-XP-Safari5.1.m4v"
		},
		Win7: {
			chrome: "Toolbar-Win7-Chrome15.webm",
			firefox: "Toolbar-Win7-FF7.webm",
			opera: "Toolbar-Win7-Opera11.52.webm",
			safari: "Toolbar-Win7-Safari5.1.m4v"
		}
	};

	var platform = navigator.platform;

	if (navigator.platform.match(/Win/)) {
		// We're some flavor of Windows.
		if (navigator.userAgent.match(/NT 5/)) {
			// We're WinXP/2000.
			platform = "WinXP";
		} else {
			// Assume we're Vista, 7, or higher.
			platform = "Win7";
		}
	}

	if (!(platform in videos))
	platform = DEFAULT_PLATFORM;

	var browser = DEFAULT_BROWSER;

	var vendors = {
		"Apple Computer, Inc.": "safari",
		"Google Inc.": "chrome"
	};

	if (navigator.vendor in vendors)
	browser = vendors[navigator.vendor];

	if (navigator.appName == "Opera")
	browser = "opera";

	var video = $("<video controls></video>");

	video.attr("src", BASE_URL + videos[platform][browser]);
	video.css('width', '100%');

	$("#bookmarks-toolbar-movie").replaceWith(video);
});