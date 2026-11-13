# 📘 Deterministički signali – Primjeri i `sis` modul

Ovaj repozitorij sadrži **programske kodove** i modul **`sis`** koji prate knjigu **_Deterministički signali_** autora **Emir Sokić** i **Melita Ahić-Đokić**  
📖 Izdavač: Univerzitet u Sarajevu - Elektrotehnički fakultet  
🆔 ISBN-13: 978-9926-575-14-4 (2026)

📗 Povezana knjiga: _Slučajni signali i procesi_ – kodovi se nalaze u repozitoriju [esokic/ssp](https://github.com/esokic/ssp).

---

## 📂 Struktura repozitorija

```
├── Primjeri/            # Svi primjeri iz knjige, po poglavljima (Jupyter notebook)
│   ├── Kodovi_p1.ipynb
│   ├── Kodovi_p2.ipynb
│   └── ...
├── sis.py               # Modul sis (namjenski implementiran za knjigu)
├── pyproject.toml       # Omogućava instalaciju: pip install git+https://github.com/esokic/sis.git
├── requirements.txt     # numpy, matplotlib, jupyter
└── README.md
```

---

## 🧩 Modul `sis`

`sis` (**S**ignali **i** **S**istemi) je Python modul razvijen kao podrška za izvođenje i vizualizaciju primjera iz knjige.  
Sva grafika u knjizi nacrtana je jednim pozivom funkcije `sis.dijagram()`, a modul sadrži i pomoćne funkcije za numeričku Fourierovu transformaciju.  
Modul je optimiziran za rad u **Jupyter Notebook** i **Google Colab** okruženjima.

---

## 🚀 Brzi početak

### 1️⃣ Otvorite primjer

☁️ **Google Colab (bez instalacije):**  
Kliknite na dugme **Open in Colab** uz željeno poglavlje u tabeli [Primjeri po poglavljima](#-primjeri-po-poglavljima).

💻 **Lokalno:**  
U terminalu pokrenite:

```bash
git clone https://github.com/esokic/sis.git
cd sis/Primjeri
pip install jupyter numpy matplotlib
jupyter notebook
```

(Komanda `pip install` je potrebna samo ako navedene biblioteke još nisu instalirane.)

---

### 2️⃣ Pokrenite ćelije

Prva ćelija svakog notebook-a sama priprema okruženje: ako modul `sis` još nije instaliran (npr. u Colab-u), automatski se instalira sa GitHub-a (potrebna je internet veza). Nikakva dodatna podešavanja nisu potrebna – dovoljno je pokrenuti ćelije redom.

```python
import numpy as np

# Modul sis (ako nije instaliran, npr. u Google Colab-u, instalira se automatski)
try:
    import sis
except ModuleNotFoundError:
    %pip install -q git+https://github.com/esokic/sis.git
    import sis

sis.FORMAT = "JUPYTER"    # prikaz grafika prilagodjen interaktivnom radu
```

---

### 3️⃣ Format prikaza grafika

📘 Napomena:

- `"JUPYTER"` format koristi se u svim primjerima i prilagođen je interaktivnom radu u Colab/Jupyter okruženju.

- `"BOOK"` format (podrazumijevana vrijednost u modulu) daje slike identične onima u knjizi: rezolucija 300 dpi i fiksna veličina 4.5 × 2.5 in. Može se uključiti u prvoj ćeliji, zamjenom reda `sis.FORMAT = "JUPYTER"` redom `sis.FORMAT = "BOOK"`.

- Osnovna boja dijagrama (`sis.BOJA`, podrazumijevano `'darkgreen'`) i veličina (`sis.SIRINA`, `sis.VISINA`) mogu se promijeniti na jednom mjestu, poslije importovanja modula.

---

## ☁️ Primjer upotrebe u Google Colab / Jupyter Notebook

- U Colab-u otvorite željeni notebook klikom na dugme **Open in Colab** (tabela ispod).

- Pokrenite ćelije redom (**Runtime → Run all**). Biblioteke `numpy` i `matplotlib` su u Colab-u već instalirane.

- Lokalno se primjeri pokreću iz foldera `Primjeri`.

---

## 📈 Funkcija `sis.dijagram()`

Jednim pozivom iscrtava dijagram: jednu ili više krivih, u obliku linije ili diskretnih uzoraka.

```python
sis.dijagram(t, x, naslov='u(t)')                        # kontinualni signal
sis.dijagram(n, x, tip='uzorci', naslov='x[n]')          # diskretna sekvenca ('stem')
sis.dijagram(t, x1, m=t, y=x2, naslov='Poređenje')       # dvije krive istog tipa

sis.dijagram(serije=[                                    # miješane krive
    dict(t=t,  x=aproks, tip='linija'),
    dict(t=t1, x=x1,     tip='uzorci'),
], naslov='Rekonstrukcija')
```

| Parametar | Značenje |
|---|---|
| `t, x` | osa (vrijeme ili indeks) i vrijednosti prve krive; `m, y` i `b, z` su druga i treća kriva |
| `serije` | lista rječnika `dict(t=..., x=..., tip=..., stil=..., marker=..., oznaka=...)` za miješane ili brojne krive |
| `tip` | `'linija'` (podrazumijevano) ili `'uzorci'` (diskretna sekvenca) |
| `nula` | tanka isprekidana linija na `y=0` (podrazumijevano `True`) |
| `marker` | oblik markera kod `tip='uzorci'` (`'o'`, `'s'`, `'^'`, `'D'`); inače se mijenjaju automatski |
| `x_labela, y_labela, naslov` | oznake osa i naslov; `x_labela` je `$t$` za linije, a `$n$` za uzorke |
| `xlim, ylim, xticks, yticks` | granice i oznake na osama (isto kao u Matplotlib-u) |
| `sirina, visina` | veličina pojedinačnog dijagrama |
| `lokacija_lgd` | položaj legende (podrazumijevano `'upper right'`) |

📘 Napomena:

- Dopunske krive (npr. analitičko rješenje uz numerički rezultat) crtaju se po konvenciji plavom bojom: `stil='b--'` (isprekidano) ili `stil='b:'` (tačkasto).

- Pomoćne funkcije se također nalaze u istom modulu, npr.: `sis.FT(x, t, w, ts)` i `sis.IFT(F, w, t, ws)` (numerička aproksimacija Fourierove transformacije i inverzne transformacije), te `sis.fft`, `sis.ifft`, `sis.fftshift`, `sis.ifftshift`, `sis.fftfreq` (iz `numpy.fft`).

---

## 📑 Primjeri po poglavljima

| Poglavlje | Notebook | Sadržaj | Colab |
|---|---|---|---|
| 1. Uvod | [`Kodovi_p1.ipynb`](Primjeri/Kodovi_p1.ipynb) | poziv `sis.dijagram()` i ekvivalentan Matplotlib kod | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p1.ipynb) |
| 2. Kontinualni signali i sistemi | [`Kodovi_p2.ipynb`](Primjeri/Kodovi_p2.ipynb) | Kodovi 2.1–2.8: specijalni signali, konvolucija | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p2.ipynb) |
| 3. Diskretni signali i sistemi | [`Kodovi_p3.ipynb`](Primjeri/Kodovi_p3.ipynb) | Kodovi 3.1–3.7: sekvence, konvolucija, impulsni i step odziv | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p3.ipynb) |
| 4. Aproksimacija kontinualnih signala | [`Kodovi_p4.ipynb`](Primjeri/Kodovi_p4.ipynb) | Kodovi 4.1–4.5: Walshove funkcije i aproksimacija | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p4.ipynb) |
| 5. Spektralna analiza periodičkih signala | [`Kodovi_p5.ipynb`](Primjeri/Kodovi_p5.ipynb) | Kodovi 5.1–5.6: Fourierov red, spektar | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p5.ipynb) |
| 6. Fourierova transformacija | [`Kodovi_p6.ipynb`](Primjeri/Kodovi_p6.ipynb) | Kodovi 6.1–6.5: FT specijalnih funkcija, inverzna FT | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p6.ipynb) |
| 7. Amplitudno impulsna modulacija | [`Kodovi_p7.ipynb`](Primjeri/Kodovi_p7.ipynb) | Kodovi 7.1–7.3: zvjezdasta funkcija, izvedena periodička funkcija | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p7.ipynb) |
| 8. DFT i FFT | [`Kodovi_p8.ipynb`](Primjeri/Kodovi_p8.ipynb) | Kodovi 8.1–8.4: koeficijenti Fourierovog reda, spektar, konvolucija pomoću DFT | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p8.ipynb) |
| 10. z-transformacija | [`Kodovi_p10.ipynb`](Primjeri/Kodovi_p10.ipynb) | Kodovi 10.1–10.2: rješavanje diferentnih jednačina rekurzijom | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esokic/sis/blob/main/Primjeri/Kodovi_p10.ipynb) |

📘 Napomena:  
Svaki primjer u notebook-u počinje komentarom `# Kod X.Y - ...`, koji odgovara oznaci koda u knjizi.

---

## 🛠️ Tehnologije

- Python 3.8+

- NumPy, Matplotlib

- Jupyter Notebook / Google Colab

---

## 📚 Reference

Emir Sokić, Melita Ahić-Đokić  
Deterministički signali,  
Univerzitet u Sarajevu - Elektrotehnički fakultet, 2026.  
ISBN-13: 978-9926-575-14-4 (2026)  
Link na knjigu: https://ebooks.unsa.ba/index.php/ebooks/catalog/book/89

---

## © Autorska prava

Sav sadržaj u ovom repozitoriju je namijenjen obrazovnoj i istraživačkoj upotrebi.  
Autorska prava pripadaju autorima knjige i Izdavaču (Univerzitet u Sarajevu - Elektrotehnički fakultet).
