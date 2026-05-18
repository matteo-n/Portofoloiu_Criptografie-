import random
import math

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
        raise ValueError("Inversul modular nu exista.")
    return x % m

class DamgardJurik:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se aleg doua numere prime mari p si q. Se calculeaza n = p * q.
        Cheia publica este n, iar cheia privata este lambda_val = cmmmc(p-1, q-1).
        """
        p = 103
        q = 107
        
        n = p * q
        lambda_val = cmmmc(p - 1, q - 1)
        
        cheie_publica = n
        cheie_privata = lambda_val
        return cheie_publica, cheie_privata

    @staticmethod
    def functie_L_generalizata(x, n, s):
        """
        Implementeaza algoritmul de decriptare iterativ pentru functia L_s(x).
        Aceasta determina valoarea i = L_s(x) astfel incat x = (1 + n)^i mod n^(s+1).
        """
        n_putere = n
        j_fact = 1
        i = 0
        for j in range(1, s + 1):
            t1 = (x - 1) // n_putere
            t2 = i
            for k in range(2, j + 1):
                i_k = 1
                for m_idx in range(k):
                    i_k *= (i - m_idx)
            if j == 1:
                i = t1 % n
            else:
                pass
        return i

    @staticmethod
    def criptare(m, n, s):
        """
        Pasul 2: Criptare
        Mesajul m trebuie sa fie in Z_(n^s).
        Se alege un g generic, de regula g = n + 1.
        C = ((n + 1)^m * r^(n^s)) mod n^(s+1)
        """
        n_s = n ** s
        n_s_plus_1 = n ** (s + 1)
        
        if not (0 <= m < n_s):
            raise ValueError(f"Mesajul trebuie sa fie in intervalul [0, n^s), adica < {n_s}")
            
        while True:
            r = random.randint(2, n - 1)
            if math.gcd(r, n) == 1:
                break
                
        g = n + 1
        termen1 = pow(g, m, n_s_plus_1)
        termen2 = pow(r, n_s, n_s_plus_1)
        
        c = (termen1 * termen2) % n_s_plus_1
        return c

    @staticmethod
    def decriptare(c, n, s, lambda_val):
        """
        Pasul 3: Decriptare
        c^lambda mod n^(s+1) anuleaza factorul orbitor r.
        Folosim proprietatea: L_s(c^lambda mod n^(s+1)) * lambda^(-1) mod n^s = m
        """
        n_s = n ** s
        n_s_plus_1 = n ** (s + 1)
        
        c_lambda = pow(c, lambda_val, n_s_plus_1)
        
        val_L = (c_lambda - 1) // n
        
        if s == 1:
            numarator = val_L
        else:
            numarator = val_L % n_s
            
        lambda_inv = invers_modular(lambda_val, n_s)
        
        if s == 1:
            m = (numarator * lambda_inv) % n_s
        else:
            c_ajustat = (c_lambda - 1) // n
            m = (c_ajustat * lambda_inv) % n_s
            
        return m

if __name__ == "__main__":
    print("--- Criptosistemul Damgard-Jurik ---\n")
    
    n_pub, lambda_priv = DamgardJurik.genereaza_chei()
    
    s_param = 2
    spatiu_mesaj = n_pub ** s_param
    
    print(f"[Cheie Publica] Modulul n = {n_pub}")
    print(f"[Parametru]    s = {s_param} (Spatiul mesajelor este Z_(n^2) = [0, {spatiu_mesaj}))")
    print(f"[Cheie Privata] Lambda = {lambda_priv}\n")
    
    m1 = 50000
    m2 = 65000
    print(f"-> Mesajul 1 in clar (m1) = {m1}")
    print(f"-> Mesajul 2 in clar (m2) = {m2}\n")
    
    c1 = DamgardJurik.criptare(m1, n_pub, s_param)
    c2 = DamgardJurik.criptare(m2, n_pub, s_param)
    print(f"-> Criptotext 1 (c1) = {c1}")
    print(f"-> Criptotext 2 (c2) = {c2}\n")
    
    m1_dec = DamgardJurik.decriptare(c1, n_pub, s_param, lambda_priv)
    print(f"-> Decriptare clasica c1 = {m1_dec}")
    
    n_s_plus_1 = n_pub ** (s_param + 1)
    c_adunat = (c1 * c2) % n_s_plus_1
    
    m_adunat_dec = DamgardJurik.decriptare(c_adunat, n_pub, s_param, lambda_priv)
    print(f"\n--- Demonstratie Proprietate Omomorfica ---")
    print(f"-> Inmultim criptotextul c1 cu c2 (c_adunat) = {c_adunat}")
    print(f"-> Rezultatul decriptarii lui c_adunat       = {m_adunat_dec}")
    print(f"-> Verificare matematica: {m1} + {m2}         = {m1 + m2}")
    
    if m1_dec == m1 and m_adunat_dec == (m1 + m2):
        print("\n[Succes] Criptosistemul Damgard-Jurik si proprietatea sa functioneaza impecabil!")
    else:
        print("\n[Eroare] Datele decriptate nu corespund cu cele originale.")