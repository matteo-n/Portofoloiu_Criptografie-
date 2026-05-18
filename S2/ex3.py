import sys

# Forțăm terminalul să folosească UTF-8 pentru afișare pe sistemele Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def euler_totient(n):
    """
    Calculează eficient funcția indicatoare a lui Euler, phi(n),
    folosind descompunerea în factori primi.
    
    Complexitate temporală: O(sqrt(n))
    Complexitate spațială: O(1)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
        
    rezultat = n
    p = 2
    
    # Căutăm factorii primi ai lui n până la partea întreagă din sqrt(n)
    while p * p <= n:
        # Dacă p este un divizor prim al lui n
        if n % p == 0:
            # Actualizăm rezultatul conform formulei: rezultat = rezultat * (1 - 1/p)
            # Folosim împărțirea întreagă (//) pentru a menține precizia la numere mari
            rezultat -= rezultat // p
            
            # Eliminăm complet factorul p din n prin împărțiri repetate
            while n % p == 0:
                n //= p
        p += 1
        
    # Dacă la finalul buclei n a rămas mai mare decât 1, înseamnă că
    # n-ul rămas este el însuși un număr prim (ultimul factor prim din descompunere)
    if n > 1:
        rezultat -= rezultat // n
        
    return rezultat  # Aici a fost corectat din 'resultado' în 'rezultat'

# --- Secțiune de testare a algoritmului ---
if __name__ == "__main__":
    print("--- Testare Funcția Indicatoare a lui Euler ---")
    
    # 1. Test cu un număr mic din seminar (Exemplul 5)
    n_mic = 100
    print(f"phi({n_mic}) = {euler_totient(n_mic)}  (Așteptat: 40)")
    
    # 2. Test cu un număr prim (phi(p) trebuie să fie p - 1)
    p_prim = 97
    print(f"phi({p_prim}) = {euler_totient(p_prim)}  (Așteptat: 96)")
    
    # 3. Test cu un număr mare (produsul a două numere prime mari consecutive)
    # 1000003 (număr prim) * 1000033 (număr prim) = 1000036000099
    n_mare = 1000036000099
    # Valoarea așteptată este (p-1)*(q-1) = 1000002 * 1000032 = 1000034000064
    print(f"phi({n_mare}) = {euler_totient(n_mare)} (Așteptat: 1000034000064)")