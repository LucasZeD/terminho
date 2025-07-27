import random
from functools import lru_cache

@lru_cache(maxsize=1)
def load_dictionary() -> set[str]:
    with open("data/words.txt", "r", encoding="utf-8") as f:
        return {line.strip().upper() for line in f if len(line.strip()) == 5}
    
def get_random_word() -> str:
    return random.choice(list(load_dictionary()))

def check_guess(guess: str, secret: str) -> list[str]:
    #return emojis
    results = ['⬛']*5
    secret_list = list(secret)
    guess_list = list(guess)
    
    for i in range(5):
        if guess_list[i] == secret_list[i]:
            results[i] = '🟩'
            secret_list[i] = None
            guess_list[i] = None
            
    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            results[i] = '🟨'
            secret_list[secret_list.index(guess_list[i])] = None
            
    return results
        