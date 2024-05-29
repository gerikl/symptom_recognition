import Levenshtein

def calculate_levenshtein_distance(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    return distance

def find_closest_string(str1: str, strings: list[str]) -> str:
    closest_string = min(strings, key=lambda x: calculate_levenshtein_distance(str1, x))
    return closest_string

def find_closest_in_text(str_: str, text: str) -> list[tuple[int, str]]:
    length = len(str_)
    substrs = []
    if length < 5:
        print('Length of the string should be at least 3')
        print(str_)
        if str_ in text:
            return 0, str_
        return 100000, ''
    for shift in [-2, -1, 0, 1, 2]:
        for i in range(len(text) - length + shift + 1):
            substr = text[i:i + length - shift]
            substrs.append((calculate_levenshtein_distance(str_, substr), substr))
    if len(substrs) == 0:
        print('No substrings found')
        print(text)
        print(str_)
        return 100000, ''
    return sorted(substrs)[0]


if __name__ == '__main__':
    str1 = 'тошнота'
    text = 'голова'
    print(*find_closest_in_text(str1, text), sep='\n')
