import math

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

def teorema_chinezeasca_a_resturilor(resturi, moduli):
    """
    Rezolva un sistem de congruente liniare: x == r_i (mod m_i),
    unde moduli sunt primi intre ei doi cate doi.
    """
    N = math.prod(moduli)
    x_final = 0
    for r, m in zip(resturi, moduli):
        N_i = N // m
        inv = invers_modular(N_i, m)
        x_final = (x_final + r * N_i * inv) % N
    return x_final, N

def pohlig_hellman(g, h, p, factori_ordin):
    """
    Rezolva ecuatia logaritmului discret g^x == h (mod p) in cazul general,
    folosind descompunerea ordinului grupului (p - 1) in factori primi.
    
    :param g: baza (generator sau element cu ordin cunoscut)
    :param h: rezultatul exponentierii
    :param p: modulul (numar prim)
    :param factori_ordin: lista de tupluri (q, e) unde q^e divide (p - 1) si q este prim.
    """
    resturi = []
    moduli = []
    
    for q, e in factori_ordin:
        q_la_e = q ** e
        x_q = 0 
        g_baza = pow(g, (p - 1) // q, p)
        
        for i in range(e):
            exp = (p - 1) // (q ** (i + 1))
            
            g_inv_partial = invers_modular(pow(g, x_q, p), p)
            h_ajustat = (h * g_inv_partial) % p
            h_curent = pow(h_ajustat, exp, p)
            
            d_i = -1
            for d in range(q):
                if pow(g_baza, d, p) == h_curent:
                    d_i = d
                    break
            
            if d_i == -1:
                raise ValueError("Eroare matematica: Coeficientul subgrupului nu a putut fi determinat. "
                                 "Verificati daca h se afla in subgrupul generat de g.")
                
            x_q += d_i * (q ** i)
            
        resturi.append(x_q)
        moduli.append(q_la_e)
    x_final, _ = teorema_chinezeasca_a_resturilor(resturi, moduli)
    return x_final

if __name__ == "__main__":
    print("--- Algoritmul Pohlig-Hellman (Caz General) ---\n")
    
    p = 31
    g = 3
    h = 26
    factori = [(2, 1), (3, 1), (5, 1)] 
    
    print(f"Ecuatie de rezolvat: {g}^x == {h} (mod {p})")
    print(f"Descompunerea lui p - 1 ({p-1}): 2^1 * 3^1 * 5^1")
    
    try:
        x = pohlig_hellman(g, h, p, factori)
        print(f"\n[Rezultat] Solutia gasita: x = {x}")
        
        # Validare aritmetica finala
        verificare = pow(g, x, p)
        print(f"[Validare] Calculand {g}^{x} mod {p} obtinem: {verificare}")
        if verificare == h:
            print("-> Rezultat Corect! Identitatea este verificata.")
            
    except ValueError as e:
        print(f"\n[Eroare]: {e}")