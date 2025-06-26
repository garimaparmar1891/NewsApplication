from utils.http_client import authorized_request
from utils.endpoints import (
    REACT_TO_ARTICLE,
    GET_USER_REACTIONS,
    DELETE_REACTION
)

def react_to_article():
    print("\n--- React to Article ---")
    article_id = prompt_article_id()
    reaction = prompt_reaction()
    if not reaction:
        return
    response = send_react_to_article_request(article_id, reaction)
    print_react_to_article_status(response)

def prompt_reaction():
    reaction = input("Enter your reaction (like/dislike): ").strip().lower()
    if reaction not in ["like", "dislike"]:
        print("Invalid reaction. Please enter 'like' or 'dislike'.")
        return None
    return reaction

def send_react_to_article_request(article_id, reaction):
    return authorized_request("POST", REACT_TO_ARTICLE.format(article_id=article_id, reaction=reaction))

def print_react_to_article_status(response):
    if response.ok:
        print("Reaction submitted.")
    else:
        print("Failed to react:", response.json().get("message", response.text))


def get_user_reactions():
    print("\n--- Your Article Reactions ---")
    response = send_get_user_reactions_request()
    print_user_reactions_status(response)

def send_get_user_reactions_request():
    return authorized_request("GET", GET_USER_REACTIONS)

def print_user_reactions_status(response):
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
    article_id = prompt_article_id(" to remove your reaction")
    response = send_delete_reaction_request(article_id)
    print_delete_reaction_status(response)

def prompt_article_id(action=""):
    return input(f"Enter Article ID{action}: ").strip()

def send_delete_reaction_request(article_id):
    return authorized_request("DELETE", DELETE_REACTION.format(article_id=article_id))

def print_delete_reaction_status(response):
    if response.ok:
        print("Reaction removed.")
    else:
        print("Failed to remove reaction:", response.json().get("message", response.text))
