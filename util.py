import string
from collections import Counter

def remove_end_punct(in_string:str) -> str:
    """
    Remove the punctuation at the end of the string.

    :param in_string: input string to remove the punctuation
    """
    
    while in_string != "" and in_string[-1] in string.punctuation:
        in_string = in_string[:-1]

    return in_string.rstrip()

def letter_counter(in_string:str) -> dict:
    """
    Count the number of each letters.

    :param in_string: input string to count the number of letters
    """
    letter_dict = dict(Counter(in_string))
    return letter_dict

def output_format(sent:str,end:bool) -> str :
    """
    Output the sentence with capitalize letter at the beginning or the end of the sentence.

    :param sent: The sentence to be output.
    :param end: Decide where to be capitalized. Default is at the beginning.
    :return: The sentence with the correct capitalization.
    """
    sent = sent.lower()
    if end:
        return sent[:-1].lower() + sent[-1:].capitalize()
    else:
        return sent.capitalize()