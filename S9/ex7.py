import random


def adunare_matrice(A, B, p):
    """Aduna doua matrice 2x2 modulo p."""
    return [
        [(A[0][0] + B[0][0]) % p, (A[0][1] + B[0][1]) % p],
        [(A[1][0] + B[1][0]) % p, (A[1][1] + B[1][1]) % p]
    ]

def inmultire_matrice(A, B, p):
    """Inmulteste doua matrice 2x2 modulo p."""
    C = [[0, 0], [0, 0]]
    C[0][0] = (A[0][0]*B[0][0] + A[0][1]*B[1][0]) % p
    C[0][1] = (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % p
    C[1][0] = (A[1][0]*B[0][0] + A[1][1]*B[1][0]) % p
    C[1][1] = (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % p
    return C

def putere_matrice(A, n, p):
    """Calculeaza A^n modulo p folosind ridicarea la putere rapida."""
    rezultat = [[1, 0], [0, 1]]
    baza = [row[:] for row in A]
    
    while n > 0:
        if n % 2 == 1:
            rezultat = inmultire_matrice(rezultat, baza, p)
        baza = inmultire_matrice(baza, baza, p)
        n //= 2
    return rezultat

def genereaza_matrice_inversabila(p):
    """Genereaza o matrice aleatorie 2x2 inversabila modulo p (determinantul != 0 mod p)."""
    while True:
        A = [
            [random.randint(1, p - 1), random.randint(1, p - 1)],
            [random.randint(1, p - 1), random.randint(1, p - 1)]
        ]
        det = (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % p
        if det != 0:
            return A

class CayleyPurser:
    @staticmethod
    def genereaza_chei():
        """
        Pasul 1: Alegerea cheilor
        Se alege un numar prim mare p.
        Se aleg aleatoriu doua matrice inversabile A si B care NU comuta (A*B != B*A).
        Se alege un intreg secret r si se calculeaza C = A^r.
        """
        p = 7919 
        
        while True:
            A = genereaza_matrice_inversabila(p)
            B = genereaza_matrice_inversabila(p)
            
            # Verificam ca A si B sa nu comute
            AB = inmultire_matrice(A, B, p)
            BA = inmultire_matrice(B, A, p)
            if AB != BA:
                break
                
       
        r = random.randint(2, p - 1)
        
       
        C = putere_matrice(A, r, p)
        cheie_publica = (p, A, B, C)
        cheie_privata = r
        
        return cheie_publica, cheie_privata

    @staticmethod
    def criptare(M, cheie_publica):
        """
        Pasul 2: Criptare
        Mesajul este codificat sub forma unei matrice M de 2x2.
        Se alege un numar aleatoriu s.
        Se calculeaza:
          U = B^(-1) * A^s * B  <- In algoritmul CP standard, asta se genereaza prin structura
          In varianta optimizata Cayley-Purser:
          Se alege s si se calculeaza textul cifrat format din perechea (U, V):
          U = B * (A^s) * B
          V = C^s * M * C^s = A^(rs) * M * A^(rs)
        """
        p, A, B, C = cheie_publica
        
        s = random.randint(2, p - 1)
        
        A_la_s = putere_matrice(A, s, p)
        U = inmultire_matrice(B, A_la_s, p)
        U = inmultire_matrice(U, B, p)
        
        C_la_s = putere_matrice(C, s, p)
        V = inmultire_matrice(C_la_s, M, p)
        V = inmultire_matrice(V, C_la_s, p)
        
        return (U, V)

    @staticmethod
    def decriptare(criptotext, cheie_publica, cheie_privata):
        """
        Pasul 3: Decriptare
        Folosind exponentul privat r, putem reface mesajul M prin operatia:
        M = U^(-r) * V * U^(-r)  -> echivalent cu inmultirea repetata folosind proprietatea:
        Deoarece U = B * A^s * B, ridicarea lui U la puterea secretului r (sau p-1-r) 
        anuleaza mastile combinate cu V.
        """
        p, A, B, C = cheie_publica
        r = cheie_privata
        U, V = criptotext
        
        U_la_r = putere_matrice(U, r, p)
        det = (U_la_r[0][0]*U_la_r[1][1] - U_la_r[0][1]*U_la_r[1][0]) % p
        det_inv = invers_modular(det, p)
        
        U_la_r_inv = [
            [(U_la_r[1][1] * det_inv) % p, (-U_la_r[0][1] * det_inv) % p],
            [(-U_la_r[1][0] * det_inv) % p, (U_la_r[0][0] * det_inv) % p]
        ]
        
        M_decriptat = inmultire_matrice(U_la_r_inv, V, p)
        M_decriptat = inmultire_matrice(M_decriptat, U_la_r_inv, p)
        
        return M_decriptat

def invers_modular(a, m):
    """Calculeaza inversul unui numar modulo m folosind Euclid Extins."""
    a = a % m
    if a < 0:
        a += m
    if a == 0:
        return 0
    
    m0, y, x = m, 0, 1
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x

if __name__ == "__main__":
    print("--- Criptosistemul Cayley-Purser --- \n")
    
    pub_key, priv_key = CayleyPurser.genereaza_chei()
    p, A, B, C = pub_key
    
    print(f"[Setari] Modulul prim p = {p}")
    print(f"[Cheie Publica] Matricea A = {A}")
    print(f"[Cheie Publica] Matricea B = {B}")
    print(f"[Cheie Publica] Matricea C (A^r) = {C}")
    print(f"[Cheie Privata] Exponentul secret r = {priv_key}\n")
    
    M_original = [
        [101, 202],
        [303, 404]
    ]
    print(f"-> Matricea mesaj original (M) = {M_original}\n")
    
    criptotext = CayleyPurser.criptare(M_original, pub_key)
    U_cifrat, V_cifrat = criptotext
    print(f"-> Criptotextul generat:")
    print(f"   U = {U_cifrat}")
    print(f"   V = {V_cifrat}\n")
    
    M_decriptat = CayleyPurser.decriptare(criptotext, pub_key, priv_key)
    print(f"-> Matricea decriptata de receptor = {M_decriptat}")
    
    if M_original == M_decriptat:
        print("\n[Succes] Decriptarea matriciala a fost realizata cu succes!")
    else:
        print("\n[Eroare] Matricea decriptata nu coincide cu cea original.")