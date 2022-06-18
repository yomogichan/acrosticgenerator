# Acrosticgenerator

Acrosticgenerator is used to generate acrostic poem in English.

Acrostic: An acrostic is a poem or other composition in which the first letter (or syllable, or word) of each line (or paragraph, or other recurring feature in the text) spells out a word, message or the alphabet.

Example of Acrostic from  *Edgar Allan Poe*:  
Each letter of *Elizabeth* is hidden at the beginning of lines.
**E**lizabeth it is in vain you say
"**L**ove not" — thou sayest it in so sweet a way:
**I**n vain those words from thee or L.E.L.
**Z**antippe's talents had enforced so well:
**A**h! if that language from thy heart arise,
**B**reath it less gently forth — and veil thine eyes.
**E**ndymion, recollect, when Luna tried
**T**o cure his love — was cured of all beside —
**H**is folly — pride — and passion — for he died.*

## Data
The source file("poetry.txt") in the sample is extracted from:
[A Project Gutenberg Poetry Corpus](https://github.com/aparrish/gutenberg-poetry-corpus) by Allison Parrish.


## Preparation
Before using the python programme, you need to download the following module

```bash
$ pip3 install spacy
$ python3 -m spacy download en_core_web_md
```

## Usage
1. Use command, e.g. *cd* to get into directory with acrosticgenerator.py.

2. Make sure your python version is the same or later than 3.9.7, spaCy Version later than 3.3.0

3. python3 acrosticgenerator.py "YOUR INPUT" filename -e -t "The theme of your poem" -o

### Parameter:  
* "YOUR INPUT": The word that you want to hide at the beginning or the end of the acrostic.  
* filename:The name of input source file, and the file should be in txt format. The lines acrostic will come from this file.

* -e:   
If you want the word to be hidden at the end of the acrostic, type "-e".   
If you do not type "-e", the word will be hidden at the beginning of the acrostic.

* -t:  
If you have a theme of your acrostic, you can type "-t" followed by a space and then type your theme within quotation marks.  
If you do not type in anything, the default theme will be "I love you"

* -o:  
If you want to output a text file of the acrostic, type "-o".  
If not, no file will be output.
The name of the output will be *"YOUR INPUT"acrostic.txt*, e.g. *missyouacrostic.txt*

### Example:

**Note:** on Max or Linux use ```python3```, on Windows use ```python``` to run the program.

```bash
$ python3 acrosticgenerator.py "missyou" poetry.txt -e -t "I love you"
```

* "missyou" will be hidden at the end of the acrositc.  

* poetry.txt is the input file.  

* "I love you" is the theme

### Example output:
```bash
$ python3 acrosticgenerator.py "missyou" poetry.txt
```

Minded i am to love you very well  
I love you  
So do i wonder what god's love can mean  
S'pose i don't know that?  i married her  
You love me, and i find you still  
Oh why must i lose myself to love you  
Unless you tell me, i feel i'm not loved.  