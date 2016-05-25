$(document).ready(function(){
	if ($('.open').first().attr('fileType') == 'other') {
		$('.preview_file').attr('src', "http://www.googledrive.com/host/"+$('.open').first().attr('value'))
	} else {
		$('.preview_file').attr('src', $('.open').first().attr('value'))
	}
	$('.open').click(function(){
		$('#nopreview').empty()
		if ($(this).attr('fileType') == 'other'){
			$('.preview_file').attr('src', "http://www.googledrive.com/host/"+$(this).attr('value'))
		} else {
			$('.preview_file').attr('src', $(this).attr('value'))
		}
	});
});