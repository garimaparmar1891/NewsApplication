import pytest
from services.scoring import ArticleScorer, UserProfile

def user_profile_stub(**kwargs):
    defaults = {
        'user_id': 1,
        'keywords': [],
        'liked_articles': set(),
        'disliked_articles': set(),
        'saved_articles': set(),
        'read_history': set(),
        'reported_articles': set(),
        'enabled_categories': set()
    }
    defaults.update(kwargs)
    return UserProfile(**defaults)

def test_keyword_scoring_keyword_in_title():
    article = {'Title': 'Python News', 'Content': '', 'Id': 1, 'CategoryId': 1}
    user = user_profile_stub(keywords=['python'])
    assert ArticleScorer._keyword_scoring(article, user) == ArticleScorer.KEYWORD_SCORE

def test_keyword_scoring_no_keyword():
    article = {'Title': 'Java News', 'Content': '', 'Id': 1, 'CategoryId': 1}
    user = user_profile_stub(keywords=['python'])
    assert ArticleScorer._keyword_scoring(article, user) == 0

def test_like_scoring_liked():
    article = {'Id': 1}
    user = user_profile_stub(liked_articles={1})
    assert ArticleScorer._like_scoring(article, user) == ArticleScorer.LIKE_SCORE

def test_like_scoring_not_liked():
    article = {'Id': 2}
    user = user_profile_stub(liked_articles={1})
    assert ArticleScorer._like_scoring(article, user) == 0

def test_dislike_scoring_disliked():
    article = {'Id': 1}
    user = user_profile_stub(disliked_articles={1})
    assert ArticleScorer._dislike_scoring(article, user) == ArticleScorer.DISLIKE_SCORE

def test_dislike_scoring_not_disliked():
    article = {'Id': 2}
    user = user_profile_stub(disliked_articles={1})
    assert ArticleScorer._dislike_scoring(article, user) == 0

def test_save_scoring_saved():
    article = {'Id': 1}
    user = user_profile_stub(saved_articles={1})
    assert ArticleScorer._save_scoring(article, user) == ArticleScorer.SAVE_SCORE

def test_save_scoring_not_saved():
    article = {'Id': 2}
    user = user_profile_stub(saved_articles={1})
    assert ArticleScorer._save_scoring(article, user) == 0

def test_read_scoring_read():
    article = {'Id': 1}
    user = user_profile_stub(read_history={1})
    assert ArticleScorer._read_scoring(article, user) == ArticleScorer.READ_SCORE

def test_read_scoring_not_read():
    article = {'Id': 2}
    user = user_profile_stub(read_history={1})
    assert ArticleScorer._read_scoring(article, user) == 0

def test_report_scoring_reported():
    article = {'Id': 1}
    user = user_profile_stub(reported_articles={1})
    assert ArticleScorer._report_scoring(article, user) == ArticleScorer.REPORT_SCORE

def test_report_scoring_not_reported():
    article = {'Id': 2}
    user = user_profile_stub(reported_articles={1})
    assert ArticleScorer._report_scoring(article, user) == 0

def test_preference_scoring_enabled_category():
    article = {'CategoryId': 1}
    user = user_profile_stub(enabled_categories={1})
    assert ArticleScorer._preference_scoring(article, user) == ArticleScorer.PREFERENCE_SCORE

def test_preference_scoring_disabled_category():
    article = {'CategoryId': 2}
    user = user_profile_stub(enabled_categories={1})
    assert ArticleScorer._preference_scoring(article, user) == 0

def test_score_with_all_strategies_positive():
    article = {'Title': 'Python', 'Content': '', 'Id': 1, 'CategoryId': 1}
    user = user_profile_stub(keywords=['python'], liked_articles={1}, enabled_categories={1})
    strategies = [ArticleScorer._keyword_scoring, ArticleScorer._like_scoring, ArticleScorer._preference_scoring]
    assert ArticleScorer.score(article, user, strategies) == ArticleScorer.KEYWORD_SCORE + ArticleScorer.LIKE_SCORE + ArticleScorer.PREFERENCE_SCORE

def test_score_with_all_strategies_zero():
    article = {'Title': 'Java', 'Content': '', 'Id': 2, 'CategoryId': 2}
    user = user_profile_stub(keywords=['python'], liked_articles={1}, enabled_categories={1})
    strategies = [ArticleScorer._keyword_scoring, ArticleScorer._like_scoring, ArticleScorer._preference_scoring]
    assert ArticleScorer.score(article, user, strategies) == 0

def test_default_strategies_returns_list():
    strategies = ArticleScorer.default_strategies()
    assert isinstance(strategies, list)

def test_default_strategies_length():
    strategies = ArticleScorer.default_strategies()
    assert len(strategies) == 7 