from utils.http_client import authorized_request

def save_article():
    print("\n--- Save Article ---")
    article_id = input("Enter Article ID to save: ")

    response = authorized_request("POST", f"/api/articles/{article_id}/save")

    if response.ok:
        print("Article saved successfully.")
    else:
        print("Failed to save article:", response.json().get("message", response.text))


def unsave_article():
    print("\n--- Unsave Article ---")
    article_id = input("Enter Article ID to unsave: ")

    response = authorized_request("DELETE", f"/api/articles/{article_id}/unsave")

    if response.ok:
        print("Article unsaved successfully.")
    else:
        print("Failed to unsave article:", response.json().get("message", response.text))
