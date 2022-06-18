"""
Author: Ai Chen 21-737-879
Generate an acrostic according to the input text and file
usage: python3 acrosticgenerator.py "YOUR INPUT" filename.txt -e -t "The theme of your poem" -o
sample usage: python3 acrosticgenerator.py "missyou" poetry.txt
"""

from argparse import ArgumentParser
import spacy
import util
import time
import typing
import multiprocessing.pool as mp_pool
import multiprocessing as mp_proc
import itertools


def find_all_lines(letter:str, filename:str, end:bool) -> list:
    """
    Find all the lines that start with the input letter in specified file.

    :param letter: A letter (from the input sentence or word).
    :param filename: The source file name that you want to use 
    :param end: Decide if the input letter is at the beginning of the line or at the end. Default is at the beginning.
    :return: List of sentences that start with given letter.
    """
    if end:
        with open(filename,'r',encoding="utf8") as f:
            sents = [util.remove_end_punct(line.rstrip("\n")) for line in f if (line[-2:-1].lower() == letter.lower())]
        # raise warning if no sentence meet the requirement
        if len(sents) == 0:
            print(f"Warning: There is no line in the file ends with '{letter}'")
    else:
        with open(filename,'r',encoding="utf8") as f:
            # ignore case
            sents = [util.remove_end_punct(line.rstrip("\n"))  for line in f if line.lower().startswith(letter.lower())]
        # raise warning if no sentence meet the requirement
        if len(sents) == 0:
            print(f"Warning: There is no line in the file starts with '{letter}'")
    return sents


def sent_similarity(spacy_nlp:typing.Callable, spacy_theme_doc:spacy.Language, sub_sent:str) -> tuple:
    """
    Calculate the similarity of two sentence using spacy.

    :param theme: A sentence or word as the topic of your acrostic.
    :param subsent: The sentence to be compared with the theme.
    :return: A tuple of the sentence and the similarity score.
    """
    doc2 = spacy_nlp(sub_sent)
    result = spacy_theme_doc.similarity(doc2)
    return sub_sent, result


def worker(args_list:list):
    """
    This function compares the theme and the sentences and scores each pair. It takes a list of agruments
    that are unpacked to use this function in a multiprocessing pool for parallelization of work.

    :params args_list: list with spacy_nlp, space_theme_doc, part of all_sent_list and a counter
    """
    spacy_nlp = args_list[0]
    spacy_theme_doc = args_list[1]
    interval_sent_list = args_list[2]
    sent_score_list = [sent_similarity(spacy_nlp, spacy_theme_doc, sent) for sent in interval_sent_list]
    return sent_score_list


def output_sent_list(proc_pool:mp_pool.Pool, spacy_nlp:typing.Callable, spacy_theme_doc:spacy.Language, all_sent_list:list, n:int)->list:
    """
    Decide the output list for each letter and avoid printing the same sentence more than once.

    :param proc_pool: for multiprocessing.
    :param spacy_nlp: spacy_nlp = spacy.load("en_core_web_md"), so that the module will only be loaded when the function is called.
    :param spacy_theme_doc: spacy_theme_doc = spacy_nlp(theme), so that spaCy only processes the theme sentence only once, instead of every time calculating the similarity.
    :param all_sent_list: All the lines that start with the input letter in specified file.
    :param n: The number of times that a letter appears in the input string. E.g. for the string "eeee", e appears 4 times, so n = 4
    :return: A list of sentences that start or end with given letter and match the theme best.
    """
    sent_score_list = []
    start = time.perf_counter()
    
    # This part is for multiprocessing 
    interval = 1000
    if len(all_sent_list) < interval:
        sent_score_list = worker((spacy_nlp, spacy_theme_doc, all_sent_list, 0,))
    else:
        interval_begin = 0
        interval_end = interval
        input = []
        counter = 0
        while True:
            interval_list = all_sent_list[interval_begin:interval_end]
            if interval_list == []:
                break
            input.append((spacy_nlp, spacy_theme_doc, interval_list, counter))
            counter += 1
            interval_begin = interval_end
            interval_end += interval

        result = proc_pool.map(worker, input)
        sent_score_list = list(itertools.chain.from_iterable(result))
    
    # Visualising the process, especially for the case when a large file is being processed
    stop = time.perf_counter()
    print("##############################", n, stop-start)

    output_sent_list = sorted(sent_score_list, key=lambda item: item[1],reverse=True)
    output_sent_list = [sent[0] for sent in output_sent_list]
    output_sent_list = output_sent_list[0:n]
    
    return output_sent_list
    

def get_argument_parser() -> ArgumentParser:   
    parser = ArgumentParser(description="")
    parser.add_argument('in_word', help="Type sentence only with latin letter,e.g.'missyou'")
    parser.add_argument("file", help="Sourse file to be used to generate the acrostic")
    parser.add_argument("--end",'-e',action="store_true",help="Acrostic at the end")
    parser.add_argument("--theme","-t",type = str, default ="I love you" ,help="the theme of your acrostic,should be a string,e.g.'I love you'")
    parser.add_argument("--output","-o",action="store_true",help="If you want to output the text file, type '-o'")

    return parser


def final_output(in_word:str,theme:str,end:bool,filename:str) -> list:
    """
    Get the list of sentences for acrostic by combining the results of other functions.
    
    :param in_word: The word that you want to hide at the beginning or the end of your acrostic.
    :param theme: A sentence or word as the topic of your acrostic
    :param file: The source file that you want to use 
    :param end: Decide if input letter is at the beginning or at the end of the line. Default is at the beginning.
    :return: List of sentences that will be shown in the output.
    """
    # Load spaCy
    spacy_nlp = spacy.load("en_core_web_md")
    # For similarity calculation
    spacy_theme_doc = spacy_nlp(theme)
    letter_sent_dict = {}
    letter_dict = util.letter_counter(in_word.lower())
    proc_pool = mp_pool.Pool(processes=mp_proc.cpu_count())

    # For each letter in the letter-sentence ditcionary, the value of this letter will be sentence(s), and it is the number of this letter in in_word
    for letter in letter_dict.keys():
        all_line_list = find_all_lines(letter, filename, end)
        letter_sent_dict[letter] = output_sent_list(proc_pool, spacy_nlp, spacy_theme_doc, all_line_list, letter_dict[letter])

    final_output_list = []

    for letter in in_word.replace(" ","").lower():
        # append the sentence in the final list and then delete it
        final_output_list.append(letter_sent_dict[letter].pop(0))

    return final_output_list

def output_file(in_word:str, result:list, end:bool):
    """
    Output a text file of the final result.

    :param in_word: The word that you want to hide at the beginning or the end of your acrostic.
    :param result: The final output list as the result from the function final_output().
    """
    # The name of the output file
    out_file_name = in_word + "acrostic.txt"

    with open(out_file_name,"w", encoding="utf8") as out_file:
            for sent in result:
                # Each line will be put into the correct format before being written in the file, and newline follows
                output_line = util.output_format(sent,end) + "\n"
                out_file.write(output_line)

def main():
    parser = get_argument_parser()
    args = parser.parse_args()
    
    in_word = args.in_word
    theme = args.theme
    end = args.end
    file = args.file
    output = args.output

    result = final_output(in_word,theme,end,file)
    
    # Print the result in terminal
    for line in result:
        print(util.output_format(line,end))
    
    if output:
        output_file(in_word, result, end)

        
if __name__ == "__main__":
    main()

