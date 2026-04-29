"""
transformations.py
------------------
2 boyutlu Afin Donusumler (2D Affine Transformations).

Tum donusumler 3x3 homojen donusum matrisleri kullanilarak uygulanir.
Bir nokta P = (x, y) homojen koordinatlarda P' = (x, y, 1) seklinde
yazilir ve donusum matrisi M ile carpilarak hedef nokta elde edilir:

        | x' |   | a  b  tx | | x |
        | y' | = | c  d  ty | | y |
        | 1  |   | 0  0  1  | | 1 |

Tum fonksiyonlar uzerine uygulandiklari Polygon'u degistirmez (immutable);
yeni bir Polygon dondururler. Bu sayede donusumler zincirleme olarak
gelistirilebilir.

Bu modul odevin su gereksinimini karsilamaktadir:
"Poligon uzerinde tanimli tum Afin donusumleri birer fonksiyonla
gerceklesin."
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from point import Point
from polygon import Polygon


# Tip kisaltmalari
Matrix3 = Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    Tuple[float, float, float],
]


# =====================================================================
# Matris yardimcilari
# =====================================================================

def identity_matrix() -> Matrix3:
    """3x3 birim matrisi dondurur."""
    return (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


def matrix_multiply(a: Matrix3, b: Matrix3) -> Matrix3:
    """Iki 3x3 matrisi carpar: C = A * B.

    Donusumlerin birlestirilmesinde kullanilir. Donusum sirasi soldan
    saga matris carpimi seklindedir:
        compose(R, T) ile bir noktaya R * T * P uygulanmis olur.
    """
    result = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(3))
    return (
        (result[0][0], result[0][1], result[0][2]),
        (result[1][0], result[1][1], result[1][2]),
        (result[2][0], result[2][1], result[2][2]),
    )


def compose(*matrices: Matrix3) -> Matrix3:
    """Birden cok donusum matrisini sirasiyla birlestirir.

    compose(M1, M2, M3) -> M1 * M2 * M3
    Donusum hep en sagdaki matristen baslayarak uygulanir.
    """
    if not matrices:
        return identity_matrix()
    result = matrices[0]
    for m in matrices[1:]:
        result = matrix_multiply(result, m)
    return result


def apply_to_point(m: Matrix3, p: Point) -> Point:
    """Bir 3x3 matrisi homojen olarak bir noktaya uygular."""
    x, y, w = p.as_homogeneous()
    nx = m[0][0] * x + m[0][1] * y + m[0][2] * w
    ny = m[1][0] * x + m[1][1] * y + m[1][2] * w
    nw = m[2][0] * x + m[2][1] * y + m[2][2] * w
    if nw != 0 and nw != 1:
        nx /= nw
        ny /= nw
    return Point(nx, ny)


def apply_to_polygon(m: Matrix3, polygon: Polygon) -> Polygon:
    """Bir 3x3 matrisi bir poligonun tum kose noktalarina uygular.

    Uygulama her kose nokta icin bagimsiz oldugundan poligonun topolojisi
    (komsuluklari, kapali olusu) bozulmaz.
    """
    return Polygon(tuple(apply_to_point(m, p) for p in polygon.vertices))


# =====================================================================
# Temel afin donusum matrisleri
# =====================================================================

def translation_matrix(tx: float, ty: float) -> Matrix3:
    """Oteleme (translation) matrisi.

        T(tx, ty) = | 1 0 tx |
                    | 0 1 ty |
                    | 0 0 1  |
    """
    return (
        (1.0, 0.0, float(tx)),
        (0.0, 1.0, float(ty)),
        (0.0, 0.0, 1.0),
    )


def scaling_matrix(sx: float, sy: Optional[float] = None) -> Matrix3:
    """Olcekleme (scaling) matrisi.

    Tek olcek katsayisi verilirse her iki eksende esit olcekleme uygulanir.

        S(sx, sy) = | sx 0  0 |
                    | 0  sy 0 |
                    | 0  0  1 |
    """
    if sy is None:
        sy = sx
    return (
        (float(sx), 0.0, 0.0),
        (0.0, float(sy), 0.0),
        (0.0, 0.0, 1.0),
    )


def rotation_matrix(theta_radians: float) -> Matrix3:
    """Orijin etrafinda saat yonunun tersine donme (rotation) matrisi.

        R(theta) = | cos(theta)  -sin(theta)  0 |
                   | sin(theta)   cos(theta)  0 |
                   |     0            0       1 |
    """
    c = math.cos(theta_radians)
    s = math.sin(theta_radians)
    return (
        (c, -s, 0.0),
        (s,  c, 0.0),
        (0.0, 0.0, 1.0),
    )


def shear_matrix(shx: float = 0.0, shy: float = 0.0) -> Matrix3:
    """Kayma (shear) matrisi.

        Sh(shx, shy) = | 1   shx 0 |
                       | shy 1   0 |
                       | 0   0   1 |

    shx > 0 -> x ekseni yonunde y'ye orantili kayma
    shy > 0 -> y ekseni yonunde x'e orantili kayma
    """
    return (
        (1.0, float(shx), 0.0),
        (float(shy), 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


def reflection_matrix_x_axis() -> Matrix3:
    """x ekseni etrafinda yansima: (x, y) -> (x, -y)."""
    return (
        (1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


def reflection_matrix_y_axis() -> Matrix3:
    """y ekseni etrafinda yansima: (x, y) -> (-x, y)."""
    return (
        (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


def reflection_matrix_origin() -> Matrix3:
    """Orijine gore yansima: (x, y) -> (-x, -y).

    Bu donusum 180 derecelik donme ile aynidir.
    """
    return (
        (-1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, 0.0, 1.0),
    )


def reflection_matrix_line_y_eq_x() -> Matrix3:
    """y = x dogrusuna gore yansima: (x, y) -> (y, x)."""
    return (
        (0.0, 1.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0),
    )


def reflection_matrix_line(a: float, b: float, c: float) -> Matrix3:
    """ax + by + c = 0 dogrusuna gore genel yansima matrisi.

    Turetilis: dogrunun normaline gore yansima formulu
        x' = x - 2a(ax + by + c) / (a^2 + b^2)
        y' = y - 2b(ax + by + c) / (a^2 + b^2)
    """
    denom = a * a + b * b
    if denom == 0:
        raise ValueError("a ve b ayni anda 0 olamaz; bu bir dogru tanimlamaz.")
    m11 = (b * b - a * a) / denom
    m12 = -2 * a * b / denom
    m13 = -2 * a * c / denom
    m21 = -2 * a * b / denom
    m22 = (a * a - b * b) / denom
    m23 = -2 * b * c / denom
    return (
        (m11, m12, m13),
        (m21, m22, m23),
        (0.0, 0.0, 1.0),
    )


def general_affine_matrix(
    a: float, b: float, tx: float,
    c: float, d: float, ty: float,
) -> Matrix3:
    """Genel afin donusum matrisi.

        M = | a b tx |
            | c d ty |
            | 0 0 1  |

    Tum afin donusumler bu formun ozel halidir; oteleme, olcekleme,
    donme, kayma ve yansima bu matrisin parametreleriyle ifade edilebilir.
    Determinant (ad - bc) sifirdan farkli olmalidir; aksi halde donusum
    tekildir (bilgi kaybeder).
    """
    return (
        (float(a), float(b), float(tx)),
        (float(c), float(d), float(ty)),
        (0.0, 0.0, 1.0),
    )


# =====================================================================
# Sabit nokta etrafinda donusumler
# =====================================================================

def about_point(matrix: Matrix3, pivot: Point) -> Matrix3:
    """Bir donusum matrisini verilen sabit nokta (pivot) etrafinda calistirir.

    Yontem: T(pivot) * M * T(-pivot)
    Once pivot orijine tasinir, donusum uygulanir, ardindan pivot eski
    konumuna geri tasinir. Donme ve olcekleme icin merkez secimi bu
    yardimcilarla kolayca degistirilebilir.
    """
    t_to_origin = translation_matrix(-pivot.x, -pivot.y)
    t_back = translation_matrix(pivot.x, pivot.y)
    return compose(t_back, matrix, t_to_origin)


# =====================================================================
# Yuksek seviye, poligon uzerinde calisan fonksiyonlar
# =====================================================================

def translate(polygon: Polygon, tx: float, ty: float) -> Polygon:
    """Poligonu (tx, ty) vektoru ile oteler."""
    return apply_to_polygon(translation_matrix(tx, ty), polygon)


def scale(
    polygon: Polygon,
    sx: float,
    sy: Optional[float] = None,
    pivot: Optional[Point] = None,
) -> Polygon:
    """Poligonu olcekler.

    pivot verilmezse orijin etrafinda olcekleme uygulanir. Genelde
    polygon.centroid() pivot olarak verilirse poligon yerinde olcek
    degistirir.
    """
    if sy is None:
        sy = sx
    m = scaling_matrix(sx, sy)
    if pivot is not None:
        m = about_point(m, pivot)
    return apply_to_polygon(m, polygon)


def rotate(
    polygon: Polygon,
    theta_radians: float,
    pivot: Optional[Point] = None,
) -> Polygon:
    """Poligonu theta radyanla saat yonunun tersine dondurur.

    pivot verilmezse orijin etrafinda donme uygulanir.
    """
    m = rotation_matrix(theta_radians)
    if pivot is not None:
        m = about_point(m, pivot)
    return apply_to_polygon(m, polygon)


def rotate_degrees(
    polygon: Polygon,
    theta_degrees: float,
    pivot: Optional[Point] = None,
) -> Polygon:
    """rotate() fonksiyonunun derece girdili surumudur."""
    return rotate(polygon, math.radians(theta_degrees), pivot)


def shear(
    polygon: Polygon,
    shx: float = 0.0,
    shy: float = 0.0,
    pivot: Optional[Point] = None,
) -> Polygon:
    """Poligona kayma uygular.

    Sadece shx verilirse x yonunde, sadece shy verilirse y yonunde,
    her ikisi verilirse her iki eksende kayma uygulanir.
    """
    m = shear_matrix(shx, shy)
    if pivot is not None:
        m = about_point(m, pivot)
    return apply_to_polygon(m, polygon)


def reflect_x_axis(polygon: Polygon) -> Polygon:
    """x ekseni etrafinda yansima."""
    return apply_to_polygon(reflection_matrix_x_axis(), polygon)


def reflect_y_axis(polygon: Polygon) -> Polygon:
    """y ekseni etrafinda yansima."""
    return apply_to_polygon(reflection_matrix_y_axis(), polygon)


def reflect_origin(polygon: Polygon) -> Polygon:
    """Orijine gore yansima."""
    return apply_to_polygon(reflection_matrix_origin(), polygon)


def reflect_line_y_eq_x(polygon: Polygon) -> Polygon:
    """y = x dogrusuna gore yansima."""
    return apply_to_polygon(reflection_matrix_line_y_eq_x(), polygon)


def reflect_line(polygon: Polygon, a: float, b: float, c: float) -> Polygon:
    """ax + by + c = 0 dogrusuna gore yansima."""
    return apply_to_polygon(reflection_matrix_line(a, b, c), polygon)


def apply_general_affine(
    polygon: Polygon,
    a: float, b: float, tx: float,
    c: float, d: float, ty: float,
) -> Polygon:
    """Genel afin donusum (kullanici tarafindan tanimlanan a, b, c, d, tx, ty)."""
    m = general_affine_matrix(a, b, tx, c, d, ty)
    return apply_to_polygon(m, polygon)


def apply_matrix(polygon: Polygon, matrix: Matrix3) -> Polygon:
    """Hazir bir 3x3 matrisi poligona uygular.

    Birden cok donusumun compose() ile birlestirilip tek seferde
    uygulanmasi icin idealdir.
    """
    return apply_to_polygon(matrix, polygon)
