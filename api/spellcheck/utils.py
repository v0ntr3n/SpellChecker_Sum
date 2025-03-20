""" Additional utility functions """
import contextlib
import gzip
import re
import typing
from pathlib import Path

KeyT = typing.Union[str, bytes]
PathOrStr = typing.Union[Path, str]



def prepare_text_for_spell_check(text):
    # Split the text into words and remove punctuation
    words = re.findall(r'\b\w+\b', text)
    # Keep track of original words with punctuation
    original_words = text.split()
    
    # Create a mapping between original and processed words
    word_mapping = dict(zip([re.sub(r'[^\w\s]', '', w).lower() for w in original_words], original_words))
    
    # Prepare words for spell checking
    prepared_words = [re.sub(r'[^\w\s]', '', w).lower() for w in original_words]
    
    return prepared_words, word_mapping

def correct_original_text(text, misspelled, word_mapping, spell_suggestions):
    # Create a mapping of misspelled words to their corrections
    correction_mapping = {}
    for word in misspelled:
        # Assuming spell_suggestions returns a list of suggestions for each word
        suggestions = spell_suggestions(word)
        if suggestions:
            correction_mapping[word] = suggestions  # Use the first suggestion
    
    # Replace misspelled words in the original text
    corrected_text = text
    for word, correction in correction_mapping.items():
        for original_word in word_mapping:
            if original_word == word:
                original_text_word = word_mapping[original_word]
                corrected_text_word = re.sub(r'\b\w+\b', correction, original_text_word)
                corrected_text = corrected_text.replace(original_text_word, corrected_text_word)
    
    return corrected_text, correction_mapping

def ensure_unicode(value: KeyT, encoding: str = "utf-8") -> str:
    """Simplify checking if passed in data are bytes or a string and decode
    bytes into unicode.

    Args:
        value (str): The input string (possibly bytes)
        encoding (str): The encoding to use if input is bytes
    Returns:
        str: The encoded string
    """
    if isinstance(value, bytes):
        return value.decode(encoding)
    return value


@contextlib.contextmanager
def __gzip_read(filename: PathOrStr, mode: str = "rb", encoding: str = "UTF-8") -> typing.Generator[KeyT, None, None]:
    """Context manager to correctly handle the decoding of the output of the gzip file

    Args:
        filename (str): The filename to open
        mode (str): The mode to read the data
        encoding (str): The file encoding to use
    Yields:
        str: The string data from the gzip file read
    """
    with gzip.open(filename, mode=mode, encoding=encoding) as fobj:
        yield fobj.read()


@contextlib.contextmanager
def load_file(filename: PathOrStr, encoding: str) -> typing.Generator[KeyT, None, None]:
    """Context manager to handle opening a gzip or text file correctly and
    reading all the data

    Args:
        filename (str): The filename to open
        encoding (str): The file encoding to use
    Yields:
        str: The string data from the file read
    """
    if isinstance(filename, Path):
        filename = str(filename)

    if filename[-3:].lower() == ".gz":
        with __gzip_read(filename, mode="rt", encoding=encoding) as data:
            yield data
    else:
        with open(filename, encoding=encoding) as fobj:
            yield fobj.read()


def write_file(filepath: PathOrStr, encoding: str, gzipped: bool, data: str) -> None:
    """Write the data to file either as a gzip file or text based on the
    gzipped parameter

    Args:
        filepath (str): The filename to open
        encoding (str): The file encoding to use
        gzipped (bool): Whether the file should be gzipped or not
        data (str): The data to be written out
    """
    if gzipped:
        with gzip.open(filepath, "wt") as fobj:
            fobj.write(data)
    else:
        with open(filepath, "w", encoding=encoding) as fobj:
            fobj.write(data)


def _parse_into_words(text: str) -> typing.Iterable[str]:
    """Parse the text into words; currently removes punctuation except for
    apostrophizes.

    Args:
        text (str): The text to split into words
    """
    # see: https://stackoverflow.com/a/12705513
    return re.findall(r"(\w[\w']*\w|\w)", text)
