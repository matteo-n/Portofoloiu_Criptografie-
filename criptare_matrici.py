import auxi
from sympy import Matrix

alfabet = auxi.citeste_alfabet("alfabet.txt")
text = "NOANSWER"
a = Matrix([[2, 3], [7, 8]])
b = Matrix([[0], [0]])
criptare = auxi.criptare_Hill(text, 2, a, b, alfabet)
print(criptare)
N = len(alfabet)

#print(criptat)
a_prim = a.inv_mod(N)
b_prim = -a_prim * b
decriptat = auxi.criptare_Hill(criptare, 2, a_prim, b_prim, alfabet)
print(decriptat)