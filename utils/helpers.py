def allowed_file(filename, allowed_extensions):
    """
    Check if the filename has an allowed extension.

    :param filename: str, the name of the file to check
    :param allowed_extensions: set, allowed file extensions (e.g. {'png', 'jpg'})
    :return: bool, True if allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
