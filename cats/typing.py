"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    count = -1    # Beginning count at -1 --> Since k = 0 can be the first condition
    for para in paragraphs:
        if select(para):
            count += 1
        if count == k:
            return para
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(paragraph) :
        paragraph = remove_punctuation(paragraph)
        paragraph = lower(paragraph)
        paragraph = split(paragraph)

        check = False
        for word in topic:
            if word in paragraph:
                check = True

        return check
    return select

    "*** YOUR CODE HERE ***"
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    count_match = 0
    # total = min(len(typed_words),len(reference_words))

    if len(typed_words) == 0 or len(reference_words) == 0:
        return 0.0
    else:
        for i in range(min(len(typed_words),len(reference_words))):
            if typed_words[i] == reference_words[i]:
                count_match+=1

        return count_match/len(typed_words) * 100
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed)/5)/(elapsed/60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word
    else:
        min_difference_word = min(valid_words,key = lambda word : diff_function(user_word,word,limit))
        if diff_function(user_word,min_difference_word,limit) > limit:
            return user_word
        else:
            return min_difference_word

    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if abs(len(start)-len(goal)) > limit :
        return limit+1
    if limit < 0:
        return 2

    if len(start) == 0 or len(goal) == 0:
            return max(len(start),len(goal))

    if start[0] != goal[0]:
        return 1 + swap_diff(start[1:],goal[1:],limit-1)
    else:
        return 0 + swap_diff(start[1:],goal[1:],limit)

    # def helper(start,goal,counter):
    #     if counter > limit:
    #         return counter

        
    # return helper(start, goal, 0)






    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    

    # if abs(len(start)-len(goal)): # Fill in the condition
    #     # BEGIN
    #     return limit+1
    #     "*** YOUR CODE HERE ***"
    #     # END

    if start == goal :
        return 0       
        
        "*** YOUR CODE HERE ***"
        # END
    if limit < 0:
        return 2
    # elif abs(len(start) - len(goal)) > limit:
    #     return limit + 1 
    elif len(start) == 0 :
       # print('len of goal = ',len(goal))
        return len(goal)
    elif len(goal) == 0:
        return len(start)  

    else:        
        if start[0] != goal[0]:
            substitute_diff = 1+edit_diff(start[1:],goal[1:],limit-1)
            add_diff = 1+edit_diff(start,goal[1:],limit-1)
            remove_diff = 1+edit_diff(start[1:],goal,limit-1)
        else:
            """substitute_diff = 0+edit_diff(start[1:],goal[1:],limit)
                                                add_diff = 0+edit_diff(start,goal[1:],limit)
                                                remove_diff = 0+edit_diff(start[1:],goal,limit)"""
            return edit_diff(start[1:],goal[1:],limit)
        # BEGIN
        "*** YOUR CODE HERE ***"
        #print(add_diff, remove_diff, substitute_diff)

        return min(add_diff,remove_diff,substitute_diff)
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    for i in range(len(typed)):
        if typed[i] != prompt[i]:
            send({'id':id, 'progress':i/len(prompt)})
            print(i/len(prompt))
            return

    send({'id':id, 'progress':len(typed)/len(prompt)})
    print(len(typed)/len(prompt))

    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    lst = [[]]*n_players

    for i in range(1,n_words+1):
        current_word = word(word_times[0][i])
        min_time = 1000
        list_of_lowest_time_players_indexes = []
        for j in range(n_players):
            
            player = word_times[j]

            current_word_time_player = player[i]

            last_word_time_player = player[i-1]

            time_to_type = elapsed_time(current_word_time_player) - elapsed_time(last_word_time_player)

            if time_to_type <= min_time:

                min_time = time_to_type

        for j in range(n_players):
            player = word_times[j]

            current_word_time_player = player[i]

            last_word_time_player = player[i-1]

            time_to_type = elapsed_time(current_word_time_player) - elapsed_time(last_word_time_player)

            if abs(time_to_type - min_time) <= margin:
                list_of_lowest_time_players_indexes.append(j)

                
            #     list_of_lowest_time_players_indexes.append(j)
            

            # el

        for index in list_of_lowest_time_players_indexes:
            lst[index]=lst[index]+[current_word]

        #print(lst)
    return lst

    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)