from math import gcd

def extended_gcd(a, b):
    """Algoritmul extins al lui Euclid pentru calcul invers modular."""
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def modinv(a, m):
    """Calculează inversa modulară a lui a modulo m."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} nu are invers modulo {m} (gcd={g})")
    return x % m

# ====================================================================
# MASSEY-OMURA: Protocol de transmitere sigura fara cheie preconvenita
# ====================================================================

def massey_omura_protocol():
    """
    Protocol Massey-Omura: permite Bob sa trimita un mesaj Alice
    fara sa se fie schimbat o cheie preconvenita.
    
    Principiu: Fiecare participant are o exponentiare si inversa ei.
    Mesajul trece prin 3 pasi de criptare/decriptare reciproca.
    """
    
    print("\n" + "=" * 70)
    print("PROTOCOLUL MASSEY-OMURA")
    print("=" * 70)
    
    # Parametri publici
    p = 61  # Numar prim
    phi_p = p - 1  # = 60 = 2^2 * 3 * 5
    
    print(f"\n[PARAMETRI PUBLICI]")
    print(f"  p = {p} (prim)")
    print(f"  phi(p) = {phi_p}")
    
    # Alegerea exponenților
    # Exponenții trebuie să fie coprimi cu phi(p)
    e_A = 7    # gcd(7, 60) = 1 ✓
    e_B = 11   # gcd(11, 60) = 1 ✓
    
    # Calculul inverselor
    d_A = modinv(e_A, phi_p)
    d_B = modinv(e_B, phi_p)
    
    print(f"\n[CHEI PRIVATE]")
    print(f"  Alice: e_A={e_A}, d_A={d_A}")
    print(f"    Verificare: {e_A}*{d_A} mod {phi_p} = {(e_A*d_A) % phi_p}")
    print(f"  Bob:   e_B={e_B}, d_B={d_B}")
    print(f"    Verificare: {e_B}*{d_B} mod {phi_p} = {(e_B*d_B) % phi_p}")
    
    # Mesajul
    M = 13
    print(f"\n[MESAJ ORIGINAL]")
    print(f"  M = {M}")
    
    # === PROTOCOL 3 PASI ===
    print(f"\n[PROTOCOL 3 PASI]")
    
    # Pasul 1: Alice cripteaza si trimite lui Bob
    C1 = pow(M, e_A, p)
    print(f"\n  [Pasul 1] Alice -> Bob")
    print(f"    C1 = M^e_A mod p = {M}^{e_A} mod {p} = {C1}")
    
    # Pasul 2: Bob cripteaza si trimite inapoi lui Alice
    C2 = pow(C1, e_B, p)
    print(f"\n  [Pasul 2] Bob -> Alice")
    print(f"    C2 = C1^e_B mod p = {C1}^{e_B} mod {p} = {C2}")
    
    # Pasul 3: Alice decripteaza si trimite inapoi lui Bob
    C3 = pow(C2, d_A, p)
    print(f"\n  [Pasul 3] Alice -> Bob")
    print(f"    C3 = C2^d_A mod p = {C2}^{d_A} mod {p} = {C3}")
    
    # Pasul 4: Bob decripteaza mesajul final
    M_recovered = pow(C3, d_B, p)
    print(f"\n  [Pasul 4] Bob decripteaza")
    print(f"    M = C3^d_B mod p = {C3}^{d_B} mod {p} = {M_recovered}")
    
    # Verificare
    print(f"\n[VERIFICARE]")
    print(f"  Mesaj original:  {M}")
    print(f"  Mesaj recuperat: {M_recovered}")
    status = "[OK] CORECT" if M == M_recovered else "[FAIL] EROARE"
    print(f"  {status}")
    
    print("=" * 70)


# ====================================================================
# DIFFIE-HELLMAN: Schimb de chei
# ====================================================================

def diffie_hellman_protocol():
    """
    Protocolul Diffie-Hellman permite doi participanti sa stabileasca
    o cheie secreta comuna fara sa se intalneasca si fara sa transmita
    direct aceasta cheie printr-un canal nesigur.
    """
    
    print("\n" + "=" * 70)
    print("PROTOCOLUL DIFFIE-HELLMAN")
    print("=" * 70)
    
    # Parametri publici
    p = 61  # Numar prim (generator al campului multiplicativ Z_p*)
    g = 2   # Generator (primitiva modulo p)
    
    print(f"\n[PARAMETRI PUBLICI]")
    print(f"  p = {p} (prim)")
    print(f"  g = {g} (generator)")
    
    # Chei private (secrete)
    a = 7   # Cheia secreta a lui Alice
    b = 11  # Cheia secreta a lui Bob
    
    print(f"\n[CHEI PRIVATE]")
    print(f"  Alice: a = {a}")
    print(f"  Bob:   b = {b}")
    
    # === SCHIMB DE CHEI ===
    print(f"\n[SCHIMB PUBLIC DE CHEI]")
    
    # Alice calculeaza si trimite cheia publica
    A = pow(g, a, p)
    print(f"\n  Alice calculeaza: A = g^a mod p = {g}^{a} mod {p} = {A}")
    print(f"  Alice trimite lui Bob: A = {A}")
    
    # Bob calculeaza si trimite cheia publica
    B = pow(g, b, p)
    print(f"\n  Bob calculeaza: B = g^b mod p = {g}^{b} mod {p} = {B}")
    print(f"  Bob trimite lui Alice: B = {B}")
    
    # === CALCUL CHEIE COMUNA ===
    print(f"\n[CALCUL CHEIE COMUNA]")
    
    # Alice calculeaza cheia comuna
    kA = pow(B, a, p)
    print(f"\n  Alice calculeaza: k = B^a mod p = {B}^{a} mod {p} = {kA}")
    
    # Bob calculeaza cheia comuna
    kB = pow(A, b, p)
    print(f"  Bob calculeaza:   k = A^b mod p = {A}^{b} mod {p} = {kB}")
    
    # Verificare
    print(f"\n[VERIFICARE]")
    print(f"  Cheia Alice: {kA}")
    print(f"  Cheia Bob:   {kB}")
    status = "[OK] CORECT - Chei identice!" if kA == kB else "[FAIL] EROARE"
    print(f"  {status}")
    
    print("=" * 70)


def explicatii():
    """Afiseaza explicatii despre protocoalele implementate."""
    
    print("\n" + "=" * 70)
    print("EXPLICATII: MASSEY-OMURA SI DIFFIE-HELLMAN")
    print("=" * 70)
    
    print(f"""
1. PROTOCOLUL MASSEY-OMURA
===========================

Scop: Transmiterea sigura a unui mesaj fara intelegere prealabila a cheii.

Principiu (metafora "lacatul"):
  - Alice si Bob fiecare au "lacatul si cheia" proprie
  - Mesajul e un colet care trece prin 3 pasi
  
Pasi:
  1. Alice cripteaza: M -> C1 = M^e_A mod p
  2. Bob adauga criptare: C1 -> C2 = C1^e_B mod p (mesaj dublu criptat)
  3. Alice decripteaza-si lacatul: C2 -> C3 = C2^d_A mod p
  4. Bob decripteaza final: C3 -> M = C3^d_B mod p

Securitate:
  - Fara e_A, d_A nu poti elimina criptarea lui Alice
  - Fara e_B, d_B nu poti elimina criptarea lui Bob
  - Intermediari vad doar C1, C2, C3 (valori puterii)

Limitari:
  - Presupune grup ciclic (Z_p* cu p prim)
  - Ataci: Pohlig-Hellman daca p-1 are factori mici


2. PROTOCOLUL DIFFIE-HELLMAN
=============================

Scop: Stabilire de cheie secreta comuna printr-un canal nesigur.

Principiu (integrare puteri):
  - Alice: alege a secret, calculeaza A = g^a mod p (public)
  - Bob: alege b secret, calculeaza B = g^b mod p (public)
  - Cheia comuna: k = g^(ab) mod p
  
Pasi:
  1. Alice trimite A, Bob trimite B (public)
  2. Alice calculeaza: k = B^a mod p = (g^b)^a = g^(ab)
  3. Bob calculeaza: k = A^b mod p = (g^a)^b = g^(ab)
  4. Ambii au aceeasi cheie k!

De ce functioneaza:
  - Ei pot calcula g^(ab) fiecare cu datele lor
  - Oricine cunoaste doar A, B, g, p nu poate calcula ab usor
  
Securitate:
  - Bazat pe greu al Discrete Logarithm Problem
  - Problema: logaritm discret e NP-hard
  - Ataci: Pohlig-Hellman, Number Field Sieve

Vulnerabilitate (MITM - Man in the Middle):
  - Atacator poate intercpta A, B si invaloca proprii parametri
  - Solutie: Autentificare cu certificate digitale (TLS/SSL)


3. DIFERENTE
=============

Massey-Omura:
  - Transmitere sigura A -> B (3 pasi)
  - Ambii trebuie sa fie online
  - Mesaj cunoscut dinainte
  
Diffie-Hellman:
  - Stabilire cheie comuna (simetrica)
  - Pentru comunicatie ulterioara
  - Fara mesaj, doar paramentri

Aplicatii moderne:
  - HTTPS/TLS: Diffie-Hellman pentru key exchange
  - GPG/PGP: RSA/ECC pentru directa, apoi simetrica
  - Massey-Omura: Putini folositi (considerat deprecated)
""")
    print("=" * 70)


if __name__ == "__main__":
    # Demonstratii
    massey_omura_protocol()
    diffie_hellman_protocol()
    
    # Explicatii
    explicatii()
    
    print("\n[OK] Programul s-a executat cu succes!\n")
