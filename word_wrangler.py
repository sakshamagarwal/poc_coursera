"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    
    ans = []
    for element in list1:
        if not element in ans:
            ans.append(element)
    return ans

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    ans = []
    for element in list1:
        if element in list2:
            ans.append(element)
    return ans

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    idx = 0
    jdx = 0
    ans = []
    while (idx < len(list1) and jdx < len(list2)):
        if list1[idx] > list2[jdx]:
            ans.append(list2[jdx])
            jdx += 1
        else:
            ans.append(list1[idx])
            idx += 1
            
    if (idx == len(list1)):
        while (jdx < len(list2)):
            ans.append(list2[jdx])
            jdx += 1
    else:
        while (idx < len(list1)):
            ans.append(list1[idx])
            idx += 1

    return ans
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if (len(list1) > 1):
        part1 = merge_sort(list1[0:len(list1)/2])
        part2 = merge_sort(list1[(len(list1)/2) : len(list1)])
        return merge(part1, part2)
    else:
        return list(list1)

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) >= 2:
        first = word[0]
        rest = word[1:len(word)]
        rest_strings = gen_all_strings(rest)
        ans = []
        for item in rest_strings:
            temp = item
            for position in range(len(item)+1):
                temp_list = list(temp)
                temp_list.insert(position, first)
                ans.append(''.join(temp_list))
        ans = ans + rest_strings
        return ans
    elif len(word) == 1:
        return ['', word]
    else:
        return ['']

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()
#print remove_duplicates([1,2,3,4,4])
#print merge_sort([1,2,37, 4, 7])
#first = 'c'
#print first[0]
#print gen_all_strings('aab')
    
    
