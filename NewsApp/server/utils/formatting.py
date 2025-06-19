def format_article_row(row):
    return {
        "Id": getattr(row, "Id", None),
        "Title": getattr(row, "Title", ""),
        "Content": getattr(row, "Content", ""),
        "Source": getattr(row, "Source", ""),
        "Url": getattr(row, "Url", ""),
        "Category": getattr(row, "Category", ""),
        "PublishedAt": row.PublishedAt.strftime("%Y-%m-%d %H:%M") if row.PublishedAt else ""
    }
