import sys
from collections import Counter

# Setam encoding-ul pentru a evita erorile de afisare in terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Alfabetul de 76 caractere din alfabet.txt
alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789():; .,!?-'"
N = len(alfabet)

text_criptat = "cG0bdtTIlbgpTV1AOI:Gu8244ut,btWuz,2t'umHUpVuz,2t0umHUpVuz,2t'umHUpVuz,2t0umHUpVuw8bpTIlbRp:uj8bt.GAGcp-GACO00Tj8200uw8ap;Z'bQp2OCbgpTT1bg4'TA'W22O1AWKTKy8iIAXvbnt2KF)c90YwES 4Ilbd60PpAWI3KA(O24Vhd2u!atBO70uz,2s4Gz82r'SA,WI.Ky,OKTJlbQp!KAAiI?zhbO04YAAW18Ihc278ukHdpTIlbTp2Ktbb38u0ESq'Yv8fpTGzGOKTShGi70wAAiI?ZpH2r'SCbgtTOu(O02KzGSI.XpA2r0TlCOKTUy,274up'dx4Jp(OI3KA(S(0wAFWI2Gk:2y YBb;9VuhGi22OCbW9-KA'OI!GzHQt?IA,b8!z1A248IpBfKTLh(2(!UA)c90uz8fx-ay,210OACc8!O2,htVut82pEbhEZI.KzGSI6Gy)4I3KACO62GAAWr8uuH20YGtbO88Tzd278zt,248Ky)29!Shd2s'IhAR9YShbOr0YhbgxTLp,bsTLv8f84ujHax;ZlbW2TfpHOI0Il:OJUvBb:p!ut8WI8TA)S74Gy84I8Gj8278utBgIvGz,ZtVujH2( Xu,Q9)uz,240fu,Q9)wAFh68MhbdtTZhGOI)GACcp!Zhd2x8uzCi2TVy,Qx;GAFWN)uj.Sp:GAFOI5OlbRtTLhGOI2Gu)27YGA,g40YpbQp;Kw8278uj,ft?Ks:3JUuj8QxVukES4-u2Bfq8Tkd278utBgIvGz,ZtTKy829;uj8f40TvF27Yaubd98uk:2 6Gy,SN1XhAnpVuj8278ut8h9?GAuO68UhEOJTBvEPpTIl:OGT1AGi20ZAFWI8zhbOs'ThG3I8Tz82s4Ml8PpTSh,2r)GtCO24YjbS9TJpA2v'XhZ2r8TlbQtTGy:2r'utHbr0uv'i0'OEbG8!Oj8Qx'Tl8274um8Q9?KCbgxTbpAc(0Z1-28!KiHWpTYhbd00Zl8gr0vA3c61GA(St0sAviI.RhGS7-KA9cv0Z1-4I2OAIW2 bhGi0UuHFOI?OAGO80sA82s0ZA Z30Hhbdt;ZyH218Tld278uw8QtTH1AOLTYpbR9.GA(SN0u2:bx-ul-26'YpAO8TJlbZpTOzCO70wA'WN0u0EO7TUA(Vt)LhASp)GA(OI0Il:OKTfp(O23sAgBpWuz8h9!GFGSI3KA(W64Yle2S4zh'iI?GAFhx8uj8288zh,210Tj8hI)OmGW68GA)SI)GA'W24wAFdp;f1EO8'Rle2d0Xlba9)Zlbg8!Oj8Qx'TpbO1TYhbap8uw-O84YjbS9TVlbi6:GAGOMTYpbWp2GA8gpTI1bQx!Kz:ZtSuzgOI8Sw-W28ZAIc61GA'O14OCbgp!ShAOKTO1GSI?OA)Sv!Gi80IcGAli1;K6:iI;zh!i80uj:Z98uj8ftTat9ZpTI1bT9!ZpFOvUu"

# 1. Detectarea lungimii cheii (L)
def gaseste_L(txt):
    best_l = 0
    max_score = 0
    for l in range(1, 16):
        # Analizam prima coloana pentru fiecare lungime posibila
        subset = txt[::l]
        frecv = Counter(subset).most_common(1)[0][1] / len(subset)
        if frecv > max_score:
            max_score = frecv
            best_l = l
    return best_l

L = gaseste_L(text_criptat)
print(f"Lungime cheie detectata: {L}")

# 2. Spargerea cheii
def dectripteaza(txt, lungime):
    cheie = ""
    # In limba romana, cel mai frecvent caracter este SPATIU (index 66)
    idx_spatiu = alfabet.index(" ")
    
    for i in range(lungime):
        coloana = txt[i::lungime]
        cel_mai_frecvent_criptat = Counter(coloana).most_common(1)[0][0]
        idx_c = alfabet.index(cel_mai_frecvent_criptat)
        
        # k = (c - p) mod N
        idx_k = (idx_c - idx_spatiu) % N
        cheie += alfabet[idx_k]
    
    print(f"Cheia detectata: {cheie}")
    
    # Decriptare finala
    clar = ""
    for i in range(len(txt)):
        idx_c = alfabet.index(txt[i])
        idx_k = alfabet.index(cheie[i % lungime])
        idx_p = (idx_c - idx_k) % N
        clar += alfabet[idx_p]
    return clar

if L > 0:
    print("\n--- REZULTAT PROBLEMA 4 ---")
    print(dectripteaza(text_criptat, L))