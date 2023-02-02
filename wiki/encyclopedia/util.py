import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import string




def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None



"""
    This code is a Python script that converts a given text in Markdown format to HTML format. 
    The script uses regular expressions to match specific patterns in the text, such as bold, italic, and heading tags, and replaces them with the corresponding HTML tags. 
    The script also uses a dictionary object, "converter_dict", to store the mapping between the Markdown tags and the corresponding HTML tags. 
    The script also uses some other regex pattern to match the different elements and replace them with their HTML equivalent. 
    The script also check for empty lines and new lines. Overall, the script reads a markdown file and converts it to a HTML file.
"""

class FormatingError(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message
            raise FormatingError("Unable to convert. Please Format properly.")



def convert(title):

    



    try:

        converter_dict = {

            '**':       ['<b>', '</b>'],
            '***':      ['<b><i>', '</i></b>'],
            '*':        ['<li>', '</li>'],
            '__':       ['<b>', '</b>'],
            '_':        ['<i>', '</i>'],
            '\n':       '<br>',
            '#':        ['<h5>', '</h5>'],
            '##':       ['<h4>', '</h4>'],
            '###':      ['<h3>', '</h3>'],
            '####':     ['<h2>', '</h2>'],
            '#####':    ['<h1>', '</h1>'],
            '\r':       '<br>'
        }

        page = re.split('[\n]', get_entry(title))
        pattern = re.compile(r'^\#{2}$|^\#{3}$|^\#{1}$|^\#{4}$|^\#{5}$')
        second_pattern = re.compile(r"^\*{3}|\*{3}$|^\*{2}|\*{2}|^\*{1}|\*{1}$|\_")
        pattern_3 = re.compile(r"\[(.*?)\]|\((.*?)\)")
        pattern_4 = re.compile(r'^\+{1}$|^\*{1}$')
        new_sentence = []
        second_word = ''
        New_line = []

        # Takes the first line from the .MD file
        for line in page:
            # checks to see if the line is empty
            if line:
                line = line + '<br>'

                # used to keep track of the words processed in the line. Resets to zero when a iterating a new line
                length = 0
                # a list object of thee words contained in the line
                words = re.split(' ', line)
                # Checks to see if the current iteration contains a match
                if re.search(pattern, words[0]) is not None:
                    temp_hold = words[0]
                    # Replace the current Markup with the matching HTML equivalent contained in the Converter_dict object
                    words[0] = words[0].replace(
                        temp_hold, converter_dict[temp_hold][0])
                    # Appends the closing HTML mark up at the end of the sentence
                    words.append(converter_dict[temp_hold][1])
                for word in words:
                    length_of_words = len(words)
                    length = length + 1
                    if re.search(second_pattern, word) is not None:
                        matches = second_pattern.finditer(word)
                        count = 0
                        for match in matches:
                            # Create a dictionary for each match in found in the second_pattern
                            holder = {f'{match.group()}': [
                                match.start(), match.end()]}
                            all_markup_found = len(
                                re.findall(second_pattern, word))
                            count = count + 1
                            for key, value in holder.items():
                                if all_markup_found == 1:
                                    if value[0] == 0:
                                        new_word = word.replace(
                                            str(key), converter_dict[key][0], 1)
                                    else:
                                        new_word = word.replace(
                                            str(key), converter_dict[key][1], 1)
                                    if length == length_of_words:
                                        new_word = new_word
                                    new_sentence.append(new_word)
                                if all_markup_found == 2 and count == 1:
                                    new_word = word.replace(
                                        str(key), converter_dict[key][0], 1)
                                    new_word = new_word.replace(
                                        str(key), converter_dict[key][1], 1)
                                    if length == length_of_words:
                                        new_word = new_word

                                    new_sentence.append(new_word)
                    elif not re.search(pattern_3, word):
                        new_sentence.append(word)
                    if re.search(pattern_3, word) is not None and re.search(pattern_3, word) is not string.whitespace:
                        word = word.split(")")
                        word[0] = word[0] + ")"
                        if '(' and ')' and '/' in word[0] or 'https' in word[0]:
                            switch_value = '<a href ="' + \
                                word[0].strip(
                                    "()") + '">' + " " + words[length-2].strip("[]") + '</a>' + word[1]
                            if length + 2 == length_of_words:
                                new_sentence.append(switch_value + '</p>')

                            else:
                                new_sentence.append(switch_value)

            else:
                new_sentence.append('<p></p>')
    except Exception as e:
        raise FormatingError("Failed to get entry, error: ", e)
    if not page:
        raise FormatingError("The entry is empty")
    
    return new_sentence


 

def converting(title):
    converter_dict = {
            '**': '<b>',
            '__': '<b>',
            '*': '<li>',
            '_': '<i>',
            '#': '<h5>',
            '##': '<h4>',
            '###': '<h3>',
            '####': '<h2>',
            '#####': '<h1>',
        }

    def replace_markup(match):
        return converter_dict.get(match.group(), match.group())

    try:
        page = get_entry(title)
    except Exception as e:
        raise FormatingError("Failed to get entry, error: ", e)
    if not page:
        raise FormatingError("The entry is empty")
    page = page.replace("\n", "<br>")
    page = re.sub(r'(?<![<])[*#_]+', replace_markup, page)
    
    return page