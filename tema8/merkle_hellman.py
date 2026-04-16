"""
Implementare Criptosistemul Merkle-Hellman (Knapsack)
Aplicare pentru mesaje cu alfabetul A-Z (26 caractere)
"""

def mod_inv(a, m):
    """Calculeaza inversul modular al lui a mod m folosind algoritmul extins al lui Euclid."""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError(f"Inversa nu exista: gcd({a}, {m}) = {gcd}")
    return (x % m + m) % m


def char_to_bits(c):
    """
    Converteste caracter (A-Z) in reprezentare binara pe 5 biti.
    A=0 -> 00000, B=1 -> 00001, ..., Z=25 -> 11001
    """
    code = ord(c.upper()) - ord('A')
    if not (0 <= code <= 25):
        raise ValueError(f"Caracter invalid: {c}. Doar A-Z sunt acceptate.")
    return [(code >> i) & 1 for i in range(5)]


def bits_to_char(bits):
    """Converteste 5 biti in caracter A-Z."""
    code = 0
    for i in range(5):
        code += bits[i] * (2 ** i)
    if not (0 <= code <= 25):
        raise ValueError(f"Cod invalid: {code}")
    return chr(ord('A') + code)


def encrypt_char(c, public_key):
    """
    Cripteaza un caracter folosind cheia publica.
    C = suma(bit_i * public_key_i)
    """
    bits = char_to_bits(c)
    ciphertext = sum(bits[i] * public_key[i] for i in range(5))
    return ciphertext


def knapsack_decode(target, supercreating_sequence):
    """
    Rezolva problema rucsacului: gaseste care elemente din secventa
    supercrescatoare se insumeaza la target.
    Returneaza lista de biti (0/1).
    
    Pentru o secventa supercrescatoare, solutia este unica si se gaseste
    greedy de la dreapta la stanga.
    """
    bits = [0] * len(supercreating_sequence)
    remaining = target
    
    for i in range(len(supercreating_sequence) - 1, -1, -1):
        if remaining >= supercreating_sequence[i]:
            bits[i] = 1
            remaining -= supercreating_sequence[i]
    
    if remaining != 0:
        raise ValueError(f"Imposibil de decriptat: {target} nu poate fi reprezentat")
    
    return bits


def decrypt_char(ciphertext, b, m, private_key):
    """
    Decripteaza un bloc criptat.
    1. Se calculeaza M' = C * b mod m
    2. Se rezolva problema rucsacului cu cheia privata
    3. Se converteste de la biti la caracter
    """
    # Pasul 1: Aplicare transformata inversa
    transformed = (ciphertext * b) % m
    
    # Pasul 2: Rezolvare problema rucsac cu cheia supercrescatoare
    bits = knapsack_decode(transformed, private_key)
    
    # Pasul 3: Conversie biti -> caracter
    return bits_to_char(bits)


def merkle_hellman_demo():
    """Demonstratie criptosistem Merkle-Hellman."""
    
    print("=" * 70)
    print("CRIPTOSISTEMUL MERKLE-HELLMAN (KNAPSACK)")
    print("=" * 70)

    private_key = [2, 3, 6, 12, 24]  # 3>2, 6>2+3=5, 12>2+3+6=11, 24>2+3+6+12=23
    
    # Parametri de transformare: b si m
    b = 13  # Inversa multiplicativa
    m = 53  # Modulus (trebuie sa fie > suma(private_key) = 47)
    
    # Calculam a = inversa lui b modulo m
    a = mod_inv(b, m)
    
    # Cheia publica: B[i] = (a * private_key[i]) mod m
    public_key = [(a * s) % m for s in private_key]
    
    print(f"\n[SETUP - GENERARE CHEI]")
    print(f"  Secventa supercrescatoare (privata): {private_key}")
    print(f"  Parametru a: {a}")
    print(f"  Parametru b (inversa lui a mod m): {b}")
    print(f"  Modulus m: {m}")
    print(f"  Verificare: a * b mod m = {(a * b) % m} (trebuie sa fie 1)")
    print(f"  Cheia publica (transformata): {public_key}")
    
    # --- CRIPTARE ---
    message = "WHY"
    print(f"\n[MESAJ ORIGINAL]")
    print(f"  {message}")
    
    print(f"\n[CRIPTARE]")
    print(f"  Pentru fiecare caracter: convertor in 5 biti, apoi C = suma(bit_i * public_key_i)")
    
    ciphertext = []
    for c in message:
        code = ord(c.upper()) - ord('A')
        bits = char_to_bits(c)
        encrypted = encrypt_char(c, public_key)
        ciphertext.append(encrypted)
        
        bit_str = ''.join(str(b) for b in bits)
        print(f"  {c} (cod={code:2d}, binar={bit_str})")
        terms = ' + '.join(f"{bits[i]}*{public_key[i]}" for i in range(5) if bits[i])
        print(f"    C = {terms} = {encrypted}")
    
    print(f"\n  Mesaj criptat: {ciphertext}")
    
    # --- DECRIPTARE ---
    print(f"\n[DECRIPTARE]")
    print(f"  Pentru fiecare valoare criptata C:")
    print(f"  1. Calculeaza M' = C * b mod m")
    print(f"  2. Rezolva problema rucsacului cu cheia privata")
    print(f"  3. Converteste de la biti la caracter")
    
    decrypted_message = ""
    for c_val in ciphertext:
        transformed = (c_val * b) % m
        bits = knapsack_decode(transformed, private_key)
        dec_char = bits_to_char(bits)
        decrypted_message += dec_char
        
        code = ord(dec_char) - ord('A')
        bit_str = ''.join(str(b) for b in bits)
        print(f"  C={c_val:3d} -> M'={(c_val * b) % m:2d} -> bits={bit_str} -> {dec_char} (cod={code:2d})")
    
    print(f"\n[REZULTAT]")
    print(f"  Mesaj original:  {message}")
    print(f"  Mesaj decriptat: {decrypted_message}")
    status = "[OK] CORECT" if message == decrypted_message else "[FAIL] EROARE"
    print(f"  {status}")
    print("=" * 70)
    
    return message, ciphertext, decrypted_message


def merkle_hellman_custom():
    """Permite utilizatorului sa cripteze orice mesaj cu cheile date."""
    
    private_key = [2, 3, 6, 12, 24]
    b = 13
    m = 53
    a = mod_inv(b, m)
    public_key = [(a * s) % m for s in private_key]
    
    print("\n" + "=" * 70)
    print("CRIPTARE PERSONALIZATA")
    print("=" * 70)
    
    message = input("Introduceti mesajul (A-Z): ").strip().upper()
    
    if not all(c.isalpha() and 'A' <= c <= 'Z' for c in message):
        print("Eroare: mesajul trebuie sa contina doar litere A-Z")
        return
    
    print(f"\nMessaj: {message}")
    ciphertext = []
    
    print("\n[Criptare]")
    for c in message:
        encrypted = encrypt_char(c, public_key)
        ciphertext.append(encrypted)
        bits = char_to_bits(c)
        code = ord(c) - ord('A')
        print(f"  {c} (cod={code:2d}) -> biți={bits} -> criptat={encrypted}")
    
    print(f"\nText criptat: {ciphertext}")
    
    print("\n[Decriptare]")
    decrypted = ""
    for c_val in ciphertext:
        dec_char = decrypt_char(c_val, b, m, private_key)
        decrypted += dec_char
        code = ord(dec_char) - ord('A')
        print(f"  {c_val:3d} -> {dec_char} (cod={code:2d})")
    
    print(f"\nMessaj recuperat: {decrypted}")


def explicatii():
    """Afiseaza explicatii despre criptosistemul Merkle-Hellman."""
    
    print("\n" + "=" * 70)
    print("EXPLICATII: CRIPTOSISTEMUL MERKLE-HELLMAN")
    print("=" * 70)

if __name__ == "__main__":
    # Demonstratie cu mesajul din cerinta
    merkle_hellman_demo()
    
    # Explicatii detaliate
    explicatii()
   
