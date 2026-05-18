import random
import hashlib

def euclid_extins(a, b):
    """
    Algoritmul lui Euclid Extins pentru calculul inversului modular.
    Returneaza (cmmdc, x, y) astfel incat a*x + b*y = cmmdc
    """
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
        raise ValueError(f"Inversul modular nu exista deoarece cmmdc({a}, {m}) != 1")
    return x % m

def functie_hash(u1, u2, e, p):
    """
    Functie hash bazata pe SHA-256.
    Concateneaza reprezentarile in octeti ale componentelor si returneaza un intreg modulo p.
    """
    date_de_intrare = f"{u1}:{u2}:{e}".encode('utf-8')
    h = hashlib.sha256(date_de_intrare).hexdigest()
    return int(h, 16) % p

class CramerShoup:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se foloseste un grup ciclic de ordin prim. Pentru demonstratie alegem 
        un prim p sigur, astfel incat p = 2q + 1 (unde q este tot prim).
        """
        p = 92879
        q = 46439
        
        while True:
            base1 = random.randint(2, p - 1)
            base2 = random.randint(2, p - 1)
            g1 = pow(base1, 2, p)
            g2 = pow(base2, 2, p)
            if g1 != 1 and g2 != 1 and g1 != g2:
                break
                
        x1 = random.randint(1, q - 1)
        x2 = random.randint(1, q - 1)
        y1 = random.randint(1, q - 1)
        y2 = random.randint(1, q - 1)
        z  = random.randint(1, q - 1)
        
        # Se calculeaza valorile publice c, d, h
        c = (pow(g1, x1, p) * pow(g2, x2, p)) % p
        d = (pow(g1, y1, p) * pow(g2, y2, p)) % p
        h = pow(g1, z, p)
        
        cheie_publica = (p, q, g1, g2, c, d, h)
        cheie_privata = (x1, x2, y1, y2, z)
        
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(m, cheie_publica):
        """
        Pasul 2: Criptarea mesajului
        Mesajul m trebuie sa fie un element din subgrup (deci un patrat perfect modulo p).
        """
        p, q, g1, g2, c, d, h = cheie_publica
        
        if not (0 < m < p):
            raise ValueError(f"Mesajul trebuie sa fie in intervalul (0, {p})")
            
        k = random.randint(1, q - 1)
        
        u1 = pow(g1, k, p)
        u2 = pow(g2, k, p)
        e  = (pow(h, k, p) * m) % p
        
        alfa = functie_hash(u1, u2, e, p)
        
        v = (pow(c, k, p) * pow(d, k * alfa, p)) % p
        
        return (u1, u2, e, v)

    @staticmethod
    def decriptare(criptotext, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptarea mesajului si verificarea validitatii
        """
        p, q, g1, g2, c, d, h = cheie_publica
        x1, x2, y1, y2, z = cheie_privata
        u1, u2, e, v = criptotext
        
        alfa = functie_hash(u1, u2, e, p)
        
        termen1 = pow(u1, x1 + y1 * alfa, p)
        termen2 = pow(u2, x2 + y2 * alfa, p)
        v_verif = (termen1 * termen2) % p
        
        if v != v_verif:
            raise ValueError("Atac detectat sau eroare de transmisie! Criptotextul este invalid.")
            
        # Daca testul a trecut, decriptam: m = e / (u1^z) mod p
        impartitor = pow(u1, z, p)
        impartitor_inv = invers_modular(impartitor, p)
        m = (e * impartitor_inv) % p
        
        return m


if __name__ == "__main__":
    print("--- Criptosistemul Cramer-Shoup (SHA-256) ---\n")
    
    # 1. Generarea cheilor
    pub_key, priv_key = CramerShoup.genereaza_chei()
    p_comun, q_comun, g1_pub, g2_pub, c_pub, d_pub, h_pub = pub_key
    
    print(f"[Cheie Publica] Modulul p = {p_comun} (Ordinul subgrupului q = {q_comun})")
    print(f"[Cheie Publica] Generator g1 = {g1_pub}, Generator g2 = {g2_pub}")
    print(f"[Cheie Publica] Componente de validare: c = {c_pub}, d = {d_pub}, h = {h_pub}\n")
    
    baza_mesaj = 12345
    mesaj_original = pow(baza_mesaj, 2, p_comun)
    print(f"-> Mesajul original in clar (m) = {mesaj_original}")
    
    criptotext = CramerShoup.criptare(mesaj_original, pub_key)
    print(f"-> Criptotextul generat (u1, u2, e, v) =\n   {criptotext}\n")
    
    try:
        mesaj_decriptat = CramerShoup.decriptare(criptotext, pub_key, priv_key)
        print(f"-> Mesajul decriptat de receptor = {mesaj_decriptat}")
        
        if mesaj_original == mesaj_decriptat:
            print("\n[Succes] Decriptarea a fost realizata cu succes! Mesajele coincid.")
    except ValueError as err:
        print(f"\n[Eroare]: {err}")
        
    print("\n--- Simulare Atac: Modificam o componenta a criptotextului ---")
    u1_atac, u2_atac, e_atac, v_atac = criptotext
    e_atac = (e_atac + 1) % p_comun
    criptotext_alterat = (u1_atac, u2_atac, e_atac, v_atac)
    
    try:
        CramerShoup.decriptare(criptotext_alterat, pub_key, priv_key)
    except ValueError as err:
        print(f"[Succes Atac Respins] Decriptarea a esuat conform asteptarilor.")
        print(f"Mesaj eroare primit de la sistem: {err}")