import random

def cmmdc(a, b):
    """Calculeaza cel mai mare divizor comun."""
    while b:
        a, b = b, a % b
    return a

def simbol_jacobi(a, n):
    """
    Calculeaza Simbolul Jacobi (a / n).
    Folosit pentru a verifica proprietatile de reziduu patratic.
    """
    if n <= 0 or n % 2 == 0:
        return 0
    ans = 1
    a = a % n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                ans = -ans
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            ans = -ans
        a = a % n
    if n == 1:
        return ans
    return 0

class GoldwasserMicali:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se aleg doua numere prime mari p si q.
        Se calculeaza n = p * q.
        Se cauta un pseudosfere (non-reziduu patratic x cu simbolul Jacobi +1).
        """
        p = 137
        q = 139
        n = p * q
        
        while True:
            x = random.randint(2, n - 1)
            if simbol_jacobi(x, p) == -1 and simbol_jacobi(x, q) == -1:
                if simbol_jacobi(x, n) == 1:
                    break
                    
        cheie_publica = (n, x)
        cheie_privata = (p, q)
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare_bit(bit, cheie_publica):
        """
        Pasul 2: Criptarea unui singur bit
        Daca bit = 0: C = y^2 mod n
        Daca bit = 1: C = (x * y^2) mod n
        Unde y este un numar aleator prim cu n.
        """
        n, x = cheie_publica
        
        while True:
            y = random.randint(2, n - 1)
            if cmmdc(y, n) == 1:
                break
                
        y_patrat = pow(y, 2, n)
        
        if bit == 0:
            c = y_patrat
        else:
            c = (x * y_patrat) % n
        return c

    @staticmethod
    def decriptare_bit(c, cheie_privata):
        """
        Pasul 3: Decriptarea unui singur bit
        Se verifica daca c este reziduu patratic modulo p.
        Daca (c/p) == 1, atunci bitul este 0.
        Daca (c/p) == -1, atunci bitul este 1.
        """
        p, q = cheie_privata
        
        simbol = simbol_jacobi(c, p)
        
        if simbol == 1:
            return 0
        else:
            return 1

if __name__ == "__main__":
    print("--- Criptosistemul Goldwasser-Micali ---\n")
    
    # 1. Generarea cheilor
    pub_key, priv_key = GoldwasserMicali.genereaza_chei()
    n_pub, x_pub = pub_key
    p_priv, q_priv = priv_key
    
    print(f"[Cheie Publica]  n = {n_pub}")
    print(f"[Cheie Publica]  x = {x_pub} (Pseudosfere)\n")
    print(f"[Cheie Privata]  p = {p_priv}")
    print(f"[Cheie Privata]  q = {q_priv}\n")
    
    mesaj_original = [1, 0, 1]
    print(f"-> Sirul de biti original (m) = {mesaj_original}")
    
    criptotext_lista = []
    for bit in mesaj_original:
        c_bit = GoldwasserMicali.criptare_bit(bit, pub_key)
        criptotext_lista.append(c_bit)
        
    print(f"-> Criptotextul rezultat (C)  = {criptotext_lista}")
    print("   (Observati cum cei doi biti de 1 au produs valori criptate diferite!)")
    
    mesaj_decriptat = []
    for c_bit in criptotext_lista:
        bit_dec = GoldwasserMicali.decriptare_bit(c_bit, priv_key)
        mesaj_decriptat.append(bit_dec)
        
    print(f"\n-> Sirul de biti decriptat     = {mesaj_decriptat}")
    
    if mesaj_original == mesaj_decriptat:
        print("\n[Succes] Decriptarea a fost realizata cu succes!")
    else:
        print("\n[Eroare] Mesajul decriptat nu coincide cu cel original.")