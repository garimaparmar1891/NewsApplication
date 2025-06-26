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
        return self.repo.react_to_article(data)

    def get_user_reactions(self, user_id):
        return self.repo.get_user_reactions(user_id)
