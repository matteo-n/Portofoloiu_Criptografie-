import sys

# Forțăm terminalul să folosească UTF-8 pentru afișare pe sistemele Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def euclid_extins(a, b):
    """
    Implementarea Algoritmului lui Euclid Extins.
    Returnează un tuplu de forma (d, u, v) unde:
    d = cmmdc(a, b)
    u, v = coeficienții Bézout astfel încât d = u * a + v * b
    """
    # Păstrăm semnele inițiale pentru a gestiona eventualele numere negative
    semn_a = -1 if a < 0 else 1
    semn_b = -1 if b < 0 else 1
    
    a, b = abs(a), abs(b)
    
    # Inițializarea coeficienților Bézout conform algoritmului din seminar
    # u1, v1 corespund vectorului x_a = (1, 0)
    u1, v1 = 1, 0
    # u2, v2 corespund vectorului x_b = (0, 1)
    u2, v2 = 0, 1
    
    # Bucla principală a algoritmului lui Euclid
    while b != 0:
        cat = a // b
        rest = a % b
        
        # Actualizarea valorilor pentru a și b
        a = b
        b = rest
        
        # Calcularea noilor coeficienți recursivi: x_r = x_a - q * x_b
        u_nou = u1 - cat * u2
        v_nou = v1 - cat * v2
        
        # Glisarea coeficienților pentru pasul următor
        u1, v1 = u2, v2
        u2, v2 = u_nou, v_nou
        
    # Ajustăm coeficienții finali în funcție de semnele inițiale ale numerelor
    u1 = u1 * semn_a
    v1 = v1 * semn_b
    
    return a, u1, v1

# --- Exemplu de testare folosind datele din Exemplul 3 din seminar ---
if __name__ == "__main__":
    nr1 = 360
    nr2 = 294
    
    # Apelul corect al funcției
    cmmdc, u, v = euclid_extins(nr1, nr2) 
    
    print(f"CMMDC({nr1}, {nr2}) = {cmmdc}")
    print(f"Coeficienții Bézout: u = {u}, v = {v}")
    print(f"Verificare: {u} * {nr1} + ({v}) * {nr2} = {u * nr1 + v * nr2}")