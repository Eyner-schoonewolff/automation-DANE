import abc
from typing import List, Dict, Any


class ExcelCalculationService(abc.ABC):
    """
    Clase base para calcular porcentajes.
    """

    @abc.abstractmethod
    def calculate_percentage(
        self, total: int, top_10_total: int
    ) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def calculate_products(self, data: dict) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def calculate_total_top_10(self, top_10: dict) -> int:
        raise NotImplementedError


class ExcelCalculationAdapter(ExcelCalculationService):
    """
    Implementación de la clase ExcelCalculationService.
    """

    def calculate_percentage(
        self, total: int, top_10_total: int
    ) -> float:
        """
        Calcula el porcentaje de ventas del Top 10 respecto al total.
        """
        if not total or not top_10_total:
            raise ValueError(
                "Los datos no están disponibles para calcular el porcentaje."
            )
        print(f"top_10_total: {top_10_total}")
        print(f"total: {total}")
        return (top_10_total / total) * 100

    def calculate_products(self, data: List[Dict[str, Any]]) -> int:
        """
        Calcula el total de la cantidad de productos.
        """
        if not data:
            raise ValueError(
                "No hay datos cargados para calcular el total de productos."
            )
        return sum(int(item["cantidad"]) for item in data)

    def calculate_total_top_10(self, top_10: List[Dict[str, Any]]) -> int:
        """
        Calcula el total de la cantidad de productos más vendidos (Top 10).
        """
        if not top_10:
            raise ValueError(
                "No hay datos cargados para calcular el total de los 10 productos más vendidos."
            )
        return sum(int(item["cantidad"]) for item in top_10)
