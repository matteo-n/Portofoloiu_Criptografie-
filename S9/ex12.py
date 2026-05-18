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
    """Algoritmul lui Euclid Extins. Returneaza (cmmdc, x, y)."""
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

def teorema_chineza_a_resturilor(resturi, moduli):
    """
    Implementarea Lemei Chineze a Resturilor (TCR).
    Rezolva sistemul de congruente liniare: 
      m == m_p (mod p)
      m == m_q (mod q)
    """
    N = math.prod(moduli)
    rezultat = 0
    for r, m in zip(resturi, moduli):
        N_i = N // m
        inv = invers_modular(N_i, m)
        rezultat = (rezultat + r * N_i * inv) % N
    return rezultat

class SchmidtSamoa:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se aleg doua numere prime mari distincte p si q.
        Se calculeaza N = (p^2) * q.
        """
        p = 127
        q = 131
       
        N = (p ** 2) * q
        
        cheie_publica = N
        cheie_privata = (p, q)
        
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(m, cheie_publica):
        """
        Pasul 2: Criptare
        C = m^N mod N
        Mesajul m trebuie sa fie strict mai mic decat p * q.
        """
        N = cheie_publica
        
        # C = m^N mod N
        c = pow(m, N, N)
        return c

    @staticmethod
    def decriptare(c, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptare folosind Teorema Chineza a Resturilor
        m_p = c^d mod p  si  m_q = c^d mod q
        unde d = N^(-1) mod cmmmc(p-1, q-1)
        """
        N = cheie_publica
        p, q = cheie_privata
        
        lambda_pq = cmmmc(p - 1, q - 1)
        
        d = invers_modular(N, lambda_pq)
        
        m_p = pow(c, d, p)
        m_q = pow(c, d, q)
        
        resturi = [m_p, m_q]
        moduli = [p, q]
        
        m = teorema_chineza_a_resturilor(resturi, moduli)
        return m

if __name__ == "__main__":
    print("--- Criptosistemul Schmidt-Samoa ---\n")
    
    N_pub, priv_key = SchmidtSamoa.genereaza_chei()
    p_priv, q_priv = priv_key
    limita_mesaj = p_priv * q_priv
    
    print(f"[Cheie Publica] Modulul N = p^2 * q = {N_pub}")
    print(f"[Cheie Privata] Componenta p = {p_priv}")
    print(f"[Cheie Privata] Componenta q = {q_priv}")
    print(f"[Setari] Spatiul maxim al mesajului (p * q) = {limita_mesaj}\n")
    
    mesaj_original = 9876
    print(f"-> Mesajul original in clar (m) = {mesaj_original}")
    
    criptotext = SchmidtSamoa.criptare(mesaj_original, N_pub)
    print(f"-> Criptotextul rezultat (C) = {criptotext}\n")
    
    mesaj_decriptat = SchmidtSamoa.decriptare(criptotext, N_pub, priv_key)
    print(f"-> Mesajul decriptat prin Lema Chineza = {mesaj_decriptat}")
    
    if mesaj_original == mesaj_decriptat:
        print("\n[Succes] Criptosistemul Schmidt-Samoa a decriptat corect textul!")
    else:
        print("\n[Eroare] Mesajul decriptat difera de cel original.")