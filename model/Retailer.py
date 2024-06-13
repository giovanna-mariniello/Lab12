from dataclasses import dataclass
@dataclass
class Retailer:
    _Retailer_code: int
    _Retailer_name: str
    _Type: str
    _Country: str

    @property
    def Country(self):
        return self._Country
    @property
    def Retailer_code(self):
        return self._Retailer_code
    @property
    def Retailer_name(self):
        return self._Retailer_name
    def __str__(self):
        return self._Retailer_code
    def __hash__(self):
        return hash(self._Retailer_code)
