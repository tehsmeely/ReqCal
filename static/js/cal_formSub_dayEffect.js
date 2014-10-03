	$(function(){
		// Form submit, adds hidden element that transfers data of stored date (only if current month)
		$("tbody td").each(function(){
			console.log("foo");
			$(this).click(function(){
				if (!$(this).hasClass("other-month"))
				{
					console.log($(this).text());
					//$('#subform').val({ 'day' : $(this).text(), 'month' : '{{ month }}'});
					$("#submitVal").remove(); // remove previous if extant, necessary if submit is called then back pressed, input will still exist from previous submit
					var input = $("<input>")
						.attr("type", "hidden")
						.attr("id", "submitVal")
						.attr("name", "dayMon").val($(this).text()+"#{{ month }}")
					$('#subform').append($(input));
					$('#subform').submit();
				}
			});
		});
		
		// form submit, for prev and next month arrows
		
		
		
		
		//Set current day
		console.log("{{today}}");
		
		// filters for correct day number and not other month, sets to current day class
		{% if today != None %}
		$('td').filter(function(){
			return $(this).text() == "{{today}}" && !$(this).hasClass("other-month");
			}).addClass("current-day");
		{% endif %}
			
		console.log({{events|safe}});
		var events = {{events|safe}};
		console.log(events['pend'])
		var day;
		for (day in events['pend'])
		{
			var dayNum = events['pend'][day];
			$('td').filter(function(){
			return $(this).text() == dayNum && !$(this).hasClass("other-month");
			}).addClass("pend");
		}
		for (day in events['conf'])
		{
			var dayNum = events['conf'][day];
			$('td').filter(function(){
			return $(this).text() == dayNum && !$(this).hasClass("other-month");
			}).addClass("event");
		}
		
	});