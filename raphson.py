import numpy as np


# Výpočet dráhy tělesa po eliptické dráze v prostoru
def orbit(m0: float, e: float, a: float, inclination: float, ascension: float, n: int, acc=1.e-2, max_iter=100):
    m = np.linspace(m0, 2 * np.pi + m0, n)  # Generuje n hodnot střední anomálie od m0 přes celou dráhu (0–2π)
    ecc_anom = m.copy()  # Začátek iterace pro excentrickou anomálii (počáteční odhad = m)
    ecc_anom_old = 0  # Pro uložení hodnoty z předchozí iterace
    iter_count = 0  # Počet iterací

    # Newtonova metoda pro řešení Keplerovy rovnice pro každou pozici na dráze
    while acc < np.abs(ecc_anom - ecc_anom_old).max():
        ecc_anom_old = ecc_anom.copy()
        ecc_anom -= (ecc_anom - m - e * np.sin(ecc_anom)) / (1. - e * np.cos(ecc_anom))
        iter_count += 1
        if iter_count > max_iter:  # Pojistka proti nekonečné smyčce
            break

    # Převod excentrické anomálie na pravou anomálii (skutečnou pozici na elipse)
    theta = 2. * np.arctan2(
        np.sqrt(1. + e) * np.sin(ecc_anom / 2.),
        np.sqrt(1. - e) * np.cos(ecc_anom / 2.)
    )
    r = a * (1 - e * np.cos(ecc_anom))  # Vzdálenost od středu (ohniska) v daném bodě dráhy

    # Výpočet prostorových souřadnic (rotace elipsy podle ascension a inclination)
    theasc = theta - ascension
    x = r * (np.cos(ascension) * np.cos(theasc) - np.sin(ascension) * np.sin(theasc) * np.cos(inclination))
    z = r * (np.sin(ascension) * np.cos(theasc) + np.cos(ascension) * np.sin(theasc) * np.cos(inclination))
    y = r * (np.sin(theta - ascension) * np.sin(inclination))

    coord = np.array((x, y, z))  # Výsledné pole souřadnic [x, y, z] všech bodů dráhy
    return coord  # Vrací pole souřadnic celé dráhy v prostoru
