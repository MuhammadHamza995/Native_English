# shared/uploads.py

import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

def handle_file_upload(file, allowed_extensions=None):
    """
    Function to handle file uploads, ensuring the file is of the correct type and saving it.
    - file: the file to be uploaded (from request.FILES)
    - allowed_extensions: a list of file extensions that are allowed for upload
    """
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.png', '.jpeg', '.gif', '.pdf', '.txt', '.docx']  # add other extensions as needed

    # Validate file extension
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(f"File type {file_extension} not allowed. Only {', '.join(allowed_extensions)} files are allowed.")

    # Define where to save the file
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    # Save file and return the file URL
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)

    return file_url
