"""
ElGamal Cryptosystem - Implementare Python
Seminar 9 - Criptosisteme cu cheie publica

Suporta:
  - Generare chei
  - Criptare text (litera -> index in alfabet -> ElGamal)
  - Decriptare text (cu cheie publica + privata si mesaj criptat)
  - Alfabet din fisier alfabet.txt (orice format)
"""

import random
import sys
import io
import os
import re

# Fix encoding pentru terminal Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ─────────────────────────────────────────
#  Matematica de baza
# ─────────────────────────────────────────

def modpow(base, exp, mod):
    return pow(base, exp, mod)


def mod_inverse(a, m):
    old_r, r = a, m
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if old_r != 1:
        raise ValueError(f"{a} nu are invers modular fata de {m}")
    return old_s % m


def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_primitive_root(p):
    phi = p - 1
    factors = set()
    n = phi
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    for g in range(2, p):
        if all(modpow(g, phi // f, p) != 1 for f in factors):
            return g
    raise ValueError(f"Nu s-a gasit generator pentru p={p}")


# ─────────────────────────────────────────
#  Citire alfabet din fisier
# ─────────────────────────────────────────

def load_alphabet(filepath="alfabet.txt"):
    """
    Citeste alfabetul din fisier. Detecteaza automat formatul:
      - O litera/simbol per linie
      - Toate pe un rand separate prin spatiu
      - Toate lipite (ABCD...)
    Returneaza lista ordonata de simboluri si dictionarul simbol->index.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Fisierul '{filepath}' nu a fost gasit!\n"
            f"Creaza fisierul '{filepath}' in acelasi folder cu scriptul."
        )

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    lines = [l.strip() for l in content.splitlines() if l.strip()]
    symbols = []

    if len(lines) > 1:
        # Fiecare linie = un simbol (sau mai multe separate prin spatiu)
        for line in lines:
            parts = line.split()
            if len(parts) > 1:
                symbols.extend(parts)
            else:
                symbols.append(line)
    else:
        # Tot pe o singura linie
        single = lines[0]
        if " " in single:
            symbols = single.split()
        else:
            symbols = list(single)

    if not symbols:
        raise ValueError(f"Alfabetul din '{filepath}' este gol!")

    char_to_idx = {ch: i for i, ch in enumerate(symbols)}
    return symbols, char_to_idx


# ─────────────────────────────────────────
#  ElGamal pe numere
# ─────────────────────────────────────────

def generate_keys(p=None, g=None, x=None):
    if p is None:
        p = 23
    if not is_prime(p):
        raise ValueError(f"p={p} nu este numar prim!")
    if g is None:
        g = find_primitive_root(p)
    if g < 2 or g >= p:
        raise ValueError(f"g={g} trebuie sa fie in [2, p-1]")
    if x is None:
        x = random.randint(2, p - 2)
    if x < 2 or x > p - 2:
        raise ValueError(f"x={x} trebuie sa fie in [2, p-2]")
    y = modpow(g, x, p)
    return (p, g, y), (p, g, x)


def encrypt_num(public_key, m, k=None):
    p, g, y = public_key
    if m < 1 or m >= p:
        raise ValueError(
            f"Indexul m={m} trebuie sa fie in [1, p-1]=[1, {p-1}].\n"
            f"  -> Verifica ca p > numarul de simboluri din alfabet."
        )
    if k is None:
        k = random.randint(2, p - 2)
    else:
        if k < 2 or k > p - 2:
            raise ValueError(f"k={k} trebuie sa fie in [2, p-2]")
    c1 = modpow(g, k, p)
    c2 = (m * modpow(y, k, p)) % p
    return c1, c2, k


def decrypt_num(private_key, c1, c2):
    p, g, x = private_key
    s = modpow(c1, x, p)
    s_inv = mod_inverse(s, p)
    m = (c2 * s_inv) % p
    return m


# ─────────────────────────────────────────
#  Criptare / Decriptare text
# ─────────────────────────────────────────

def encrypt_text(public_key, plaintext, alphabet, char_to_idx, k=None):
    """
    Cripteaza un text litera cu litera.
    Litera -> index 1-based -> pereche (c1, c2).
    """
    pairs = []
    ks = []
    unknown = []
    for ch in plaintext:
        if ch not in char_to_idx:
            unknown.append(repr(ch))
            continue
        idx = char_to_idx[ch] + 1  # 1-based (evitam m=0)
        c1, c2, k_used = encrypt_num(public_key, idx, k)
        pairs.append((c1, c2))
        ks.append(k_used)
    if unknown:
        print(f"  [Atentie] Simboluri negasite in alfabet (ignorate): {', '.join(set(unknown))}")
    return pairs, ks


def decrypt_text(private_key, pairs, alphabet):
    """
    Decripteaza o lista de perechi (c1, c2) -> text.
    """
    result = []
    for c1, c2 in pairs:
        idx = decrypt_num(private_key, c1, c2)
        real_idx = idx - 1  # inapoi la 0-based
        if 0 <= real_idx < len(alphabet):
            result.append(alphabet[real_idx])
        else:
            result.append(f"[?{idx}]")
    return "".join(result)


def parse_ciphertext(raw):
    """
    Parseaza mesajul criptat introdus de utilizator.
    Accepta:
      - Perechi:  (5,18) (21,3) (7,14)
      - Numere:   5,18,21,3,7,14
    """
    perechi = re.findall(r'\(?\s*(\d+)\s*,\s*(\d+)\s*\)?', raw)
    if perechi:
        return [(int(a), int(b)) for a, b in perechi]
    nums = [int(x) for x in re.findall(r'\d+', raw)]
    if len(nums) % 2 != 0:
        raise ValueError("Numarul de valori este impar - nu se pot forma perechi (c1,c2)!")
    return [(nums[i], nums[i+1]) for i in range(0, len(nums), 2)]


# ─────────────────────────────────────────
#  Meniu principal
# ─────────────────────────────────────────

def sep(title=""):
    w = 57
    if title:
        pad = (w - len(title) - 2) // 2
        print("=" * pad + f" {title} " + "=" * (w - pad - len(title) - 2))
    else:
        print("=" * w)


def main():
    sep("ElGamal cu Alfabet")

    # Incarcare alfabet
    try:
        alphabet, char_to_idx = load_alphabet("alfabet.txt")
        print(f"\n  Alfabet incarcat: {len(alphabet)} simboluri")
        preview = " ".join(alphabet[:20])
        if len(alphabet) > 20:
            preview += " ..."
        print(f"  Simboluri: {preview}")
    except FileNotFoundError as e:
        print(f"\n  EROARE: {e}")
        sys.exit(1)

    while True:
        print()
        sep()
        print("  1. Generare chei")
        print("  2. Criptare text")
        print("  3. Decriptare text  <-- primesti (c1,c2) de la alta echipa")
        print("  4. Demo complet automat")
        print("  0. Iesire")
        sep()
        opt = input("  Alege optiunea: ").strip()

        # ── Generare chei ──────────────────────────────────────
        if opt == "1":
            print()
            print(f"  [Info] Alfabetul tau are {len(alphabet)} simboluri.")
            print(f"         Alege p > {len(alphabet)} (numar prim).")
            p = int(input("  p: "))
            if not is_prime(p):
                print(f"  EROARE: {p} nu este numar prim!")
                continue
            if p <= len(alphabet):
                print(f"  EROARE: p={p} trebuie sa fie mai mare decat numarul de simboluri ({len(alphabet)})!")
                continue
            g_in = input("  g (generator, lasa gol = auto): ").strip()
            g = int(g_in) if g_in else None
            x_in = input("  x (cheie privata, lasa gol = aleator): ").strip()
            x = int(x_in) if x_in else None
            pub, priv = generate_keys(p=p, g=g, x=x)
            p_, g_, y = pub
            _, _, x_ = priv
            print(f"\n  Cheie PUBLICA  : p={p_}  g={g_}  y={y}")
            print(f"  Cheie PRIVATA  : x={x_}")
            print(f"  (y = {g_}^{x_} mod {p_} = {y})")

        # ── Criptare text ──────────────────────────────────────
        elif opt == "2":
            print()
            p = int(input("  p: "))
            g = int(input("  g: "))
            y = int(input("  y: "))
            pub = (p, g, y)

            k_in = input("  k (lasa gol = aleator per litera | numar = k fix): ").strip()
            k = int(k_in) if k_in else None

            text = input("  Text de criptat: ")
            try:
                pairs, ks = encrypt_text(pub, text, alphabet, char_to_idx, k=k)
            except ValueError as e:
                print(f"  EROARE: {e}")
                continue

            # Afisare detaliata
            print(f"\n  Text original  : {text}")
            print(f"  {'Litera':<8} {'Idx':>5}  {'k':>5}  {'c1':>6}  {'c2':>6}")
            print(f"  {'-'*8} {'-'*5}  {'-'*5}  {'-'*6}  {'-'*6}")
            valid_chars = [ch for ch in text if ch in char_to_idx]
            for i, ((c1, c2), ki) in enumerate(zip(pairs, ks)):
                ch = valid_chars[i]
                idx = char_to_idx[ch] + 1
                print(f"  {repr(ch):<8} {idx:>5}  {ki:>5}  {c1:>6}  {c2:>6}")

            flat = " ".join(f"({c1},{c2})" for c1, c2 in pairs)
            print(f"\n  Text criptat   : {flat}")

        # ── Decriptare text ────────────────────────────────────
        elif opt == "3":
            print()
            print("  -- Introduceti cheile si mesajul criptat --")
            p = int(input("  p: "))
            g = int(input("  g: "))
            y = int(input("  y (cheie publica): "))
            x = int(input("  x (cheie privata): "))
            priv = (p, g, x)

            print()
            print("  Mesaj criptat (acceptat: '(5,18) (21,3)' sau '5,18,21,3'):")
            raw = input("  > ")
            try:
                pairs = parse_ciphertext(raw)
            except ValueError as e:
                print(f"  EROARE la parsare: {e}")
                continue

            plaintext = decrypt_text(priv, pairs, alphabet)
            print(f"\n  Mesaj decriptat: {plaintext}")

        # ── Demo complet ───────────────────────────────────────
        elif opt == "4":
            print()
            # Gasim un p potrivit
            p = len(alphabet) + 2
            while not is_prime(p):
                p += 1
            pub, priv = generate_keys(p=p, x=None)
            p_, g_, y = pub
            _, _, x_ = priv
            print(f"  p={p_}, g={g_}, y={y}, x={x_}")

            # Primele 5 simboluri din alfabet
            sample = "".join(alphabet[:min(5, len(alphabet))])
            print(f"  Text de test   : '{sample}'")

            pairs, ks = encrypt_text(pub, sample, alphabet, char_to_idx)
            print(f"  {'Litera':<8} {'Idx':>5}  {'k':>5}  {'c1':>6}  {'c2':>6}")
            print(f"  {'-'*8} {'-'*5}  {'-'*5}  {'-'*6}  {'-'*6}")
            for i, ((c1, c2), ki) in enumerate(zip(pairs, ks)):
                ch = sample[i]
                print(f"  {repr(ch):<8} {char_to_idx[ch]+1:>5}  {ki:>5}  {c1:>6}  {c2:>6}")

            recovered = decrypt_text(priv, pairs, alphabet)
            print(f"\n  Decriptat      : '{recovered}'")
            ok = "OK" if recovered == sample else "EROARE"
            print(f"  Verificare     : {ok}")

        elif opt == "0":
            print("  La revedere!")
            break
        else:
            print("  Optiune invalida.")


if __name__ == "__main__":
    main()
