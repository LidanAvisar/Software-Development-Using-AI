import logging
import time
import word_tools


def test_empty_text():
    assert word_tools.count_anagrams("", "abc") == 0


def test_empty_word():
    assert word_tools.count_anagrams("abc", "") == 0


def test_empty_word_and_text():
    assert word_tools.count_anagrams("", "") == 0


def test_eql_text():
    assert word_tools.count_anagrams("abc", "abc") == 1


def test_word_longer_than_text():
    assert word_tools.count_anagrams("a", "abc") == 0


def test_word_as_is_in_text():
    assert word_tools.count_anagrams("ba", "a") == 1


def test_word_permutation_in_text():
    assert word_tools.count_anagrams("for", "of") == 1


def test_word_not_in_order():
    assert word_tools.count_anagrams("orf", "of") == 0


def test_text_is_palindrome():
    assert word_tools.count_anagrams("fof", "of") == 2


def test_word_is_palindrome():
    assert word_tools.count_anagrams("fofoff", "fof") == 3


def test_word_contained_in_text():
    assert word_tools.count_anagrams("forfo", "for") == 3


def test_time_count_anagrams_performance():
    logging.basicConfig(level=logging.INFO, force=True)
    long_text = "a" * 1000 + "b" * 1000 + "c" * 1000 
    word = "abc"
    
    start_time = time.time()

    # Running the function 10,000 times in a loop
    for _ in range(1000):
        word_tools.count_anagrams(long_text, word)

    end_time = time.time()

    # Calculate the time taken in milliseconds
    time_taken_ms = (end_time - start_time) * 1000
    logging.info(f"Time taken: {time_taken_ms} ms")

    assert time_taken_ms < 1000


test_time_count_anagrams_performance()






    
    

