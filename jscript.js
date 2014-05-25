$( document ).ready(function() {
	$("tr").tsort({attr:"significance",order:'desc'});

	$('.showdiff').click(function() {
		var encoded = encodeURIComponent($(this).attr('href'));
		$(this).parent().append($("<div>").load("/cgi-bin/getdiff.py?filename="+encoded));
		$(this).remove();
		return false;
	});
	$('.showfile').click(function() {
		var encoded = encodeURIComponent($(this).attr('href'));
		$(this).parent().append($("<div>").load("/cgi-bin/getfile.py?filename="+encoded));
		$(this).remove();
		return false;
	});
});
