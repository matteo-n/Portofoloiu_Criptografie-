from sympy import Matrix

def citeste_alfabet(fisier_alfabet):
    with open(fisier_alfabet, "r", encoding="utf-8") as f:
        alfabet = f.read().strip()
    alfabet = tuple(alfabet)
    return alfabet

def get_text(fisier_sursa):
    with open(fisier_sursa, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def write_text(fisier_destinatie, text):
    with open(fisier_destinatie, "w", encoding="utf-8") as f:
        f.write(text)

def criptare_Hill(text, n, a, b, alfabet):
    N = len(alfabet)
    char_to_index = {c: i for i, c in enumerate(alfabet)}
    if len(text) % n != 0:
        text += alfabet[0] * (n - len(text) % n)
    rezultat = ""
    for j in range(0, len(text), n):
        bloc = text[j:j + n]
        valori = []
        for c in bloc:
            if c not in char_to_index:
                c_upper = c.upper()
                if c_upper in char_to_index:
                    c = c_upper
                else:
                    raise ValueError(f"Character {c!r} is not in alfabet: {alfabet}")
            valori.append(char_to_index[c])
        mesaj = Matrix(valori)
        criptat = (a * mesaj + b) % N
        for c in criptat:
            rezultat += alfabet[int(c)]
    return rezultat
