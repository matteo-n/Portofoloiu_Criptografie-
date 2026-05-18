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

def teorema_chinezeasca_a_resturilor(resturi, moduli):
    """Rezolva sistemul de congruente liniare: x == r_i (mod m_i)."""
    N = math.prod(moduli)
    x_final = 0
    for r, m in zip(resturi, moduli):
        N_i = N // m
        inv = invers_modular(N_i, m)
        x_final = (x_final + r * N_i * inv) % N
    return x_final, N

class NaccacheStern:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se alege o multime de k numere prime mici si distincte p_1, p_2, ..., p_k.
        Se impart in doua multimi pentru a construi u si v.
        """
       
        prime_mici = [3, 5, 7, 11, 13, 17, 19, 23]
        k = len(prime_mici)
        
       
        u_list = prime_mici[:k//2]      
        v_list = prime_mici[k//2:]      
        
        u = math.prod(u_list)
        v = math.prod(v_list)
        sigma = u * v  
        
        a = 10
        while True:
            p = 2 * a * u + 1
            if NaccacheStern.este_prim(p):
                break
            a += 1
            
        b = 12
        while True:
            q = 2 * b * v + 1
            if NaccacheStern.este_prim(q) and q != p:
                break
            b += 1
            
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        while True:
            g = random.randint(2, n - 1)
            conditie_valida = True
            for p_i in prime_mici:
                test_exp = phi_n // p_i
                if pow(g, test_exp, n) == 1:
                    conditie_valida = False
                    break
            if conditie_valida:
                break
                
        cheie_publica = (n, g, prime_mici)
        cheie_privata = (p, q)
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(m, cheie_publica):
        """
        Pasul 2: Criptarea mesajului
        Mesajul m trebuie sa fie mai mic decat sigma (produsul primelor mici).
        C = (g^m * x^sigma) mod n, unde x este ales aleatoriu.
        """
        n, g, prime_mici = cheie_publica
        sigma = math.prod(prime_mici)
        
        if not (0 <= m < sigma):
            raise ValueError(f"Mesajul trebuie sa fie mai mic decat sigma = {sigma}")
            
        while True:
            x = random.randint(2, n - 1)
            if math.gcd(x, n) == 1:
                break
                
        termen1 = pow(g, m, n)
        termen2 = pow(x, sigma, n)
        c = (termen1 * termen2) % n
        return c

    @staticmethod
    def decriptare(c, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptarea mesajului
        Pentru fiecare p_i, se izoleaza componenta m_i = m mod p_i prin ridicarea la puterea phi_n / p_i.
        Se aplica TCR pentru a reconstitui m modulo sigma.
        """
        n, g, prime_mici = cheie_publica
        p, q = cheie_privata
        phi_n = (p - 1) * (q - 1)
        
        resturi_m = []
        
        for p_i in prime_mici:
            exp = phi_n // p_i
            c_prim = pow(c, exp, n)
            
            m_i = -1
            for candidi_m in range(p_i):
                if pow(g, exp * candidi_m, n) == c_prim:
                    m_i = candidi_m
                    break
                    
            if m_i == -1:
                raise ValueError("Eroare la decriptarea unei componente paratiale.")
            resturi_m.append(m_i)
            
        m_final, _ = teorema_chinezeasca_a_resturilor(resturi_m, prime_mici)
        return m_final

    @staticmethod
    def este_prim(numar):
        """Functie simpla de verificare daca un numar este prim."""
        if numar < 2:
            return False
        for i in range(2, int(math.isqrt(numar)) + 1):
            if numar % i == 0:
                return False
        return True

if __name__ == "__main__":
    print("--- Criptosistemul Naccache-Stern ---\n")
    
    pub_key, priv_key = NaccacheStern.genereaza_chei()
    n_pub, g_pub, prime_list = pub_key
    sigma_limita = math.prod(prime_list)
    
    print(f"[Cheie Publica] Modulul n = {n_pub}")
    print(f"[Cheie Publica] Generatorul g = {g_pub}")
    print(f"[Cheie Publica] Multimea de prime mici = {prime_list}")
    print(f"[Setari] Spatiul maxim al mesajului (sigma) = {sigma_limita}\n")
    
    mesaj_original = 123456
    print(f"-> Mesajul original in clar (m) = {mesaj_original}")
    
    criptotext = NaccacheStern.criptare(mesaj_original, pub_key)
    print(f"-> Criptotextul rezultat (C) = {criptotext}\n")
    
    try:
        mesaj_decriptat = NaccacheStern.decriptare(criptotext, pub_key, priv_key)
        print(f"-> Mesajul decriptat de receptor = {mesaj_decriptat}")
        
        if mesaj_original == mesaj_decriptat:
            print("\n[Succes] Decriptarea a fost realizata cu succes! Mesajele coincid.")
        else:
            print("\n[Eroare] Mesajul decriptat este gresit.")
    except ValueError as e:
        print(f"\n[Eroare]: {e}")