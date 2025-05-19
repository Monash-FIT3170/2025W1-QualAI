from pathlib import Path
from moviepy import VideoFileClip

def convert_media(file_path : str) -> str:
    input_path = Path(file_path)
    
    # Check if the file is already an mp3, then just return the same file path
    if input_path.suffix.lower() == '.mp3':
        return input_path
    
    output_path = input_path.with_suffix('.mp3')

    video =  VideoFileClip(str(input_path))
    if video.audio:
        video.audio.write_audiofile(str(output_path))
    else:
        raise ValueError("The video has no audio track.")

    return output_path