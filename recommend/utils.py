def get_embed_url(url):
    if "youtube.com/watch?v=" in url:
        video_id = url.split('watch?v=')[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be/" in url:
        video_id = url.split('youtu.be/')[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return url  # Handle other cases if necessary



