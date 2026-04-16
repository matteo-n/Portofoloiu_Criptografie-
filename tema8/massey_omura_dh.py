"""
Implementare Massey-Omura si Diffie-Hellman
"""

# ─────────────────────────────────────────────────────────────
# Utilitare aritmetice
# ─────────────────────────────────────────────────────────────

def mod_exp(base: int, exp: int, mod: int) -> int:
    """Ridicare la putere modulara eficienta (square-and-multiply)."""
    return pow(base, exp, mod)

def mod_inv(a: int, m: int) -> int:
    """Inversul modular al lui a mod m (algoritmul extins al lui Euclid)."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"{a} nu are invers modular fata de {m}")
    return x % m

def extended_gcd(a: int, b: int):
    """Algoritmul extins al lui Euclid: returneaza (gcd, x, y) cu a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

# ─────────────────────────────────────────────────────────────
# Criptosistemul Massey-Omura
# ─────────────────────────────────────────────────────────────

class MasseyOmura:
    """
    Protocol Massey-Omura pe Z_p*.
    
    Parametri publici: p (numar prim)
    Alice: cheie privata eA, cu gcd(eA, p-1) = 1
    Bob  : cheie privata eB, cu gcd(eB, p-1) = 1
    """

    def __init__(self, p: int):
        self.p = p
        self.phi = p - 1          # phi(p) = p-1 pentru p prim

    def generate_keys(self, e: int):
        """
        Genereaza perechea (e, d) unde d = e^{-1} mod (p-1).
        e trebuie sa fie coprim cu p-1.
        """
        from math import gcd
        if gcd(e, self.phi) != 1:
            raise ValueError(f"e={e} nu este coprim cu phi={self.phi}")
        d = mod_inv(e, self.phi)
        return e, d

    def encrypt(self, M: int, e: int) -> int:
        """Criptare: C = M^e mod p."""
        return mod_exp(M, e, self.p)

    def decrypt(self, C: int, d: int) -> int:
        """Decriptare: M = C^d mod p."""
        return mod_exp(C, d, self.p)

    def protocol(self, M: int, eA: int, eB: int):
        """
        Simuleaza protocolul complet in 3 pasi:
          Pas 1: Alice trimite C1 = M^{eA} mod p
          Pas 2: Bob   trimite C2 = C1^{eB} mod p = M^{eA*eB}
          Pas 3: Alice trimite C3 = C2^{dA} mod p = M^{eB}
          Final: Bob   calculeaza M = C3^{dB} mod p
        """
        p = self.p
        _, dA = self.generate_keys(eA)
        _, dB = self.generate_keys(eB)

        print("=" * 55)
        print("  PROTOCOL MASSEY-OMURA")
        print(f"  Parametru public: p = {p}")
        print(f"  Mesaj original:   M = {M}")
        print("=" * 55)
        print(f"\n[Chei]")
        print(f"  Alice: eA={eA}, dA={dA}  (eA*dA ≡ {(eA*dA) % (p-1)} mod {p-1})")
        print(f"  Bob  : eB={eB}, dB={dB}  (eB*dB ≡ {(eB*dB) % (p-1)} mod {p-1})")

        # Pas 1: Alice → Bob
        C1 = self.encrypt(M, eA)
        print(f"\n[Pas 1] Alice → Bob")
        print(f"  C1 = M^eA mod p = {M}^{eA} mod {p} = {C1}")

        # Pas 2: Bob → Alice
        C2 = self.encrypt(C1, eB)
        print(f"\n[Pas 2] Bob → Alice")
        print(f"  C2 = C1^eB mod p = {C1}^{eB} mod {p} = {C2}")

        # Pas 3: Alice → Bob
        C3 = self.decrypt(C2, dA)
        print(f"\n[Pas 3] Alice → Bob")
        print(f"  C3 = C2^dA mod p = {C2}^{dA} mod {p} = {C3}")

        # Final: Bob decripteaza
        M_rec = self.decrypt(C3, dB)
        print(f"\n[Final] Bob decripteaza")
        print(f"  M  = C3^dB mod p = {C3}^{dB} mod {p} = {M_rec}")

        ok = "✓ CORECT" if M_rec == M else "✗ EROARE"
        print(f"\n  Mesaj recuperat: {M_rec}  {ok}")
        print("=" * 55)
        return C1, C2, C3, M_rec

# ─────────────────────────────────────────────────────────────
# Schimbul de chei Diffie-Hellman
# ─────────────────────────────────────────────────────────────

class DiffieHellman:
    """
    Schimb de chei Diffie-Hellman pe Z_p*.
    Parametri publici: p (prim), g (generator).
    """

    def __init__(self, p: int, g: int):
        self.p = p
        self.g = g

    def public_key(self, secret: int) -> int:
        """Cheie publica: g^secret mod p."""
        return mod_exp(self.g, secret, self.p)

    def shared_key(self, their_public: int, my_secret: int) -> int:
        """Cheie comuna: their_public^my_secret mod p."""
        return mod_exp(their_public, my_secret, self.p)

    def protocol(self, a: int, b: int):
        """Ruleaza protocolul DH si afiseaza toti pasii."""
        p, g = self.p, self.g
        print("=" * 55)
        print("  SCHIMB DE CHEI DIFFIE-HELLMAN")
        print(f"  Parametri publici: p={p}, g={g}")
        print("=" * 55)

        # Chei private
        print(f"\n[Chei private]")
        print(f"  Alice: a = {a}")
        print(f"  Bob  : b = {b}")

        # Chei publice
        A = self.public_key(a)
        B = self.public_key(b)
        print(f"\n[Chei publice trimise]")
        print(f"  Alice trimite: A = g^a mod p = {g}^{a} mod {p} = {A}")
        print(f"  Bob   trimite: B = g^b mod p = {g}^{b} mod {p} = {B}")

        # Chei comune
        kA = self.shared_key(B, a)
        kB = self.shared_key(A, b)
        print(f"\n[Cheie comuna calculata]")
        print(f"  Alice: k = B^a mod p = {B}^{a} mod {p} = {kA}")
        print(f"  Bob  : k = A^b mod p = {A}^{b} mod {p} = {kB}")

        ok = "✓ CORECT — chei identice!" if kA == kB else "✗ EROARE"
        print(f"\n  Cheie secreta k = {kA}   {ok}")
        print("=" * 55)
        return A, B, kA

# ─────────────────────────────────────────────────────────────
# Demonstratie
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Massey-Omura ──────────────────────────────────────────
    print("\n" + "█" * 55)
    print("  DEMO MASSEY-OMURA")
    print("█" * 55)
    mo = MasseyOmura(p=31)
    mo.protocol(M=13, eA=7, eB=11)

    # ── Diffie-Hellman (problema din enunt) ───────────────────
    print("\n" + "█" * 55)
    print("  DEMO DIFFIE-HELLMAN  (p=17, g=5, a=3, b=6)")
    print("█" * 55)
    dh = DiffieHellman(p=17, g=5)
    dh.protocol(a=3, b=6)
