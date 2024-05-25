def count_anagrams(text, word):
    if not text or not word or len(text) < len(word):
        return 0

    word_len = len(word)
    text_len = len(text)
    word_freq = [0] * 26
    text_freq = [0] * 26

    for char in word:
        word_freq[ord(char) - ord('a')] += 1

    for i in range(word_len):
        text_freq[ord(text[i]) - ord('a')] += 1

    count = 0

    for i in range(word_len, text_len):
        if text_freq == word_freq:
            count += 1

        text_freq[ord(text[i]) - ord('a')] += 1
        text_freq[ord(text[i - word_len]) - ord('a')] -= 1

    if text_freq == word_freq:
        count += 1

    return count
    

'''

#NAIVE SOLUTION:
def count_anagrams(text, word):
    # Function to check if two words are anagrams
    def are_anagrams(w1, w2):
        return sorted(w1) == sorted(w2)

    # Calculate the length of the word and text
    word_length = len(word)
    text_length = len(text)

    # Initialize a counter to keep track of the anagram count
    count = 0

    # If the word is empty, return 0
    if word_length == 0:
        return 0

    # Loop through the text to check for anagrams
    for i in range(text_length - word_length + 1):
        substring = text[i:i + word_length]

        # Check if the substring is an anagram of the word
        if are_anagrams(substring, word):
            count += 1

    return count
'''