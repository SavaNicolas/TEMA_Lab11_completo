from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Go_product:
    Product_number:int #chiave
    Product_line:str
    Product_type:str
    Product:str
    Product_brand:str
    Product_color:str
    Unit_cost:Decimal
    Unit_price:Decimal

    def __hash__(self):
        return self.Product_number

    def __str__(self):
        return f"{self.Product}"

    def __eq__(self, other):
        return self.Product_number == other.Product_number