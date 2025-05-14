from dataclasses import dataclass

from model.go_products import Go_product


@dataclass
class Arco:
    nodo1:Go_product
    nodo2: Go_product
