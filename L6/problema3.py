import auxi
from sympy import Matrix
import random

# alfabet
alfabet = auxi.citeste_alfabet("alfabet.txt")
N = len(alfabet)

# text criptat
text_criptat = """PASTE TEXTUL TAU AICI"""

# scor simplu de lizibilitate
def scor_text(text):
    scor = 0
    cuvinte = [" the ", " si ", " este ", " in ", " la ", " and ", " to "]
    for w in cuvinte:
        scor += text.lower().count(w) * 10
    
    # penalizare pentru caractere ciudate
    scor -= sum(1 for c in text if c not in alfabet)
    
    return scor


def random_matrix():
    while True:
        a = random.randint(0, N-1)
        b = random.randint(0, N-1)
        c = random.randint(0, N-1)
        d = random.randint(0, N-1)

        a, b, c, d = [random.randint(0, N-1) for _ in range(4)]
        A = Matrix([[a, b], [c, d]])
        try:
            A.inv_mod(N)
            return A
        except:
            continue


best_score = -999999
best_text = "tRJLjQe(-xex.h)!He)!.) Yep)IJ(td-6gsI1eSDHHpCH AI1gs;Me.)meZEm Y)nDrgsE6ChBD-K.) YeZHR:Bex.);MF,BXCHC4-Ae9-vJQefKE)I-9IEj0ef;B)t); ADWIk)t-d.!e BD-ief)j-9D,L: Y)z;Mef-9IEeSDf.LFqe j0eZ.x.) ADWDgK9eTDWJQ)I;: YefKE)I.);4EfJQgsDrBDex)I)jDW!2-E wgs)zJQFB);;mIeJ Bdex-6FB)IKp-ieSDWBs-p);D;)h.Le2-E.h-9J;DT); Ye2EG wdJHe)t);I1 Y);-Ee.-cBh;mBX;MI1-xef-9;MD!HpeZEGHG);D!eqHpex.GJLK3:xJoJ HphHIa)!EfgsLcHj);;9.LcuyJef. .Lgs;Mj7-9I1 Ye9EyE.KKdJJQL:ew.),v;mJTBsefK:)U)-e2E(-Qew.)JoJoeSDW)U:B.zex.)BsDH);)UJ;-9LKE6;lDf-fIEI1gs;MHRe Ik..JoK3IEeA.),v;lew.M)I;MHRfI4Y.L:xeqHpe ;BBhgsD!eSDfKv;MBsdJIdeSDf);I1e2.3.Lew.wHp:xgs;M;leN.G.Le2K3,A!KeS)5CHHe;mBX Yeu)UJ;;9D,gs;MHRe ;9BseqIk.);9eqIk.5ef-9CHef;B)U);CHCHe J Df-9CH-9 ACgDT)t); Y;MJT)UJQew)t-9Idjc-9P(;9e2K3Jd)t);-E-K)EePe--?)1ewHp!kBXCHC4-reN.H-9;MeZ)t)jJoK3.) BI4Bse2EGIEgs;M;lef.)I;KjKv);Ea)zKKe2.S);FSeMEsdJIdeqK3)z.M.G.)D!jc-9Ln b;MF,BX YeZHR:BdJJ e.)meA)z); TKEKv-Q.)IdefJo-9BsDH);CHCh;Mgs Yj0ek);JQL:ef-9BU)y)I);;BF.B?Bde2jbFf-9IdeqK3J;jQ-9B?); YeA);q8BD-?.G-9E6FqBsH Kj);;meZ)zCHefjQe2Kv)UKp); Ye2.S.);me2?-C4H gsIk-ie2EN;0e2);FSDCH.eZ-E.tePe?-E.ze.)O)vew)5gs-Eee)I BBXC4Kre9KE)meqK3Ik-JC1ejEGJQe2);Jd)t.S.zew)5eA);;mIeJTIdef)5),KcJTIeCHDTef-9CH-9)U.xeA);He)t)1e.);-EJL.'.LC7;mek.r.S.);9BUe.)5-9 ADWJdHGdJIdew-Ee Ik);FN-?-E)1el)nJo;lEGIEew.)xUH K:);3RL;;mB?-xe2)5.zewHRFBef);LnefF,DKe9KZCgeqHpeTHpJogs,v;9);),.x.AH eSDW;lK6);C4);Idjc-9:xJQ); ADWF,CC-xexEy.'B!DZKZCHecEBejEy;MBsKre2KEeS-9P(;9);K-KceZ-u)Iew-EeX)I)tEy-3ecDI);FSDCH.e Ik);JdJT-K-9.3); T)y)1ef-9JdHd.LC7-KFN.lDre2K3 wDI)1eA);KE:U);D!;mB?-9BhHIe2)t.hE6C!L:Bsew.) TKo-9 Ye2)IKv)1ew.)CHef)5Kj);CHCHgs;MDZeSeA.))5)t)Oef.LHpe ;MIEfI"
best_key = None

ITERATII = 5000  # crește dacă vrei rezultate mai bune

for i in range(ITERATII):
    A = random_matrix()
    b = Matrix([[random.randint(0, N-1)], [random.randint(0, N-1)]])
    
    try:
        A_inv = A.inv_mod(N)
        b_inv = -A_inv * b
        
        text = auxi.criptare_Hill(text_criptat, 2, A_inv, b_inv, alfabet)
        s = scor_text(text)
        
        if s > best_score:
            best_score = s
            best_text = text
            best_key = (A, b)
            
            print("\n=== POSIBIL TEXT BUN ===")
            print(text[:500])
            print("\nCheie:")
            print("A =", A)
            print("b =", b)
            print("Scor:", s)
            
    except:
        continue

print("\n\n=== CEL MAI BUN REZULTAT ===")
print(best_text)

print(best_key)