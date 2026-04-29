"""
main.py
-------
2D Afin Donusumler programinin demo / surucu dosyasi.

Calistirildiginda:
  - Ornek bir poligon olusturulur,
  - tum afin donusumler poligona uygulanir,
  - dogan yeni poligonun koordinatlari ekrana yazilir.

Calistirma:
    python main.py

Odev gereksinimi:
"Programin bir GUI programi olmasi gerekmiyor. Calistirildiginda donusum
fonksiyonlarinin urettigi yeni poligon'a ait koordinatlari donmesi veya
ekranda goruntulemesi yeterlidir."
"""

from __future__ import annotations

import math

from point import Point
from polygon import Polygon
import transformations as T


def banner(title: str) -> None:
    """Ekrana baslik yazdirir."""
    print()
    print("=" * 64)
    print(f"  {title}")
    print("=" * 64)


def show(label: str, polygon: Polygon) -> None:
    """Bir donusumun adi ile birlikte cikan poligonun koordinatlarini yazar."""
    print(f"\n>>> {label}")
    for i, p in enumerate(polygon.vertices):
        print(f"    P{i}: ({p.x:+.4f}, {p.y:+.4f})")


def main() -> None:
    # --- Ornek poligon: bir besgen ----------------------------------
    # Birim cember uzerinde 5 nokta secilerek olusturulan duzgun besgen.
    n_vertices = 5
    pentagon = Polygon(
        tuple(
            Point(
                math.cos(2 * math.pi * k / n_vertices),
                math.sin(2 * math.pi * k / n_vertices),
            )
            for k in range(n_vertices)
        )
    )

    banner("BAŞLANGIÇ POLİGONU")
    show("Orijinal poligon (duzgun besgen, birim cember uzerinde)", pentagon)

    # --- 1) Oteleme -------------------------------------------------
    banner("1) ÖTELEME (Translation)")
    show("translate(P, tx=3, ty=2)", T.translate(pentagon, 3, 2))
    show("translate(P, tx=-1.5, ty=4)", T.translate(pentagon, -1.5, 4))

    # --- 2) Olcekleme ----------------------------------------------
    banner("2) ÖLÇEKLEME (Scaling)")
    show("scale(P, 2)  -> her iki eksende 2 katina cikar",
         T.scale(pentagon, 2))
    show("scale(P, 1.5, 0.5)  -> x'te 1.5, y'de 0.5",
         T.scale(pentagon, 1.5, 0.5))
    show("scale(P, 2, pivot=centroid)  -> agirlik merkezi etrafinda",
         T.scale(pentagon, 2, pivot=pentagon.centroid()))

    # --- 3) Donme --------------------------------------------------
    banner("3) DÖNME (Rotation)")
    show("rotate_degrees(P, 90)  -> orijine gore 90 derece",
         T.rotate_degrees(pentagon, 90))
    show("rotate_degrees(P, 45, pivot=Point(1, 0))",
         T.rotate_degrees(pentagon, 45, pivot=Point(1, 0)))

    # --- 4) Kayma --------------------------------------------------
    banner("4) KAYMA (Shear)")
    show("shear(P, shx=0.5)  -> y'ye orantili x kaymasi",
         T.shear(pentagon, shx=0.5))
    show("shear(P, shy=0.3)  -> x'e orantili y kaymasi",
         T.shear(pentagon, shy=0.3))
    show("shear(P, shx=0.3, shy=0.2)  -> her iki eksende kayma",
         T.shear(pentagon, shx=0.3, shy=0.2))

    # --- 5) Yansimalar ----------------------------------------------
    banner("5) YANSIMA (Reflection)")
    show("reflect_x_axis(P)", T.reflect_x_axis(pentagon))
    show("reflect_y_axis(P)", T.reflect_y_axis(pentagon))
    show("reflect_origin(P)", T.reflect_origin(pentagon))
    show("reflect_line_y_eq_x(P)", T.reflect_line_y_eq_x(pentagon))
    show("reflect_line(P, a=1, b=-1, c=0)  -> y = x dogrusu",
         T.reflect_line(pentagon, 1, -1, 0))
    show("reflect_line(P, a=0, b=1, c=-2)  -> y = 2 dogrusu",
         T.reflect_line(pentagon, 0, 1, -2))

    # --- 6) Genel afin donusum --------------------------------------
    banner("6) GENEL AFİN DÖNÜŞÜM (General Affine)")
    show("apply_general_affine(P, 2, 1, 3, 0, 1, -1)",
         T.apply_general_affine(pentagon, 2, 1, 3, 0, 1, -1))

    # --- 7) Birlesik (compose) donusum -----------------------------
    banner("7) BİRLEŞİK DÖNÜŞÜM (Composition)")
    # Once 45 derece dondur, sonra 2 katina olcekle, son olarak (5, 0) otele.
    M = T.compose(
        T.translation_matrix(5, 0),
        T.scaling_matrix(2, 2),
        T.rotation_matrix(math.radians(45)),
    )
    transformed = T.apply_matrix(pentagon, M)
    show("translate(5,0) * scale(2) * rotate(45)", transformed)

    # --- 8) Determinant kontrolu -----------------------------------
    banner("8) BİLGİ NOTLARI")
    print("- Tum afin donusumler 3x3 homojen matrislerle ifade edilir.")
    print("- Determinant > 0 -> yon korunur, alan |det| katina olcek alir.")
    print("- Determinant < 0 -> yansima vardir.")
    print("- Determinant = 0 -> donusum tekildir, bilgi kaybeder.\n")


if __name__ == "__main__":
    main()
