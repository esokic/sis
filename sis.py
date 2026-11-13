"""
sis - modul za graficki prikaz uz knjigu "Deterministicki signali"
Autori: Emir Sokic, Melita Ahic-Djokic

Sva grafika u knjizi se crta jednim pozivom funkcije dijagram().
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq  # sis.fft(...) itd.

# Na starijim verzijama matplotlib-a (prije potpunog uklanjanja
# use_line_collection parametra) stem() zna izbaciti bezopasno
# upozorenje o internom nacinu iscrtavanja - utisano je ovdje.
warnings.filterwarnings('ignore', message='In Matplotlib 3.3 individual lines.*')

# ----------------------------------------------------------------
# Podesavanje prikaza
# ----------------------------------------------------------------
FORMAT  = "BOOK"     # "BOOK" / "JUPYTER"
FIG_DPI = 300        # rezolucija pri exportu (samo FORMAT="BOOK")

SIRINA = 4.5   # sirina grafika u inchima (= \textwidth knjige, B5) - FIKSNO
VISINA = 2.5   # ukupna visina grafika u inchima - FIKSNO, po potrebi
               # se moze promijeniti pojedinacno preko visina=... u pozivu
BOJA   = 'darkgreen' #'firebrick'#'orange'   # osnovna boja svih dijagrama (jedno mjesto za promjenu)

_LINIJE  = ['-', '--', ':', '-.']    # stilovi linije (boja odvojeno, vidi nize)
_MARKERI = ['o', '^', 's', 'D']      # oblici markera kod tip='uzorci'
VELICINA_MARKERA = 4    # velicina kruzica/markera kod tip='uzorci'


def _jedna_serija(ax, t, x, tip, indeks, stil, oznaka, marker=None):
    """Iscrtava jednu krivu (liniju ili diskretnu sekvencu) u datom axes-u."""
    if tip == 'linija':
        if stil is not None:
            ax.plot(t, x, stil, label=oznaka)          # npr. stil='b--'
        else:
            ax.plot(t, x, color=BOJA, linestyle=_LINIJE[indeks % 4],
                    label=oznaka)
    else:  # 'uzorci'
        mk   = marker if marker is not None else _MARKERI[indeks % 4]
        boja = stil if stil is not None else BOJA
        markerline, stemlines, baseline = ax.stem(t, x, basefmt=' ',
                                                    label=oznaka)
        markerline.set(color=boja, marker=mk, markerfacecolor=boja, markersize=VELICINA_MARKERA)
        if isinstance(stemlines, (list, tuple)):
            for linija in stemlines:      # starije verzije matplotlib-a
                linija.set_color(boja)
        else:
            stemlines.set_color(boja)     # novije verzije (LineCollection)


def dijagram(t=None, x=None, m=None, y=None, b=None, z=None,
             serije=None, tip='linija', nula=True, marker=None,
             x_labela=None, y_labela=None, naslov=None,
             lokacija_lgd='upper right',
             xlim=None, ylim=None, xticks=None, yticks=None,
             sirina=None, visina=None):
    """
    Iscrtava dijagram - jednim pozivom funkcije.

    Jednostavan slucaj (1-3 krive u istom dijagramu):
        sis.dijagram(t, x, naslov="u(t)")
        sis.dijagram(t, x, m=t, y=x2, tip='uzorci', naslov="f[n]")

    Mijesane krive (npr. linija + uzorci u istom dijagramu):
        sis.dijagram(serije=[
            dict(t=t, x=aprox, tip='linija'),
            dict(t=t1, x=x1, tip='uzorci'),
        ], naslov="Rekonstrukcija")

    Rucno postavljanje markera kod uzoraka (umjesto automatskog):
        sis.dijagram(t, x, tip='uzorci', marker='s')
        sis.dijagram(serije=[
            dict(t=t, x=x1, tip='uzorci'),                # automatski 'o'
            dict(t=t, x=x2, tip='uzorci', marker='D'),     # rucno postavljen
        ])

    x_labela je po defaultu '$t$' za tip='linija', a '$n$' za tip='uzorci'
    (osim ako se eksplicitno zada drugacije, npr. x_labela=r'$\\omega$').

    Nulta linija (isprekidana, crna) se crta po defaultu; iskljucuje se
    sa nula=False.
    """
    if serije is None:
        serije = []
        for par in [(t, x), (m, y), (b, z)]:
            if par[1] is not None:
                serije.append(dict(t=par[0], x=par[1], tip=tip, marker=marker))

    if x_labela is None:
        prvi_tip = serije[0].get('tip', tip) if serije else tip
        x_labela = '$n$' if prvi_tip == 'uzorci' else '$t$'

    if sirina is None:
        sirina = SIRINA
    if visina is None:
        visina = VISINA

    fig, ax = plt.subplots(figsize=(sirina, visina))
    if FORMAT == "BOOK":
        fig.set_dpi(FIG_DPI)

    ima_oznaku = False
    for i, s in enumerate(serije):
        oznaka = s.get('oznaka')
        ima_oznaku = ima_oznaku or (oznaka is not None)
        _jedna_serija(ax, s['t'], s.get('x'), s.get('tip', tip),
                      i, s.get('stil'), oznaka, s.get('marker'))

    if nula and serije:
        ax.axhline(0, color='k', linewidth=0.5, linestyle='--')

    ax.set_xlabel(x_labela)
    if y_labela is not None:
        ax.set_ylabel(y_labela)
    if naslov is not None:
        ax.set_title(naslov)
    if ima_oznaku:
        ax.legend(loc=lokacija_lgd, framealpha=1)
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)

    plt.tight_layout()
    plt.show()


def FT(x, t, w, ts):
    """Numericka aproksimacija Fourierove transformacije."""
    c = np.zeros(len(w), dtype=complex)
    for k, wk in enumerate(w):
        c[k] = ts * np.sum(x * np.exp(-1j * wk * t))
    return c


def IFT(F, w, t, ws):
    """Numericka aproksimacija inverzne Fourierove transformacije."""
    f = np.zeros(len(t), dtype=complex)
    for k, tk in enumerate(t):
        f[k] = ws / (2 * np.pi) * np.sum(F * np.exp(1j * w * tk))
    return f
