def problem_url2slug(url: str) -> str:
    # Extract the path, remove trailing slashes, and split by '/'
    path_parts = url.strip('/').split('/')
    
    # Look for the 'problems' segment and return the next part
    if 'problems' in path_parts:
        index = path_parts.index('problems')
        if index + 1 < len(path_parts):
            return path_parts[index + 1]
    
    # If not matched above, return empty string
    print(f"No slug found for url: {url}")
    return ''


def tutorial_url2slug(url):
    """
    Supports GFG, YouTube
    """
    slug = ""
    if "geeksforgeeks.org" in url:
        slug = url.strip("/").split("/")[-1]
        return slug
    elif "youtube.com/watch" in url:
        slug = url.split("watch/?v=")[-1].split("&")[0]
        return slug
    elif "youtube.com/playlist" in url:
        slug = url.split("playlist?list=")[-1].split("&")[0]
        return slug
    print(f"No slug found for url: {url}")
    return slug