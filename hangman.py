import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)



def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for char in secret_word:
        if char not in letters_guessed:
            guessed_word += '_ '
        else:
            guessed_word += char
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ''
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters



def check_valid_input(user_guess, letters_guessed):
    '''
    user_guess: the input from the user
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: boolean, True if the input is valid; otherwise False
    A valid input is:
        a single char
        an alphabet letter and not any other symbol
        not a letter the user has already previously input
    '''
    if len(user_guess) == 0 or len(user_guess) > 1:
        print('Oops! That is not a valid letter.')
        return False
    elif not user_guess.isalpha():
        print('Oops! That is not a valid letter.')
        return False
    elif user_guess in letters_guessed:
        print('Oops! You already previously guessed that letter')
        return False
    else:
        return True



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with hidden letter (_ ) characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the hidden letter symbol
        _ , and the hidden letter (_ ) is also not one of the letters in the word that
        has already been revealed, and my_word and other_word are of the same length;
        False otherwise:
    '''
    my_word = my_word.replace(' ','')
    if len(my_word) != len(other_word):
        return False
    else:
        for i in range(len(my_word)):
            if my_word[i] != '_' and my_word[i] != other_word[i]:
                return False
            elif my_word[i] == '_' and other_word[i] in my_word:
                return False
            else:
                continue
        return True



def show_possible_matches(my_word):
    '''
    my_word: string with '_ ' characters, current guess of secret word
    word_matches: list, this function creates a list of every word in the wordlist
      that matches my_word.
    returns: string, all the words in the word_matches list joined together
    '''
    word_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            word_matches.append(word)
    return ' '.join(word_matches)



def calculate_score(secret_word, guesses_remaining):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    Calculates the user's score by multiplying their number of guesses
      remaining by the amount of unique letters in the secret word
    returns: int, a score reflecting how well the user did
    '''
    unique_letters = []
    for char in secret_word:
        if char not in unique_letters:
            unique_letters.append(char)

    return guesses_remaining * len(unique_letters)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, lets the user know how many
      letters the secret_word contains and how many guesses they start with.

    * The user starts with 6 guesses

    * Before each round, displays to the user how many guesses
      they have left and the letters that the user has not yet guessed.

    * Asks the user to supply one guess per round. User receives a warning if
      they input an invalid string.

    * The user can receive up to 3 warnings, afterwards they start losing
      guesses if they input invalid strings,

    * The user receives feedback after each guess
      about whether their guess appears in the computer's word.

    * After each guess, displays to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.
    '''

    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    can_receive_hints = False
    received_hint_notication = False
    guessed_vowels = 0
    guessed_consonants = 0

    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print('-------------')

    while guessed_word != secret_word and guesses_remaining > 0:
        print(f'You have {guesses_remaining} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')
        if can_receive_hints and not received_hint_notication:
            print(f'Well done! You have correctly guessed {guessed_vowels + guessed_consonants} letters so far, you can now type in an asterisk (*) to receive hints!')
            received_hint_notication = True
        elif can_receive_hints:
            print('You can type in an asterisk (*) to receive hints.')

        user_guess = (input('Please guess a letter: ')).lower()

        if user_guess == '*' and can_receive_hints:
            print('-------------')
            print(f'Possible matches for your guessed letters so far are:\n{show_possible_matches(get_guessed_word(secret_word, letters_guessed))}')
        elif check_valid_input(user_guess, letters_guessed):
            letters_guessed.append(user_guess)
            if user_guess in secret_word:
                guessed_word = get_guessed_word(secret_word, letters_guessed)
                print(f'Good guess: {guessed_word}')
                if user_guess in 'aeiou':
                    guessed_vowels += 1
                else:
                    guessed_consonants += 1
                if guessed_vowels > 0 and guessed_consonants > 0:
                    can_receive_hints = True
            else:
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
                guesses_remaining -= 1
        else:
            if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(f'You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                guesses_remaining -= 1
                print(f'You are out of warnings. You now have {guesses_remaining} guesses left: {get_guessed_word(secret_word, letters_guessed)}')

        print('-------------')

    if guesses_remaining < 1:
        print('Sorry, you ran out of guesses and lost!')
        print('The secret word is', secret_word)
    else:
        print('Congratulations, you won!')
        print('Your total score for this game is:', calculate_score(secret_word, guesses_remaining))



if __name__ == "__main__":
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
