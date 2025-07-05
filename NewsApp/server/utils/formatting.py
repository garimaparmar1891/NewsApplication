from datetime import datetime

def safe_get(row, key, default=""):
    return row.get(key, default) if isinstance(row, dict) else getattr(row, key, default)

def format_article_row(row):
    published_at = safe_get(row, "PublishedAt")
    if published_at:
        if isinstance(published_at, datetime):
            published_at_str = published_at.strftime("%Y-%m-%d %H:%M")
        else:
            published_at_str = str(published_at)
    else:
        published_at_str = ""
    
    return {
        "Id": safe_get(row, "Id"),
        "Title": safe_get(row, "Title"),
        "Content": safe_get(row, "Content"),
        "Source": safe_get(row, "Source"),
        "Url": safe_get(row, "Url"),
        "Category": safe_get(row, "Category"),
        "CategoryId": safe_get(row, "CategoryId"),
        "PublishedAt": published_at_str
    }

def clean_word(word):
    return str(word).strip().lower()
