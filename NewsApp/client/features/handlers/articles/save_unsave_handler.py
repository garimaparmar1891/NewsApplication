from constants import messages as msg
from features.services.articles.save_unsave_service import ArticleSaveService
from utils.input_utils import get_article_id_input

SAVE_OPERATION = "save"
UNSAVE_OPERATION = "unsave"

class SaveUnsaveHandler:

    @staticmethod
    def save_article():
        try:
            article_id = get_article_id_input(SAVE_OPERATION)
            response = ArticleSaveService.save_article(article_id)
            
            if response.ok:
                print("Article saved successfully.")
                return True
            else:
                return False
                
        except Exception as e:
            return False

    @staticmethod
    def unsave_article():
        try:
            article_id = get_article_id_input(UNSAVE_OPERATION)
            response = ArticleSaveService.unsave_article(article_id)
            
            if response.ok:
                print("Article unsaved successfully.")
                return True
            else:
                return False
                
        except Exception as e:
            return False
