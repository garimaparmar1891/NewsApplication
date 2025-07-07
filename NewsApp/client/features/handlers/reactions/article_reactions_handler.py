from features.services.reactions.article_reactions_service import ArticleReactionsService
from utils.input_utils import get_article_id_input
from constants.messages import (
    REACT_TO_ARTICLE_TITLE, USER_REACTIONS_TITLE, REMOVE_REACTION_TITLE,
    REACTION_INVALID, REACTION_PROMPT, REACTION_FAILED,
    REACTIONS_FETCH_FAILED, NO_REACTIONS_FOUND, REACTION_REMOVED,
    REACTION_REMOVE_FAILED, REACTION_DISPLAY_FORMAT, REACTION_SUCCESS
)

class ArticleReactionsHandler:

    @staticmethod
    def react_to_article():
        print(REACT_TO_ARTICLE_TITLE)
        try:
            article_id = ArticleReactionsHandler._get_article_id()
            reaction = ArticleReactionsHandler._get_reaction()
            if not reaction:
                return
            
            response = ArticleReactionsService.react_to_article(article_id, reaction)
            ArticleReactionsHandler._handle_reaction_response(response)
        except Exception as e:
            print(f"Error occurred while reacting to article: {str(e)}")

    @staticmethod
    def get_user_reactions():
        print(USER_REACTIONS_TITLE)
        try:
            response = ArticleReactionsService.get_user_reactions()
            ArticleReactionsHandler._handle_reactions_display(response)
        except Exception as e:
            print(f"Error occurred while fetching user reactions: {str(e)}")

    @staticmethod
    def delete_reaction():
        print(REMOVE_REACTION_TITLE)
        try:
            article_id = ArticleReactionsHandler._get_article_id(" to remove your reaction")
            response = ArticleReactionsService.delete_reaction(article_id)
            ArticleReactionsHandler._handle_delete_response(response)
        except Exception as e:
            print(f"Error occurred while deleting reaction: {str(e)}")

    @staticmethod
    def _get_reaction():
        try:
            reaction = input(REACTION_PROMPT).strip().lower()
            if reaction not in ["like", "dislike"]:
                print(REACTION_INVALID)
                return None
            return reaction
        except Exception as e:
            print(f"Error occurred while getting reaction input: {str(e)}")
            return None

    @staticmethod
    def _get_article_id(action=""):
        try:
            return get_article_id_input(action)
        except Exception as e:
            print(f"Error occurred while getting article ID: {str(e)}")
            return None

    @staticmethod
    def _handle_reaction_response(response):
        try:
            if response.ok:
                print(REACTION_SUCCESS)
            else:
                error_msg = response.json().get("error", response.text)
                print(REACTION_FAILED.format(error_msg))
        except Exception as e:
            print(f"Error occurred while handling reaction response: {str(e)}")

    @staticmethod
    def _handle_reactions_display(response):
        try:
            if response.ok:
                reactions = response.json().get("data", [])
                if not reactions:
                    print(NO_REACTIONS_FOUND)
                    return
                for idx, reaction in enumerate(reactions, start=1):
                    print(REACTION_DISPLAY_FORMAT.format(
                        idx=idx,
                        article_id=reaction.get('ArticleId'),
                        reaction=reaction.get('Reaction'),
                        reacted_at=reaction.get('ReactedAt')
                    ))
            else:
                error_msg = response.json().get("message", response.text)
                print(REACTIONS_FETCH_FAILED.format(error_msg))
        except Exception as e:
            print(f"Error occurred while handling reactions display: {str(e)}")

    @staticmethod
    def _handle_delete_response(response):
        try:
            if response.ok:
                print(REACTION_REMOVED)
            else:
                error_msg = response.json().get("message", response.text)
                print(REACTION_REMOVE_FAILED.format(error_msg))
        except Exception as e:
            print(f"Error occurred while handling delete response: {str(e)}")
