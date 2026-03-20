def filter_evens(input):
    new_list = []
    for i in input:
        if i % 2 == 0:
            new_list.append(i)
    return new_list


print(filter_evens([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
