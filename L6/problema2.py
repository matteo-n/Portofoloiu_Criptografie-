import auxi
from sympy import Matrix
from collections import Counter

# 1. Încărcăm alfabetul și textul exact ca în seminar
alfabet = auxi.citeste_alfabet("alfabet.txt") # 
N = len(alfabet)
text_criptat = "Qj5j9Xw9L!z5j'9L!9)j'j!z9aX95w2L!X392L9djz9)X9dX92j9'j9L!Xd39aX9dLwaj9dXu'L9X5j692L9aL!9a5jR 2zXj9dXj9'j5X9aX9'jL9aL!L j5Xj39L'L9tX!Xj9jdw'92j9CX92z5j!R9aX9Rjz39!w9jCzjdXtj69fj59t 5gj9dXXj.9, zL9 )5L9tj!zwC39j)j92L9Rw5LCX9 j'X!LC 5x9fXujdXXj9CXuj'9Cj2jz92L9Xw9)X9UXzX92j95jaj39)j!j9CL92uj9awdX9Rw5j9Cj9w5XdOX392L9)j!aL!a9t5X'X9)X9dj!a92Xa9XCX9)CXdjzX92L9ajw9)j!hj9L!9j)j9Cj9ROLCLz39Ujd9zw2zL09aL!9gjCzj92u 9Ljw9Cj92j!jz j2j:92L9j2j9UwRXj'9aX9zj5X9)X9)5w!a39aX92j5Xjw9)LXz5XCX39)X9dj!a92Xa9XCX9)CXdjzX92L9ajw9)j!hj9L!9j)j9Cj9ROLCLz39Ujd9zw2zL09aL!9gjCzj92u 9Ljw9Cj92j!jz j2j:"

# 2. Funcția de invers modular din document [cite: 69-77]
def invers(a, N):
    x1, x2, copy = 1, 0, N
    while N:
        r = a % N
        x = x1 - (a // N) * x2
        x1, x2 = x2, x
        a, N = N, r
    if a == 1: return x1 % copy
    return None

# 3. Analiza frecvențelor pentru a găsi cheia [cite: 81]
def spargere_afina(text, alfabet):
    N = len(alfabet)
    frecvente = Counter(text).most_common(5)
    
    # Încercăm combinații de caractere frecvente (Spațiu, a, e, i, n)
    # După structura textului, 'j' și '9' par a fi Spațiu și 'a'
    c0 = alfabet.index(frecvente[0][0]) # Cel mai frecvent din criptat
    c1 = alfabet.index(frecvente[1][0]) # Al doilea cel mai frecvent
    
    # Ipoteză: j -> ' ' (spațiu) și 9 -> 'a'
    p0 = alfabet.index(" ")
    p1 = alfabet.index("a")
    
    # Sistem: a*p0 + b = c0 (mod N) și a*p1 + b = c1 (mod N)
    # Rezultă: a = (c0 - c1) * inv(p0 - p1) (mod N)
    diff_p = (p0 - p1) % N
    diff_c = (c0 - c1) % N
    inv_p = invers(diff_p, N)
    
    if inv_p is not None:
        a = (diff_c * inv_p) % N
        b = (c0 - a * p0) % N
        return a, b
    return None, None

# 4. Calcul cheie și decriptare
a, b = spargere_afina(text_criptat, alfabet)

if a:
    # Pentru decriptare avem nevoie de a_prim și b_prim
    a_mat = Matrix([[a]])
    b_mat = Matrix([[b]])
    a_prim = a_mat.inv_mod(N)
    b_prim = (-a_prim * b_mat) % N
    
    text_decriptat = auxi.criptare_Hill(text_criptat, 1, a_prim, b_prim, alfabet)
    print(text_decriptat)
else:
    print("Nu s-a putut găsi o cheie validă.")