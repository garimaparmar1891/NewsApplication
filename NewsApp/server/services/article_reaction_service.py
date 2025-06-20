from repositories.article_reaction_repository import ArticleReactionRepository


class ArticleReactionService:
    def __init__(self):
        self.repo = ArticleReactionRepository()

    def react_to_article(self, user_id, article_id, reaction_type):
        data = {
            "user_id": user_id,
            "article_id": article_id,
            "reaction_type": reaction_type
        }
        return self.repo.add_or_update_reaction(data)

    def get_user_reactions(self, user_id):
        return self.repo.get_reactions_by_user(user_id)

    def delete_reaction(self, user_id, article_id):
        data = {
            "user_id": user_id,
            "article_id": article_id
        }
        return self.repo.delete_reaction(data)
