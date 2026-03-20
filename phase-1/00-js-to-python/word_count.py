def word_count(my_string):
    words = my_string.split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


print(str(word_count("Hello my name is Bayley! Hello")))
