from utils.http_client import HttpClient
from utils.endpoints import REACT_TO_ARTICLE, GET_USER_REACTIONS, DELETE_REACTION

class ArticleReactionsService:
    @staticmethod
    def react_to_article(article_id, reaction):
        return HttpClient.authorized_request("POST", REACT_TO_ARTICLE.format(article_id=article_id, reaction=reaction))

    @staticmethod
    def get_user_reactions():
        return HttpClient.authorized_request("GET", GET_USER_REACTIONS)

    @staticmethod
    def delete_reaction(article_id):
        return HttpClient.authorized_request("DELETE", DELETE_REACTION.format(article_id=article_id)) 