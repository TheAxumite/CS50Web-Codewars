from re import *

title = "# dfsdfdDjango"

class FormatingError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        raise FormatingError("Unable to convert. Please Format properly.")
        
def convert(title):
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
        page = title
    except Exception as e:
        raise FormatingError("Failed to get entry, error: ", e)
    if not page:
        raise FormatingError("The entry is empty")
    page = page.replace("\n", "<br>")
    page = re.sub(r'(?<![<])[*#_]+', replace_markup, page)
    

    print(page)
