from utils.http_client import HttpClient
from utils.endpoints import REACT_TO_ARTICLE, GET_USER_REACTIONS, DELETE_REACTION

class ArticleReactionsService:

    @staticmethod
    def react_to_article(article_id, reaction):
        endpoint = REACT_TO_ARTICLE.format(article_id=article_id, reaction=reaction)
        return HttpClient.authorized_request("POST", endpoint)

    @staticmethod
    def get_user_reactions():
        return HttpClient.authorized_request("GET", GET_USER_REACTIONS)

    @staticmethod
    def delete_reaction(article_id):
        endpoint = DELETE_REACTION.format(article_id=article_id)
        return HttpClient.authorized_request("DELETE", endpoint)
