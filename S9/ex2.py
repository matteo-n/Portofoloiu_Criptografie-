import random
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
def cmmdc(a, b):
    """Calculează cel mai mare divizor comun."""
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
    """Calculează inversul modular al lui a modulo m."""
    g, x, y = euclid_extins(a, m)
    if g != 1:
        raise ValueError(f"Inversul modular nu există pentru cmmdc({a}, {m}) != 1")
    return x % m
class MerkleHellman:
    @staticmethod
    def genereaza_chei(dimensiune_bloc=8):
        """
        Generează perechea de chei publică/privată.
        dimensiune_bloc reprezintă numărul de biți procesați per bloc.
        """
        w = []
        suma_curenta = 0
        for _ in range(dimensiune_bloc):
            # Fiecare element trebuie să fie strict mai mare decât suma precedentă
            termen = suma_curenta + random.randint(2, 10)
            w.append(termen)
            suma_curenta += termen
        q = suma_curenta + random.randint(11, 100)
        while True:
            r = random.randint(2, q - 1)
            if cmmdc(r, q) == 1:
                break
        b = [(x * r) % q for x in w]
        cheie_publica = b
        cheie_privata = (w, q, r)
        return cheie_publica, cheie_privata
    @staticmethod
    def criptare(mesaj_biti, cheie_publica):
        """
        Criptează un vector de biți utilizând cheia publică.
        Suma elementelor din cheia publică corespunzătoare biților de 1.
        """
        if len(mesaj_biti) != len(cheie_publica):
            raise ValueError("Dimensiunea blocului de biți nu corespunde cu dimensiunea cheii publice.")
        # C = suma(b_i * m_i)
        criptotext = sum(b_i * m_i for b_i, m_i in zip(cheie_publica, mesaj_biti))
        return criptotext
    @staticmethod
    def decriptare(criptotext, cheie_privata):
        """
        Decriptează un număr (criptotext) înapoi într-un vector de biți.
        """
        w, q, r = cheie_privata
        r_inv = invers_modular(r, q)
        c_prim = (criptotext * r_inv) % q
        mesaj_biti = [0] * len(w)
        for i in range(len(w) - 1, -1, -1):
            if c_prim >= w[i]:
                mesaj_biti[i] = 1
                c_prim -= w[i]
        return mesaj_biti
if __name__ == "__main__":
    print("--- Simulare Criptosistem Rucsac (Merkle-Hellman) ---\n")
    N_BITI = 8
    public_key, private_key = MerkleHellman.genereaza_chei(dimensiune_bloc=N_BITI)
    w_privat, q_privat, r_privat = private_key
    
    print(f"[Cheia Privată - Rucsacul Ușor W]:  {w_privat}")
    print(f"[Cheia Privată - Modulul q]:        {q_privat}")
    print(f"[Cheia Privată - Multiplicatorul r]: {r_privat}\n")
    print(f"[Cheia Publică - Rucsacul Greu B]:   {public_key}\n")
    
    mesaj_clar = [0, 1, 0, 0, 1, 0, 1, 1]
    print(f"-> Blocul în clar trimis (m) = {mesaj_clar}")
    
    c = MerkleHellman.criptare(mesaj_clar, public_key)
    print(f"-> Mesajul criptat rezultat (C) = {c}\n")
    
    mesaj_decriptat = MerkleHellman.decriptare(c, private_key)
    print(f"-> Blocul decriptat de receptor = {mesaj_decriptat}\n")
    
    if mesaj_clar == mesaj_decriptat:
        print("Succes: Decriptarea rucsacului a fost realizată cu succes!")
    else:
        print("Eroare: Datele decriptate sunt eronate.")