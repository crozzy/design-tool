$(document).ready(function() {

	$('#main-content').after('<div class="inline-login"></div>');

	$('.inline-login').load('../inc/inline-login.html').dialog({
		width:510,
		autoOpen:false,
		modal:true,
		closeOnEscape: true,
		title: 'Login',
		cache: false
	});
	$('.btn-login').click(function(event){
		$('.inline-login').dialog('open');
		event.preventDefault();
	});

});
