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

function selectAllCases() {
	var allCheckboxes = document.querySelectorAll("input[type=checkbox]");

	for (var i = 0; i < allCheckboxes.length; i++){
		allCheckboxes[i].checked = true;
	}
}

function deselectAllCases() {
	var allCheckboxes = document.querySelectorAll("input[type=checkbox]");

	for (var i = 0; i < allCheckboxes.length; i++){
		allCheckboxes[i].checked = false;
	}
}