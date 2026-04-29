"""
tests.py
--------
2D Afin Donusum kutuphanesi icin temel dogrulama testleri.

Calistirma:
    python tests.py

Tum testler bagimsiz olarak yazilmistir; harici test cercevesi
gerekmemektedir.
"""

from __future__ import annotations

import math

from point import Point
from polygon import Polygon
import transformations as T


TOL = 1e-9


def almost_equal(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def points_close(p: Point, q: Point, tol: float = TOL) -> bool:
    return almost_equal(p.x, q.x, tol) and almost_equal(p.y, q.y, tol)


def polygons_close(p: Polygon, q: Polygon, tol: float = TOL) -> bool:
    if p.n != q.n:
        return False
    return all(points_close(a, b, tol) for a, b in zip(p.vertices, q.vertices))


def assert_close(p: Polygon, q: Polygon, msg: str) -> None:
    assert polygons_close(p, q), (
        f"FAIL: {msg}\n  beklenen: {q}\n  gercek:   {p}"
    )
    print(f"OK  - {msg}")


def square() -> Polygon:
    """Birim kare (kose noktalari (0,0), (1,0), (1,1), (0,1))."""
    return Polygon.from_pairs([(0, 0), (1, 0), (1, 1), (0, 1)])


# ---------------------------------------------------------------------
# Testler
# ---------------------------------------------------------------------

def test_translation() -> None:
    p = square()
    out = T.translate(p, 3, -2)
    expected = Polygon.from_pairs([(3, -2), (4, -2), (4, -1), (3, -1)])
    assert_close(out, expected, "Oteleme (3, -2)")


def test_scaling_at_origin() -> None:
    p = square()
    out = T.scale(p, 2, 3)
    expected = Polygon.from_pairs([(0, 0), (2, 0), (2, 3), (0, 3)])
    assert_close(out, expected, "Olcekleme orijine gore (sx=2, sy=3)")


def test_scaling_at_pivot() -> None:
    p = square()
    pivot = Point(0.5, 0.5)
    out = T.scale(p, 2, pivot=pivot)
    expected = Polygon.from_pairs(
        [(-0.5, -0.5), (1.5, -0.5), (1.5, 1.5), (-0.5, 1.5)]
    )
    assert_close(out, expected, "Olcekleme merkez (0.5,0.5) etrafinda (2x)")


def test_rotation_90() -> None:
    p = square()
    out = T.rotate_degrees(p, 90)
    # 90 derece: (x, y) -> (-y, x)
    expected = Polygon.from_pairs([(0, 0), (0, 1), (-1, 1), (-1, 0)])
    assert_close(out, expected, "Donme 90 derece (orijin)")


def test_rotation_360_identity() -> None:
    p = square()
    out = T.rotate_degrees(p, 360)
    assert_close(out, p, "Donme 360 derece -> birim donusum")


def test_shear_x() -> None:
    p = square()
    out = T.shear(p, shx=2)
    # (x, y) -> (x + 2y, y)
    expected = Polygon.from_pairs([(0, 0), (1, 0), (3, 1), (2, 1)])
    assert_close(out, expected, "Kayma shx=2")


def test_reflection_x_axis() -> None:
    p = square()
    out = T.reflect_x_axis(p)
    expected = Polygon.from_pairs([(0, 0), (1, 0), (1, -1), (0, -1)])
    assert_close(out, expected, "x ekseni etrafinda yansima")


def test_reflection_line_y_eq_x() -> None:
    p = square()
    out = T.reflect_line_y_eq_x(p)
    # (x, y) -> (y, x)
    expected = Polygon.from_pairs([(0, 0), (0, 1), (1, 1), (1, 0)])
    assert_close(out, expected, "y = x dogrusuna gore yansima")


def test_reflection_arbitrary_line() -> None:
    # y = 2 dogrusu -> 0*x + 1*y - 2 = 0
    p = square()
    out = T.reflect_line(p, 0, 1, -2)
    expected = Polygon.from_pairs([(0, 4), (1, 4), (1, 3), (0, 3)])
    assert_close(out, expected, "y = 2 dogrusuna gore yansima")


def test_composition_order() -> None:
    """Once dondur, sonra otele -> compose(T, R)."""
    p = square()
    M = T.compose(T.translation_matrix(5, 0), T.rotation_matrix(math.pi / 2))
    out = T.apply_matrix(p, M)
    # (x,y) -> rotate -> (-y, x) -> translate (5,0) -> (5-y, x)
    expected = Polygon.from_pairs([(5, 0), (5, 1), (4, 1), (4, 0)])
    assert_close(out, expected, "compose(translate, rotate) sirasi")


def test_inverse_via_negative_translation() -> None:
    p = square()
    out = T.translate(T.translate(p, 7, -3), -7, 3)
    assert_close(out, p, "Oteleme ve tersi -> orijinal poligon")


def test_double_reflection_identity() -> None:
    p = square()
    out = T.reflect_x_axis(T.reflect_x_axis(p))
    assert_close(out, p, "x ekseni etrafinda iki kez yansima -> birim")


def test_general_affine_matches_translation() -> None:
    p = square()
    out = T.apply_general_affine(p, 1, 0, 5, 0, 1, -3)
    expected = T.translate(p, 5, -3)
    assert_close(out, expected, "Genel afin (1,0,5,0,1,-3) = oteleme(5,-3)")


def test_polygon_min_vertices() -> None:
    try:
        Polygon.from_pairs([(0, 0), (1, 0)])
    except ValueError:
        print("OK  - 2 noktali poligon ValueError firlatti (en az 3 olmali)")
        return
    raise AssertionError("FAIL: 2 noktali poligon icin hata beklendi")


def test_centroid() -> None:
    p = square()
    c = p.centroid()
    assert points_close(c, Point(0.5, 0.5)), f"Beklenen merkez (0.5, 0.5), bulunan {c}"
    print("OK  - Birim karenin agirlik merkezi (0.5, 0.5)")


def run_all() -> None:
    tests = [
        test_translation,
        test_scaling_at_origin,
        test_scaling_at_pivot,
        test_rotation_90,
        test_rotation_360_identity,
        test_shear_x,
        test_reflection_x_axis,
        test_reflection_line_y_eq_x,
        test_reflection_arbitrary_line,
        test_composition_order,
        test_inverse_via_negative_translation,
        test_double_reflection_identity,
        test_general_affine_matches_translation,
        test_polygon_min_vertices,
        test_centroid,
    ]
    print("Tum testler calistiriliyor...")
    print("-" * 64)
    for t in tests:
        t()
    print("-" * 64)
    print(f"BASARILI: {len(tests)} test gecti.")


if __name__ == "__main__":
    run_all()
