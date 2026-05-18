import random
import math

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
        raise ValueError("Inversul modular nu exista.")
    return x % m

class Benaloh:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se alege dimensiunea blocului r (un numar prim mic, de exemplu r = 17).
        Se aleg doua numere prime mari p si q astfel incat:
          - r divide (p - 1)
          - cmmdc(r, (p - 1) / r) == 1
          - cmmdc(r, q - 1) == 1
        """
        r = 17  
        
        p = 239  
                 
        q = 251 
        
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        while True:
            g = random.randint(2, n - 1)
            if math.gcd(g, n) == 1:
                test_val = pow(g, phi_n // r, n)
                if test_val != 1:
                    break
                    
        cheie_publica = (n, r, g)
        cheie_privata = phi_n
        
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(m, cheie_publica):
        """
        Pasul 2: Criptare
        Mesajul m trebuie sa fie in Z_r (0 <= m < r).
        Se alege un u aleatoriu prim cu n.
        C = (g^m * u^r) mod n
        """
        n, r, g = cheie_publica
        
        if not (0 <= m < r):
            raise ValueError(f"Mesajul trebuie sa fie in intervalul [0, {r-1}]")
            
        while True:
            u = random.randint(2, n - 1)
            if math.gcd(u, n) == 1:
                break
                
        termen1 = pow(g, m, n)
        termen2 = pow(u, r, n)
        c = (termen1 * termen2) % n
        return c

    @staticmethod
    def decriptare(c, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptare
        Calculam c^(phi_n / r) mod n.
        Cautam m prin verificare exhaustiva in intervalul [0, r - 1].
        """
        n, r, g = cheie_publica
        phi_n = cheie_privata
        martor_c = pow(c, phi_n // r, n)
        baza_g = pow(g, phi_n // r, n)
        for candidat_m in range(r):
            if pow(baza_g, candidat_m, n) == martor_c:
                return candidat_m
                
        raise ValueError("Eroare la decriptare: Solutia nu a putut fi identificata.")

if __name__ == "__main__":
    print("--- Criptosistemul Benaloh ---\n")
    
    # 1. Generarea cheilor
    pub_key, priv_key = Benaloh.genereaza_chei()
    n_pub, r_pub, g_pub = pub_key
    
    print(f"[Cheie Publica] Modulul n = {n_pub}")
    print(f"[Cheie Publica] Dimensiunea blocului r = {r_pub} (Spatiul mesajelor: Z_17)")
    print(f"[Cheie Publica] Generatorul g = {g_pub}\n")
    print(f"[Cheie Privata] Phi(n) = {priv_key}\n")
    
    m1 = 5
    m2 = 7
    print(f"-> Mesajul 1 in clar (m1) = {m1}")
    print(f"-> Mesajul 2 in clar (m2) = {m2}\n")
    
    c1 = Benaloh.criptare(m1, pub_key)
    c2 = Benaloh.criptare(m2, pub_key)
    print(f"-> Criptotext 1 (c1) = {c1}")
    print(f"-> Criptotext 2 (c2) = {c2}\n")
    
    m1_dec = Benaloh.decriptare(c1, pub_key, priv_key)
    print(f"-> Decriptare clasica c1 = {m1_dec}")
    
    c_adunat = (c1 * c2) % n_pub
    
    m_adunat_dec = Benaloh.decriptare(c_adunat, pub_key, priv_key)
    print(f"\n--- Demonstratie Proprietate Omomorfica ---")
    print(f"-> Inmultim criptotextul c1 cu c2 (c_adunat) = {c_adunat}")
    print(f"-> Rezultatul decriptarii lui c_adunat       = {m_adunat_dec}")
    print(f"-> Verificare matematica: ({m1} + {m2}) mod {r_pub}   = {(m1 + m2) % r_pub}")
    
    if m1_dec == m1 and m_adunat_dec == ((m1 + m2) % r_pub):
        print("\n[Succes] Criptosistemul Benaloh si proprietatea sa omomorfica functioneaza corect!")
    else:
        print("\n[Eroare] Datele decriptate nu corespund.")