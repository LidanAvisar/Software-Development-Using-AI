import numpy as np
from ShowSuggesterAI import show_suggester, get_recommendations, cosine_similarity, suggest_closest_matches


def test_show_suggester_valid_matches():
    assert show_suggester("Breaking Bad, Game of Thrones", ["Breaking Bad", "Game of Thrones", "Friends"]) == ["Breaking Bad", "Game of Thrones"]


def test_show_suggester_single_show():
    assert show_suggester("Friends", ["Breaking Bad", "Game of Thrones", "Friends"]) == ["Friends"]


def test_show_suggester_empty():
    assert show_suggester("", ["Breaking Bad", "Game of Thrones", "Friends"]) == []


def test_show_suggester_duplicates():
    assert len(show_suggester("Breaking Bad, Breaking Bad, Game of Thrones", ["Breaking Bad", "Game of Thrones", "Friends"])) == 2


def test_show_suggester_no_comma():
    assert show_suggester("Breaking Bad Game of Thrones", ["Breaking Bad", "Game of Thrones", "Friends"]) == ["Breaking Bad"]


def test_show_suggester_start_with_comma():
    assert show_suggester(",Breaking Bad, Game of Thrones", ["Breaking Bad", "Game of Thrones", "Friends"]) == ["Breaking Bad", "Game of Thrones"]
    assert show_suggester(", Friends", ["Breaking Bad", "Game of Thrones", "Friends"]) == ["Friends"]


def test_show_suggester_end_with_comma():
    assert show_suggester("Breaking Bad, Game of Thrones,", ["Breaking Bad", "Game of Thrones", "Friends"]) == ["Breaking Bad", "Game of Thrones"]
    assert show_suggester("Friends,", ["Breaking Bad", "Game of Thrones", "Friends"]) == ["Friends"]


def test_suggest_closest_matches_exact():
    user_input = "Breaking Bad, Game of Thrones"
    tv_shows_list = ["Breaking Bad", "Game of Thrones", "Westworld"]
    assert suggest_closest_matches(user_input, tv_shows_list) == ["Breaking Bad", "Game of Thrones"]


def test_suggest_closest_matches_partial():
    user_input = "Breaking, Thrones"
    tv_shows_list = ["Breaking Bad", "Game of Thrones", "Westworld"]
    assert suggest_closest_matches(user_input, tv_shows_list) == ["Breaking Bad", "Game of Thrones"]


def test_suggest_closest_matches_none():
    user_input = "Some Random Show"
    tv_shows_list = ["Breaking Bad", "Game of Thrones", "Westworld"]
    assert suggest_closest_matches(user_input, tv_shows_list) == []


def test_show_suggester_partial_matches():
    user_input = "Breaking, Thrones"
    tv_shows_list = ["Breaking Bad", "Game of Thrones", "Westworld"]
    assert show_suggester(user_input, tv_shows_list) == ["Breaking Bad", "Game of Thrones"]


def test_cosine_similarity_identical():
    vec_a = [1, 0, 0]
    assert cosine_similarity(vec_a, vec_a) == 1


def test_cosine_similarity_orthogonal():
    vec_a = [1, 0, 0]
    vec_b = [0, 1, 0]
    assert cosine_similarity(vec_a, vec_b) == 0


def test_cosine_similarity_opposite():
    vec_a = [1, 0, 0]
    vec_b = [-1, 0, 0]
    assert np.isclose(cosine_similarity(vec_a, vec_b), -1)


def test_get_recommendations_basic():
    favorite_shows = ["Breaking Bad"]
    embeddings = {"Breaking Bad": [1, 2, 3], "Game of Thrones": [2, 3, 4], "Westworld": [3, 4, 5]}
    tv_shows_list = ["Breaking Bad", "Game of Thrones", "Westworld"]
    mock_index = None
    recommendations = get_recommendations(favorite_shows, embeddings, mock_index, tv_shows_list)
    assert len(recommendations) == 0


def test_get_recommendations_empty_favorites():
    favorite_shows = []
    embeddings = {"Breaking Bad": [1, 2, 3]}
    tv_shows_list = ["Breaking Bad"]
    mock_index = None
    recommendations = get_recommendations(favorite_shows, embeddings, mock_index, tv_shows_list)
    assert len(recommendations) == 0


def test_get_recommendations_no_matches():
    favorite_shows = ["Unknown Show"]
    embeddings = {"Breaking Bad": [1, 2, 3]}
    tv_shows_list = ["Breaking Bad"]
    mock_index = None
    recommendations = get_recommendations(favorite_shows, embeddings, mock_index, tv_shows_list)
    assert len(recommendations) == 0

