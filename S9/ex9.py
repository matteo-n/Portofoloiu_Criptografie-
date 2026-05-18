import random

def cmmdc(a, b):
    """Calculeaza cel mai mare divizor comun."""
    while b:
        a, b = b, a % b
    return a

def cmmmc(a, b):
    """Calculeaza cel mai mic multiplu comun."""
    return (a * b) // cmmdc(a, b)

def euclid_extins(a, b):
    """Algoritmul lui Euclid Extins pentru calculul inversului modular."""
    if a == 0:
        return b, 0, 1
    g, x1, y1 = euclid_extins(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def invers_modular(a, m):
    """Calculeaza inversul modular: a^(-1) mod m."""
    g, x, y = euclid_extins(a, m)
    if g != 1:
        raise ValueError(f"Inversul modular nu exista.")
    return x % m

class Paillier:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se aleg doua numere prime mari p si q (distincte).
        Se calculeaza n = p * q si lambda_val = cmmmc(p-1, q-1).
        Se alege un g oarecare din Z*_(n^2). In varianta standard simplificata, g = n + 1.
        """
        p = 191
        q = 193
        n = p * q
        n_patrat = n ** 2
        lambda_val = cmmmc(p - 1, q - 1)
        g = n + 1
        def L(x):
            return (x - 1) // n
            
        u = invers_modular(L(pow(g, lambda_val, n_patrat)), n)
        
        cheie_publica = (n, g)
        cheie_privata = (lambda_val, u)
        
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(m, cheie_publica):
        """
        Pasul 2: Criptare
        C = (g^m * r^n) mod n^2
        Mesajul m trebuie sa fie din intervalul [0, n).
        """
        n, g = cheie_publica
        n_patrat = n ** 2
        
        if not (0 <= m < n):
            raise ValueError(f"Mesajul trebuie sa fie in intervalul [0, {n})")
            
        while True:
            r = random.randint(2, n - 1)
            if cmmdc(r, n) == 1:
                break
                
        termen1 = pow(g, m, n_patrat)
        termen2 = pow(r, n, n_patrat)
        c = (termen1 * termen2) % n_patrat
        
        return c

    @staticmethod
    def decriptare(c, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptare
        m = ( L(c^lambda mod n^2) * u ) mod n
        Unde L(x) = (x - 1) / n
        """
        n, g = cheie_publica
        lambda_val, u = cheie_privata
        n_patrat = n ** 2
        
        def L(x):
            return (x - 1) // n
            
        c_lambda = pow(c, lambda_val, n_patrat)
        
        m = (L(c_lambda) * u) % n
        return m

if __name__ == "__main__":
    print("--- Criptosistemul Paillier ---\n")
    
    pub_key, priv_key = Paillier.genereaza_chei()
    n_pub, g_pub = pub_key
    
    print(f"[Cheie Publica] Modulul n = {n_pub} (n^2 = {n_pub**2})")
    print(f"[Cheie Publica] Generatorul g = {g_pub}\n")
    print(f"[Cheie Privata] Lambda = {priv_key[0]}")
    print(f"[Cheie Privata] u (Invers modular) = {priv_key[1]}\n")
    
    m1 = 150
    m2 = 230
    print(f"-> Mesajul 1 in clar (m1) = {m1}")
    print(f"-> Mesajul 2 in clar (m2) = {m2}\n")
    
    c1 = Paillier.criptare(m1, pub_key)
    c2 = Paillier.criptare(m2, pub_key)
    print(f"-> Criptotext 1 (c1) = {c1}")
    print(f"-> Criptotext 2 (c2) = {c2}\n")
    
    m1_decriptat = Paillier.decriptare(c1, pub_key, priv_key)
    print(f"-> Decriptare clasica standard c1 = {m1_decriptat}")
    
    c_adunat = (c1 * c2) % (n_pub ** 2)
    
    m_adunat_decriptat = Paillier.decriptare(c_adunat, pub_key, priv_key)
    print(f"\n--- Demonstratie Proprietate Omomorfica ---")
    print(f"-> Inmultim criptotextul c1 cu c2 (c_adunat) = {c_adunat}")
    print(f"-> Rezultatul decriptarii lui c_adunat       = {m_adunat_decriptat}")
    print(f"-> Verificare matematica: {m1} + {m2}         = {m1 + m2}")
    
    if m1_decriptat == m1 and m_adunat_decriptat == (m1 + m2):
        print("\n[Succes] Criptosistemul Paillier si proprietatea omomorfica functioneaza corect!")
    else:
        print("\n[Eroare] Datele decriptate nu corespund.")