"""
polygon.py
----------
2 boyutlu duzlemde N adet noktadan olusan kapali bir sekli (poligonu)
modelleyen Polygon sinifi.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Sequence, Tuple

from point import Point


@dataclass(frozen=True)
class Polygon:
    """N adet Point'ten olusan kapali bir cokgen.

    Poligon kapali oldugu icin son nokta ile ilk nokta arasinda kapali
    bir kenar oldugu varsayilir; bu nedenle nokta listesinde ilk nokta
    tekrar yazilmaz. En az 3 nokta gereklidir.

    Attributes:
        vertices: Poligonu olusturan kose noktalarin listesi.
    """

    vertices: Tuple[Point, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if len(self.vertices) < 3:
            raise ValueError(
                "Bir Poligon en az 3 noktadan olusmalidir; "
                f"verilen nokta sayisi: {len(self.vertices)}"
            )

   

    @classmethod
    def from_pairs(cls, pairs: Iterable[Sequence[float]]) -> "Polygon":
        """[(x1, y1), (x2, y2), ...] sirasindan Polygon olusturur."""
        return cls(tuple(Point(float(p[0]), float(p[1])) for p in pairs))

 

    @property
    def n(self) -> int:
        """Kose nokta sayisi."""
        return len(self.vertices)

    def edges(self) -> List[Tuple[Point, Point]]:
        """Kapali kenarlarin (P_i, P_{i+1}) ciftleri olarak listesi.

        Son kenar (P_{n-1}, P_0) seklindedir, cunku poligon kapalidir.
        """
        v = self.vertices
        return [(v[i], v[(i + 1) % self.n]) for i in range(self.n)]

    def centroid(self) -> Point:
        """Kose noktalarinin aritmetik ortalamasi olarak agirlik merkezi.

        Donusumlerde (donme, olcekleme) sabit nokta secimi icin yararlidir.
        """
        cx = sum(p.x for p in self.vertices) / self.n
        cy = sum(p.y for p in self.vertices) / self.n
        return Point(cx, cy)

    def coordinates(self) -> List[Tuple[float, float]]:
        """Kose noktalarini (x, y) demetleri listesine cevirir."""
        return [p.as_tuple() for p in self.vertices]



    def __repr__(self) -> str:
        coords = ", ".join(str(p) for p in self.vertices)
        return f"Polygon[n={self.n}]({coords})"

    def pretty(self) -> str:
        """Poligonu okunakli, satir bazli bir formatta dondurur."""
        lines = [f"Polygon (N={self.n}):"]
        for i, p in enumerate(self.vertices):
            lines.append(f"  P{i}: {p}")
        return "\n".join(lines)
