from flask import Blueprint
from flasgger import swag_from
from controllers.article_reaction_controller import ArticleReactionController
from utils.auth_decorators import user_required

reaction_bp = Blueprint("reactions", __name__)
reaction_controller = ArticleReactionController()

# ---------- React to an article ----------
@reaction_bp.route("/api/reactions/<int:article_id>/<string:reaction_type>", methods=["POST"])
@user_required
@swag_from("../docs/reactions/react_to_article.yml")
def react_to_article(article_id, reaction_type):
    return reaction_controller.react_to_article(article_id, reaction_type)

# ---------- Get all user reactions ----------
@reaction_bp.route("/api/reactions", methods=["GET"])
@user_required
@swag_from("../docs/reactions/get_user_reactions.yml")
def get_user_reactions():
    return reaction_controller.get_user_reactions()
