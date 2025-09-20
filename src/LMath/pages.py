from functools import lru_cache
from decimal import Decimal

DEFAULT_ALPHABET = 'etaoinshrdlcumwfgypbvkjxqz,. '
CLOSE_ALPHABET   = ' etaoinshrdlcumwfgypbvkjxqz,.'

@lru_cache(maxsize=128)
def _get_page_f(base: int, digits: str, length: int):
    def _to_compile(numb):
        if numb == 0:
            s = digits[0]
        else:
            chars = []
            numb = int(numb)
            while numb:
                numb, r = divmod(numb, base)
                chars.append(digits[r])
            s = ''.join(reversed(chars))
        
        s = digits[0] * (length - len(s)) + s
        return s

    return _to_compile

@lru_cache(maxsize=128)
def _get_search_f(base: int, digits: str):
    def _to_compile(number_str: str) -> Decimal:
        decimal_value = 0
        
        for i, char in enumerate(reversed(number_str)):
            value = digits.index(char)
            decimal_value += value * (base ** i)
        
        return Decimal(decimal_value)

    return _to_compile

def formated(sstr: str, line_len: int):
    out = ""
    for i in range(len(sstr)):
        out += sstr[i]
        if (i + 1) % line_len == 0:
            out += "\n"
    
    return out

class Page:
    def __init__(
            self, 
            alphabet: str, 
            address: Decimal = Decimal(-1), 
            text: str = "", 
            context_max_len = 200 * 30 * 50, 
            title: str = "nt-page"
    ) -> None:
        self.address: Decimal = address
        self._cached_val: str = text
        self.alphabet: str = alphabet
        self.title: str = title

        self.context_max_len = context_max_len

        if self._cached_val != '' and len(self._cached_val) < self.context_max_len:
            self._cached_val += ' ' * (self.context_max_len - len(self._cached_val))

        self.search_f = _get_search_f(len(self.alphabet), self.alphabet)
        self.page_f = _get_page_f(len(self.alphabet), self.alphabet, self.context_max_len)

    def max_address(self) -> Decimal:
        return self.search_f("".join([self.alphabet[-1] for i in range(self.context_max_len)]))

    def get_addr(self) -> Decimal:
        if self.address != -1:
            return self.address
        if self._cached_val == '':
            return Decimal(-1)
        
        if len(self._cached_val) < self.context_max_len:
            self._cached_val += ' ' * (self.context_max_len - len(self._cached_val))

        self.address = self.search_f(self._cached_val)
        return self.address

    def get_text(self) -> str:
        if self._cached_val == '':
            self._cached_val = self.page_f(self.address)
        return self._cached_val

    def get_formatted(self, line_len: int = 80) -> str:
        if self._cached_val == '':
            self.get_text()
        return formated(self._cached_val, line_len)

    def file_dump(self, path: str, line_len = 80):
        with open(path, 'w') as f:
            f.write(self.get_formatted(line_len))

    def search(self, text: str) -> 'Page':
        if len(text) < self.context_max_len:
            text += ' ' * (self.context_max_len - len(text))

        _addr = self.search_f(text)
        return self.fork(address = _addr, text = text)
    
    def acquire(self, address: Decimal, title: str = '') -> 'Page':
        _text = self.page_f(address)
        return self.fork(address = address, text = _text, title = title)
    
    def fork(self, address: Decimal = Decimal(-1), text: str = '', title: str = '') -> 'Page':
        if address != -1:
            return Page(
                alphabet = self.alphabet,
                address = address,
                text = '',
                context_max_len = self.context_max_len,
                title = title
            )

        if text != '':
            return Page(
                alphabet = self.alphabet,
                address = Decimal(-1),
                text = text,
                context_max_len = self.context_max_len,
                title = title
            )
        
        return self