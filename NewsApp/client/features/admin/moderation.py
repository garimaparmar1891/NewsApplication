from utils.http_client import authorized_request
from utils.endpoints import (
    GET_REPORTS,
    HIDE_UNHIDE_ARTICLE,
    HIDE_UNHIDE_CATEGORY
)

def view_reported_articles():
    response = authorized_request("GET", GET_REPORTS)
    if not response.ok:
        print("Failed to fetch reports:", response.text)
        return

    reports = response.json().get("data", [])
    if not reports:
        print("No reports found.")
        return

    for report in reports:
        print(f"\nArticle ID: {report['ArticleId']}")
        print(f"Reported By: {report['UserId']}")
        print(f"Reason: {report['Reason']}")
        print("-" * 40)

def hide_unhide_entity(entity_type):
    entity_id = input(f"Enter {entity_type.capitalize()} ID: ").strip()
    action = input(f"Do you want to 'hide' or 'unhide' the {entity_type}? ").lower().strip()
    if action not in ("hide", "unhide"):
        print("Invalid action.")
        return

    if entity_type == "article":
        endpoint = HIDE_UNHIDE_ARTICLE.format(article_id=entity_id, action=action)
    else:
        endpoint = HIDE_UNHIDE_CATEGORY.format(category_id=entity_id, action=action)

    response = authorized_request("PATCH", endpoint)
    if response.ok:
        print("Success.")
    else:
        print("Failed:", response.text)

def hide_unhide_article():
    hide_unhide_entity("article")

def hide_unhide_category():
    hide_unhide_entity("category")