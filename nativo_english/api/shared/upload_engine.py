# shared/uploads.py

import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import uuid
def handle_file_upload(file, allowed_extensions=None):
    """
    Function to handle file uploads, ensuring the file is of the correct type and saving it.
    """
    if allowed_extensions is None:
        # Default allowed extensions
        allowed_extensions = ['.jpg', '.png', '.jpeg', '.gif', '.pdf', '.mp4', '.mp3']

    # Validate file extension
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(f"File type {file_extension} not allowed. Only {', '.join(allowed_extensions)} files are allowed.")

    # Generate a unique filename to avoid collisions
    unique_filename = f"{uuid.uuid4().hex}_{file.name}"

    # Define where to save the file
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save(unique_filename, file)
    
    # Generate the URL for accessing the file
    file_url = fs.url(filename)

    return file_url

