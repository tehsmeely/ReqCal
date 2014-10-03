
$(function(){
	console.log('ORIDIFY')
	$('#ordify').each(function()
	{
		var number = $(this).text();
		console.log('Ordify internal')
		console.log(number);
		var lastNum = number.slice(-1);
		var ord = 'th';
		// specials are 11, 12, and 13, which are all "th"
		if (number != '11' && number != '12' && number != '13')
		{
			switch(lastNum) {
				case '1':
					ord = 'st';
					break;
				case '2':
					ord = 'nd';
					break;
				case '3':
					ord = 'rd';
			}
		}
		$(this).text(number + ord);
	});

});