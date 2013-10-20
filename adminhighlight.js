//<nowiki>
/**
 * Admin highlighter 2.0
 * ---------------------
 * A jQuery/mediawiki-heavy rewrite of [[User:Amalthea/userhighlighter.js]]
 * 
 * This script highlights links to admins' userpages or talkpages in bodyContent
 * (that is, everything but the tabs, personal links at the top of the screen and sidebar)
 * by giving them a cyan background.
 *
 * See [[User:Theopolisme/Scripts/adminhighlighter]] for more details.
 *
 * @author theopolisme
 */
;(function($, mw){
	$.getJSON(mw.config.get('wgScriptPath')+'/index.php?action=raw&ctype=application/json&title=User:Amalthea_(bot)/userhighlighter.js/sysop.js', function(data){
		ADMINHIGHLIGHT_EXTLINKS = window.ADMINHIGHLIGHT_EXTLINKS || false;
		ADMINHIGHLIGHT_NAMESPACES = [-1,2,3];
		$('#bodyContent a').each(function(index,linkraw){
			try {
				var link = $(linkraw);
				var url = link.attr('href');
				if (!url || url.charAt(0) === '#') return; // Skip <a> elements that aren't actually links; skip anchors
				var uri = new mw.Uri(url);
				if (!ADMINHIGHLIGHT_EXTLINKS && !$.isEmptyObject(uri.query)) return; // Skip links with query strings if highlighting external links is disabled
				if (uri.host == 'en.wikipedia.org') {
					var mwtitle = new mw.Title(mw.util.getParamValue('title',url) || decodeURIComponent(uri.path.slice(6))); // Try to get the title parameter of URL; if not available, remove '/wiki/' and use that
					if ($.inArray(ADMINHIGHLIGHT_NAMESPACES, mwtitle.getNamespaceId())) {
						var user = mwtitle.getMain().replace(/_/g," ");
						if (mwtitle.getNamespaceId() === -1) user = user.replace('Contributions/',''); // For special page "Contributions/<username>"
						if (data[user] == 1) {
							appendCSS(".userhighlighter_sysop {background-color: #00FFFF !important}");
							link.addClass('userhighlighter_sysop'); // Override the above color by using `a.userhighlighter_sysop {background-color: COLOR !important}`
						}
					}
				}
			} catch (e) {
				// Sometimes we will run into unparsable links, so just log these and move on
				window.console && console.error('Admin highlighter recoverable error',e.message);
			}
		});
	});
}(jQuery, mediaWiki));
//</nowiki>
