import random

def cmmdc(a, b):
    """Calculeaza cel mai mare divizor comun."""
    while b:
        a, b = b, a % b
    return a

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
        raise ValueError(f"Inversul modular nu exista pentru cmmdc({a}, {m}) != 1")
    return x % m

class OkamotoUchiyama:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se aleg doua numere prime mari p si q (aici mici pentru demonstratie).
        """
        p = 233
        q = 241
        
        n = (p ** 2) * q
        
        while True:
            g = random.randint(2, n - 1)
            g_p = pow(g, p - 1, p ** 2)
            if g_p != 1:
                break
        h = pow(g, n, n)
        
        cheie_publica = (n, g, h)
        cheie_privata = (p, q)
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(m, cheie_publica):
        """
        Pasul 2: Criptarea mesajului
        C = (g^m * h^r) mod n
        """
        n, g, h = cheie_publica
        
        r = random.randint(2, n - 1)
        
        c = (pow(g, m, n) * pow(h, r, n)) % n
        return c

    @staticmethod
    def decriptare(c, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptarea mesajului
        m = ( L(c^(p-1) mod p^2) / L(g^(p-1) mod p^2) ) mod p
        unde L(x) = (x - 1) / p
        """
        n, g, h = cheie_publica
        p, q = cheie_privata
        
        def L(x):
            return (x - 1) // p
        c_p = pow(c, p - 1, p ** 2)
        numarator = L(c_p)
        g_p = pow(g, p - 1, p ** 2)
        numitor = L(g_p)
        
        numitor_inv = invers_modular(numitor, p)
        m = (numarator * numitor_inv) % p
        return m

if __name__ == "__main__":
    print("--- Criptosistemul Okamoto-Uchiyama ---\n")
    
    pub_key, priv_key = OkamotoUchiyama.genereaza_chei()
    n_pub, g_pub, h_pub = pub_key
    p_priv, q_priv = priv_key
    
    print(f"[Cheie Publica]  n = {n_pub}")
    print(f"[Cheie Publica]  g = {g_pub}")
    print(f"[Cheie Publica]  h = {h_pub}\n")
    print(f"[Cheie Privata]  p = {p_priv}")
    print(f"[Cheie Privata]  q = {q_priv}\n")
    
    mesaj_original = 145
    print(f"-> Mesajul original in clar (m) = {mesaj_original}")
    
    criptotext = OkamotoUchiyama.criptare(mesaj_original, pub_key)
    print(f"-> Mesajul criptat rezultat (C) = {criptotext}\n")
    
    mesaj_decriptat = OkamotoUchiyama.decriptare(criptotext, pub_key, priv_key)
    print(f"-> Mesajul decriptat de receptor = {mesaj_decriptat}")
    
    if mesaj_original == mesaj_decriptat:
        print("\n[Succes] Decriptarea a fost realizata cu succes!")
    else:
        print("\n[Eroare] Mesajul decriptat nu coincide cu cel original.")