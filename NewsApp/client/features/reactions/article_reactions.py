from utils.http_client import authorized_request

def react_to_article():
    print("\n--- React to Article ---")
    article_id = input("Enter Article ID: ")
    reaction = input("Enter your reaction (like/dislike): ").strip().lower()
    if reaction not in ["like", "dislike"]:
        print("Invalid reaction. Please enter 'like' or 'dislike'.")
        return
    response = authorized_request("POST", f"/api/reactions/{article_id}/{reaction}")
    if response.ok:
        print("Reaction submitted.")
    else:
        print("Failed to react:", response.json().get("message", response.text))


def get_user_reactions():
    print("\n--- Your Article Reactions ---")
    response = authorized_request("GET", "/api/reactions")
    if response.ok:
        reactions = response.json().get("data", [])
        if not reactions:
            print("You haven't reacted to any articles yet.")
            return
        for idx, r in enumerate(reactions, start=1):
            print(f"\nReaction {idx}:")
            print(f"Article ID : {r.get('ArticleId')}")
            print(f"Reaction   : {r.get('Reaction')}")
            print(f"Reacted At : {r.get('ReactedAt')}")
    else:
        print("Could not fetch reactions:", response.json().get("message", response.text))


def delete_reaction():
    print("\n--- Remove Reaction ---")
    article_id = input("Enter Article ID to remove your reaction: ")
    response = authorized_request("DELETE", f"/api/reactions/{article_id}")
    if response.ok:
        print("Reaction removed.")
    else:
        print("Failed to remove reaction:", response.json().get("message", response.text))
