"""
point.py
--------
2 boyutlu duzlemde bir noktayi (x, y) gercel sayi cifti olarak modelleyen
Point sinifi.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Point:
    """2 boyutlu duzlemde bir nokta.

    Nokta degismez (immutable) olarak tasarlanmistir; her donusum yeni bir
    Point uretir. Bu sayede orijinal poligon korunur ve donusum zincirleri
    yan etki olusturmadan uygulanabilir.

    Attributes:
        x: Noktanin yatay (x) koordinati.
        y: Noktanin dikey (y) koordinati.
    """

    x: float
    y: float

    def as_tuple(self) -> Tuple[float, float]:
        """Noktayi (x, y) demeti olarak dondurur."""
        return (self.x, self.y)

    def as_homogeneous(self) -> Tuple[float, float, float]:
        """Noktayi (x, y, 1) homojen koordinat ucluse cevirir.

        Afin donusumler 3x3 matrislerle homojen koordinatlar uzerinde
        uygulandigi icin bu yardimci method onemlidir.
        """
        return (self.x, self.y, 1.0)

    def __repr__(self) -> str:
        return f"Point({self.x:.4f}, {self.y:.4f})"

    def __str__(self) -> str:
        return f"({self.x:.4f}, {self.y:.4f})"
