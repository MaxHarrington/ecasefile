import mammoth
import os
from ecasefile.settings import MEDIA_ROOT

def convert_docx(file):
	file_location = file.split('/media/')
	file = MEDIA_ROOT + file_location[1]

	with open(file, "rb") as docx_file:
		result = mammoth.convert_to_html(docx_file)
		html = result.value # The generated HTML
		messages = result.messages # Any messages, such as warnings during conversion
		os.remove(file) # Deletes the file from the drive after reading it

		return html, messages
