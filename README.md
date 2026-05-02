# 2D Afin Dönüşümler (2D Affine Transformations)

Bu depo, **Bilgisayar Grafiklerinde İleri Konular** dersi dönem ödevinin
ikinci sorusunun çözümünü içermektedir. Programlama dili olarak
**saf Python (standart kütüphane)** seçilmiştir; harici hiçbir bağımlılık
yoktur.

## Ödev gereksinimleri

> Seçtiğiniz herhangi bir programlama dilinde 2 boyutta Afin Dönüşümü
> örnekleyen aşağıdaki özelliklerde basit bir program yazın.
> - GitHub'ta bir depo açın ve bu depoda çalışın.
> - 2 boyutlu düzlemde x, y gerçel sayı çifti halinde bir noktayı (Point)
>   modelleyin.
> - Geometrik eleman olarak sadece bir Poligon'u modelleyin (N adet
>   noktadan oluşan kapalı bir şekil).
> - Poligon üzerinde tanımlı tüm Afin dönüşümleri birer fonksiyonla
>   gerçekleyin.
> - Programın bir GUI programı olması gerekmiyor. Çalıştırıldığında
>   dönüşüm fonksiyonlarının ürettiği yeni poligona ait koordinatları
>   döndürmesi veya ekranda görüntülemesi yeterlidir.

## Dosya yapısı

```
2d-affine-transformations/
├── point.py              # Point sınıfı (x, y) gerçel sayı çifti
├── polygon.py            # Polygon sınıfı (N kapalı nokta)
├── transformations.py    # Tüm afin dönüşüm fonksiyonları
├── main.py               # Demo: dönüşümleri uygular ve koordinatları yazar
├── tests.py              # Birim testleri (harici çerçeveye gerek yok)
├── README.md             # Bu dosya
└── .gitignore
```

## Çalıştırma

Python 3.8+ yeterlidir. Hiçbir paket kurulumu gerekmez.

```bash
# Demo programı:
python main.py

# Testler:
python tests.py
```



## Uygulanan afin dönüşümler

| Dönüşüm | Fonksiyon | Matris |
|---|---|---|
| Öteleme | `translate(P, tx, ty)` | T(tx, ty) |
| Ölçekleme | `scale(P, sx, sy, pivot=None)` | S(sx, sy) |
| Döndürme | `rotate(P, theta, pivot=None)` | R(theta) |
| Kayma | `shear(P, shx, shy, pivot=None)` | Sh(shx, shy) |
| x ekseni yansıması | `reflect_x_axis(P)` | F_x |
| y ekseni yansıması | `reflect_y_axis(P)` | F_y |
| Orijine göre yansıma | `reflect_origin(P)` | F_O |
| y = x doğrusuna yansıma | `reflect_line_y_eq_x(P)` | F_{y=x} |
| Genel doğru yansıması | `reflect_line(P, a, b, c)` | F_{ax+by+c=0} |
| Genel afin dönüşüm | `apply_general_affine(P, a, b, tx, c, d, ty)` | M |
| Birleşik dönüşüm | `compose(M1, M2, ...)` + `apply_matrix(P, M)` | M1·M2·... |

Tüm dönüşümler **3x3 homojen matrisler** üzerinden uygulanır. Sabit nokta
(pivot) etrafında dönüşüm için `about_point(M, pivot)` yardımcı
fonksiyonu kullanılır:

```
M_pivot = T(pivot) · M · T(-pivot)
```

## Tasarım kararları

- **Değişmezlik (Immutability):** `Point` ve `Polygon` `@dataclass(frozen=True)`
  ile tanımlanmıştır. Her dönüşüm yeni bir nesne döndürür; bu sayede
  zincirleme dönüşümler yan etki üretmez.
- **Homojen koordinatlar:** Tüm dönüşümler 3x3 matrislerle ifade edildiği
  için öteleme dahil her şey aynı çarpım altyapısıyla birleştirilebilir.
- **Bağımsızlık:** Yalnızca `math` modülü kullanılır. NumPy gibi harici
  paketlere ihtiyaç yoktur.

## Örnek çıktı

`python main.py` çağrısı, beşgen şeklinde örnek bir poligon üzerinde her
dönüşümü uygular ve sonucu konsola yazar. Aşağıda kısa bir kesit:

```
================================================================
  1) ÖTELEME (Translation)
================================================================

>>> translate(P, tx=3, ty=2)
    P0: (+4.0000, +2.0000)
    P1: (+3.3090, +2.9511)
    P2: (+2.1910, +2.5878)
    P3: (+2.1910, +1.4122)
    P4: (+3.3090, +1.0489)
```
