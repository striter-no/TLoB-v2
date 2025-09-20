from decimal import Decimal

def dec_sum(l: list[Decimal]) -> Decimal:
    o = Decimal(0)
    for i in l:
        o += i
    return o

class NDIM_Point:
    def __init__(self, coords: list[Decimal]) -> None:
        self.coords = coords
    
    def get_tup(self) -> tuple[Decimal, ...]:
        return tuple(self.coords)

    def distance(self, other: 'NDIM_Point') -> Decimal:
        return Decimal.sqrt(dec_sum([
            (self[i] - other[i]) ** 2 for i in range(self.dimensions)
        ]))

    def length(self) -> Decimal:
        return Decimal.sqrt(dec_sum([
            self[i] ** 2 for i in range(self.dimensions)
        ]))
    
    def normalization(self) -> 'NDIM_Point':
        return NDIM_Point([coord / self.length() for coord in self.coords])

    def __mul__(self, scalar: Decimal) -> 'NDIM_Point':
        return NDIM_Point([coord * scalar for coord in self.coords])

    def __rmul__(self, scalar: Decimal) -> 'NDIM_Point':
        return self.__mul__(scalar)

    def dot(self, other: 'NDIM_Point') -> Decimal:
        if self.dimensions != other.dimensions:
            raise ValueError("Cannot compute dot product of vectors with different dimensions")
        return dec_sum([a * b for a, b in zip(self.coords, other.coords)])

    """
    Value bw -1 and 1 (1 - identical, 0 - perpendicular, -1 - reversed)
    """
    def cosine_similarity(self, other: 'NDIM_Point') -> Decimal:
        dot_product = self.dot(other)
        len1 = self.length()
        len2 = other.length()
        if len1 == 0 or len2 == 0:
            raise ValueError("Cannot compute cosine similarity with zero vector")
        return dot_product / (len1 * len2)

    @property
    def dimensions(self):
        return len(self.coords)
    
    def __getitem__(self, key):
        return self.coords[key]

    def __setitem__(self, key, value):
        self.coords[key] = value
    
    def __add__(self, other) -> 'NDIM_Point':
        return NDIM_Point([
            a + b for a, b in zip(self.coords, other.coords)
        ])

    def __sub__(self, other) -> 'NDIM_Point':
        return NDIM_Point([
            a - b for a, b in zip(self.coords, other.coords)
        ])

    def __str__(self) -> str:
        return f"/".join([f"{c:f}" for c in self.coords])