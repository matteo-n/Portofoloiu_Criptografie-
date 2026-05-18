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
    """
    Implementează Algoritmul lui Euclid Extins.
    Returnează (cmmdc, x, y) astfel încât a*x + b*y = cmmdc
    """
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
        raise ValueError(f"Inversul modular nu există deoarece cmmdc({a}, {m}) != 1")
    return x % m

class MasseyOmura:
    def __init__(self, p):
        """
        Inițializează criptosistemul cu un parametru global comun: numărul prim p.
        Ordinul grupului multiplicativ este p - 1.
        """
        self.p = p
        self.ordin = p - 1

    def genereaza_chei_utilizator(self):
        """
        Generează o pereche de chei (e, d) pentru un utilizator.
        e = exponentul de criptare (trebuie să fie prim cu p-1)
        d = exponentul de decriptare (inversul lui e modulo p-1)
        """
        while True:
            e = random.randint(2, self.ordin - 1)
            if cmmdc(e, self.ordin) == 1:
                d = invers_modular(e, self.ordin)
                return e, d

    def pas1_alice_cripteaza(self, m, e_A):
        """Alice aplică primul lacăt: c1 = m^e_A mod p"""
        if not (0 < m < self.p):
            raise ValueError(f"Mesajul trebuie să fie un număr în intervalul (0, {self.p})")
        return pow(m, e_A, self.p)

    def pas2_bob_cripteaza(self, c1, e_B):
        """Bob aplică al doilea lacăt: c2 = c1^e_B mod p"""
        return pow(c1, e_B, self.p)

    def pas3_alice_decipreaza(self, c2, d_A):
        """Alice își scoate lacătul: c3 = c2^d_A mod p"""
        return pow(c2, d_A, self.p)

    def pas4_bob_decipreaza(self, c3, d_B):
        """Bob își scoate lacătul și obține mesajul: m_final = c3^d_B mod p"""
        return pow(c3, d_B, self.p)


if __name__ == "__main__":
    print("--- Simulare Criptosistem Massey-Omura ---\n")
    
    p_comun = 4771487638337373
    
    mo = MasseyOmura(p_comun)
    print(f"[Setări] Parametrul public (Modulul prim p) = {p_comun}")
    
    e_Alice, d_Alice = mo.genereaza_chei_utilizator()
    e_Bob, d_Bob     = mo.genereaza_chei_utilizator()
    
    print(f"[Chei Alice] Secret Criptare (e_A) = {e_Alice} | Secret Decriptare (d_A) = {d_Alice}")
    print(f"[Chei Bob]   Secret Criptare (e_B) = {e_Bob} | Secret Decriptare (d_B) = {d_Bob}\n")
    
    mesaj_original = 20260518
    print(f"-> Mesajul în clar trimis de Alice (m) = {mesaj_original}\n")
    
    c1 = mo.pas1_alice_cripteaza(mesaj_original, e_Alice)
    print(f"[Pasul 1] Alice trimite lui Bob (c1 = m^e_A mod p):")
    print(f"          c1 = {c1}")
    
    c2 = mo.pas2_bob_cripteaza(c1, e_Bob)
    print(f"[Pasul 2] Bob retrimite lui Alice (c2 = c1^e_B mod p):")
    print(f"          c2 = {c2}")
    
    c3 = mo.pas3_alice_decipreaza(c2, d_Alice)
    print(f"[Pasul 3] Alice trimite din nou lui Bob (c3 = c2^d_A mod p):")
    print(f"          c3 = {c3}")
    
    mesaj_decriptat = mo.pas4_bob_decipreaza(c3, d_Bob)
    print(f"[Pasul 4] Bob decriptează textul final (m_final = c3^d_B mod p):")
    print(f"          m_final = {mesaj_decriptat}\n")
    
    if mesaj_original == mesaj_decriptat:
        print("Succes: Decriptarea a fost realizată cu succes! Mesajele coincid.")
    else:
        print("Eroare: Mesajul decriptat nu coincide cu cel original.")