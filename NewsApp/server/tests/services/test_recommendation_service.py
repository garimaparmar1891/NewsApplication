import pytest
from services.recommendation_service import RecommendationService

class DummyProfileLoader:
    def load(self, user_id):
        return {'id': user_id}

class DummyScorer:
    @staticmethod
    def default_strategies():
        return ['dummy']
    @staticmethod
    def score(article, user_profile, strategies):
        return article.get('score', 0)

@pytest.fixture
def service(monkeypatch):
    s = RecommendationService()
    monkeypatch.setattr(s, 'profile_loader', DummyProfileLoader())
    monkeypatch.setattr(s, 'scoring_strategies', DummyScorer.default_strategies())
    monkeypatch.setattr('services.recommendation_service.ArticleScorer', DummyScorer)
    return s

def test_score_and_sort_articles_returns_sorted(service):
    articles = [{'id': 1, 'score': 2}, {'id': 2, 'score': 5}]
    result = service.score_and_sort_articles(1, articles)
    assert result[0]['id'] == 2

def test_score_and_sort_articles_single(service):
    articles = [{'id': 1, 'score': 3}]
    result = service.score_and_sort_articles(1, articles)
    assert result[0]['id'] == 1

def test__score_articles_returns_scores(service):
    articles = [{'id': 1, 'score': 7}]
    user_profile = {'id': 1}
    result = service._score_articles(articles, user_profile)
    assert result[0][0] == 7

def test__score_articles_empty(service):
    user_profile = {'id': 1}
    result = service._score_articles([], user_profile)
    assert result == []

def test__score_articles_single(service):
    articles = [{'id': 2, 'score': 4}]
    user_profile = {'id': 1}
    result = service._score_articles(articles, user_profile)
    assert result[0][1]['id'] == 2

def test__extract_sorted_articles_returns_sorted(service):
    scored = [(5, {'id': 1}), (10, {'id': 2})]
    result = service._extract_sorted_articles(scored)
    assert result[0]['id'] == 2

def test__extract_sorted_articles_empty(service):
    result = service._extract_sorted_articles([])
    assert result == []

def test__extract_sorted_articles_single(service):
    scored = [(3, {'id': 1})]
    result = service._extract_sorted_articles(scored)
    assert result[0]['id'] == 1 