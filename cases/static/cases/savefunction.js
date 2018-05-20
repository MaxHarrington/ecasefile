arraySelected = new Array;
$('input:checkbox:checked').each(function () { 
	var checkedBox = $(this).attr('id'); 
	arraySelected.push(checkedBox);
}); 

$('#id_cases').val(arraySelected); 

$('#select-casefile').each(function () { 
	var casefileTitle = $(this).attr('id');
});