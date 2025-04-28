def extract_txt(file):
    #extracts a txt file to a string
    if isinstance(file, str):
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()
    if hasattr(file, 'read'):
        return file.read().decode('utf-8') if hasattr(file, 'decode') else file.read()
    raise TypeError("Unsupported file type provided. Must be a path or file-like object.")
def save_file(text:str,location:str):
    #saves a file to 'location' from a string of text
    with open(location, 'w', encoding='utf-8') as f:
        f.write(text)


