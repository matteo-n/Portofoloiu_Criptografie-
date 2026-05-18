import random

def euclid_extins(a, b):
    """Algoritmul lui Euclid Extins pentru determinarea coeficientilor Bezout."""
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

def text_in_biti(text):
    """Converteste un string in blocuri de biti (lista de 0 si 1)."""
    biti = []
    for caractere in text:
        b = bin(ord(caractere))[2:].zfill(8)
        biti.extend([int(x) for x in b])
    return biti

def biti_in_text(biti):
    """Converteste o lista de biti inapoi intr-un string text."""
    caractere = []
    for i in range(0, len(biti), 8):
        bloc = biti[i:i+8]
        if len(bloc) < 8:
            break
        str_bit = "".join(str(x) for x in bloc)
        caractere.append(chr(int(str_bit, 2)))
    return "".join(caractere)

class BlumGoldwasser:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se aleg doua numere prime mari p si q asfel incat p == 3 (mod 4) si q == 3 (mod 4).
        """
        p = 499  # 499 % 4 == 3
        q = 503  # 503 % 4 == 3
        n = p * q
        
        cheie_publica = n
        cheie_privata = (p, q)
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(mesaj_biti, cheie_publica):
        """
        Pasul 2: Criptarea fluxului de biti
        Foloseste generatorul Blum Blum Shub pentru a face XOR cu mesajul.
        """
        n = cheie_publica
        L = len(mesaj_biti)
        
        while True:
            x = random.randint(2, n - 1)
            if math_cmmdc(x, n) == 1:
                break
                
        x_curent = pow(x, 2, n)
        
        criptotext_biti = []
        for i in range(L):
            x_curent = pow(x_curent, 2, n)
            bit_cheie = x_curent % 2  
            criptotext_biti.append(mesaj_biti[i] ^ bit_cheie)
            
        x_final = pow(x_curent, 2, n)
        
        return criptotext_biti, x_final

    @staticmethod
    def decriptare(criptotext_pachet, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptarea fluxului de biti
        Inversul generatorului BBS folosind proprietatile numerelor Blum si Teorema Chinezeasca.
        """
        n = cheie_publica
        p, q = cheie_privata
        criptotext_biti, x_final = criptotext_pachet
        L = len(criptotext_biti)
        
        exp_p = pow((p + 1) // 4, L + 1, p - 1)
        exp_q = pow((q + 1) // 4, L + 1, q - 1)
        
        x0_p = pow(x_final, exp_p, p)
        x0_q = pow(x_final, exp_q, q)
        
        _, r, s = euclid_extins(p, q)
        
        x_0 = (x0_q * r * p + x0_p * s * q) % n
        
        x_curent = x_0
        mesaj_decriptat_biti = []
        
        for i in range(L):
            x_curent = pow(x_curent, 2, n)
            bit_cheie = x_curent % 2
            mesaj_decriptat_biti.append(criptotext_biti[i] ^ bit_cheie)
            
        return mesaj_decriptat_biti

def math_cmmdc(a, b):
    while b:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    print("--- Criptosistemul Blum-Goldwasser ---\n")
    
    pub_key, priv_key = BlumGoldwasser.genereaza_chei()
    print(f"[Cheie Publica] Modulul public n = {pub_key}")
    print(f"[Cheie Privata] Factorii prime Blum: p = {priv_key[0]}, q = {priv_key[1]}\n")
    
    text_original = "UAIC"
    print(f"-> Textul original de trimis = '{text_original}'")
    
    biti_clari = text_in_biti(text_original)
    print(f"-> Reprezentarea in biti ({len(biti_clari)} biti) = {biti_clari}\n")
    
    criptotext_pachet = BlumGoldwasser.criptare(biti_clari, pub_key)
    cripto_biti, x_final_stare = criptotext_pachet
    print(f"-> Criptotextul rezultat (biti) = {cripto_biti}")
    print(f"-> Starea finala atasata x_final = {x_final_stare}\n")
    
    biti_decriptati = BlumGoldwasser.decriptare(criptotext_pachet, pub_key, priv_key)
    text_decriptat = biti_in_text(biti_decriptati)
    
    print(f"-> Bitii decriptati obtinuti    = {biti_decriptati}")
    print(f"-> Textul final decriptat      = '{text_decriptat}'")
    
    if text_original == text_decriptat:
        print("\n[Succes] Criptosistemul Blum-Goldwasser functioneaza corect!")
    else:
        print("\n[Eroare] Datele decriptate sunt corupte.")