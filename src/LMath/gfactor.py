from collections import Counter
import math

def g2_factor(text: str, words_min = 470, stopwords = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
    'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'he', 'she',
    'it', 'they', 'we', 'you', 'i', 'this', 'that', 'these', 'those', 'there', 'here',
    'what', 'why', 'how', 'when', 'where', 'who', 'which', 'not', 'no', 'yes', 'if',
    'then', 'else', 'than', 'so', 'such', 'as', 'from', 'into', 'through', 'over',
    'under', 'above', 'below', 'between', 'among', 'during', 'before', 'after',
    'since', 'while', 'until', 'again', 'further', 'more', 'most', 'some', 'any',
    'all', 'both', 'each', 'every', 'either', 'neither', 'one', 'two', 'first',
    'second', 'last', 'next', 'up', 'down', 'out', 'off', 'about', 'around',
    'because', 'though', 'although', 'even', 'ever', 'never', 'always', 'often',
    'sometimes', 'usually', 'just', 'only', 'also', 'well', 'very', 'too', 'much',
    'many', 'few', 'little', 'own', 'same', 'different', 'good', 'bad', 'new',
    'old', 'great', 'small', 'large', 'long', 'short', 'high', 'low', 'right',
    'left', 'top', 'bottom', 'inside', 'outside', 'near', 'far', 'together',
    'alone', 'back', 'forward', 'away', 'home', 'work', 'school', 'life',
    'time', 'day', 'year', 'man', 'woman', 'child', 'people', 'person'
}):
    
    text = text.replace(',', ' ').replace('.', ' ')
    if text.count(" ") < words_min:
        return -3

    length = len(text)
    counter = Counter(text)
    unique_chars = len(counter)
    
    max_entropy = math.log2(unique_chars) if unique_chars > 1 else 1.0
    entropy_score = -sum((count / length) * math.log2(count / length) for count in counter.values() if count > 0) / max_entropy if max_entropy > 0 else 1.0

    if entropy_score >= 0.9 or entropy_score < 0.8:
        return -1

    words = text.split()
    if len(words) == 0:
        word_len_score = 1.0
    else:
        avg_word_len = sum(len(w) for w in words) / len(words)
        word_len_score = 1.0 - max(0, 1 - abs(avg_word_len - 6) / 6) if avg_word_len > 0 else 1.0

    print(word_len_score)
    if word_len_score > 0.27 or word_len_score < 0.1:
        return -4

    bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
    stopword_bigrams = sum(
        1 for w1, w2 in bigrams
        if w1 in stopwords and w2 in stopwords
    )
    total = len(set(bigrams))
    if (stopword_bigrams / total if total > 0 else 0) < 0.1:
        return -5

    return (entropy_score * 0.03 * word_len_score * 0.35 * stopword_bigrams * 0.6)

def decode_g2(val: int | float) -> str:
    if isinstance(val, float):
        return f"likely real (score: {val})"
    
    match val:
        case -1: return "very high or low entropy"
        case -3: return "too litle words"
        case -4: return "too big or little words"
        case -5: return "lack of real words"
    
    return f"unknown code ({val})"