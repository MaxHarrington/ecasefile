function selectCases() {
	arraySelected = new Array;
	$('input:checkbox:checked').each(function () { 
		var checkedBox = $(this).attr('id'); 
		arraySelected.push(checkedBox);
	}); 
	
	$('#id_cases').val(arraySelected); 
	var selectedCasefile = $('select#select-casefile').val();
	document.getElementById("id_title").value = selectedCasefile;
}
