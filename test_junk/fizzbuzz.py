
def is_anagram(firstWord: str, secondWord: str) -> bool:
    if firstWord is secondWord[::-1]:
        return True
    else:
        print(secondWord[::-1])
        return False

print(is_anagram("eat","tea"))