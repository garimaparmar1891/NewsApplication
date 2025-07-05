from .article_reactions_service import ArticleReactionsService

class ArticleReactionsManager:
    """Handles article reactions (like, dislike, remove, view)."""

    @staticmethod
    def react_to_article():
        print("\n--- React to Article ---")
        article_id = ArticleReactionsManager.prompt_article_id()
        reaction = ArticleReactionsManager.prompt_reaction()
        if not reaction:
            return
        response = ArticleReactionsService.react_to_article(article_id, reaction)
        ArticleReactionsManager.print_react_to_article_status(response)

    @staticmethod
    def prompt_reaction():
        reaction = input("Enter your reaction (like/dislike): ").strip().lower()
        if reaction not in ["like", "dislike"]:
            print("Invalid reaction. Please enter 'like' or 'dislike'.")
            return None
        return reaction

    @staticmethod
    def print_react_to_article_status(response):
        if response.ok:
            print("Reaction submitted.")
        else:
            print("Failed to react:", response.json().get("message", response.text))

    @staticmethod
    def get_user_reactions():
        print("\n--- Your Article Reactions ---")
        response = ArticleReactionsService.get_user_reactions()
        ArticleReactionsManager.print_user_reactions_status(response)

    @staticmethod
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

    @staticmethod
    def delete_reaction():
        print("\n--- Remove Reaction ---")
        article_id = ArticleReactionsManager.prompt_article_id(" to remove your reaction")
        response = ArticleReactionsService.delete_reaction(article_id)
        ArticleReactionsManager.print_delete_reaction_status(response)

    @staticmethod
    def prompt_article_id(action=""):
        return input(f"Enter Article ID{action}: ").strip()

    @staticmethod
    def print_delete_reaction_status(response):
        if response.ok:
            print("Reaction removed.")
        else:
            print("Failed to remove reaction:", response.json().get("message", response.text))