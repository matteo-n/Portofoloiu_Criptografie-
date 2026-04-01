import auxi
from collections import Counter

# Alfabetul de 76 caractere
alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789():; .,!?-'"
N = len(alfabet)

def get_frequencies(text):
    result = Counter()
    for ch in text:
        result[ch] += 1
    return result

def cesar_break(text_criptat, alfabet):
    N = len(alfabet)
    frecvente = get_frequencies(text_criptat)
    # Identificăm cel mai frecvent caracter din textul criptat [cite: 55]
    cel_mai_frecvent_criptat = max(frecvente, key=frecvente.get)
    idx_criptat = alfabet.index(cel_mai_frecvent_criptat)
    
    # Presupunem că în textul clar, cel mai frecvent caracter este SPATIUL (index 66)
    # k = (idx_clar - idx_criptat) % N [cite: 55]
    idx_spatiu = alfabet.index(" ")
    k = (idx_spatiu - idx_criptat) % N
    
    # Decriptăm folosind cheia găsită
    res = ""
    for ch in text_criptat:
        res += alfabet[(alfabet.index(ch) + k) % N]
    return res, k

text_criptat = "w K h?NhBGMK FhBGhI F GMh!?hKNLBG?jhLBh, MhI?h,?hL hF hBG?,jh!?h,BN! h,?mFBh?K ihLBh!BGh!K 'HLM? h,? hF K?h!?hF Bh!BGBH K? jhBFBhO?G? h ,NFhL hE?hLMK G'h!?h' MjhGNh EM ,?O ihr KhOHK. h,?? fh3HMBhHIKBhO GMNEjh I hLBh'NKBE?hH F?GBEHKlhr?m ,?? hE?m FhE L MhLBh?NhI?h-?M?hL hK ! jhI G hEBhLm h!N,?h'NK hE hNK?,A?jhLBhI G!BG!hOK?F?hI?h, G!hL?!h?E?hIE?, M?hLBh! NhI GS hBGh I hE h'ABEBMjh- ,hMNLMBkh!BGh. EM hLmHhB NhE hL G MH L ghLBh L h-N'? Fh!?hM K?hI?hIKNG!jh!?hL K? NhIB?MK?E?jhI?h, K?hE?hLM KG? Fh,NhIB,BH K?E?jh, MhFBG?h!?hLNLihLBh-N' jhLBh-N' jh- K hL hF hNBMhBGhNKF jhI G h,?h! NhBGMK?hAN!BMBjhI?h!KNFNEh, K?h!N,? hE hGHBh , L ihr KhGNhF?K'hI?h!KNFjh!?hKNLBG?hL hGNhBGM EG?L,hOKNGhHFjh,BhL KhBGh'K !BG hENBhqHLM ,A?hLBhF?K'hMNIBENLhIKBGhI INLHBgh IHBhBGMKmHhAN!BM jh!BGhAN!BM hBGh'K !BG hE h7K LG? jhLBhB KhIKBGhI INLHBghLBh, G!h IKH I?hL hB?Lh!BGh'K !BG jhF hLBFM?L,h, BGBBhENBh7K LG? jhLBhE hFBG?jhL hF hKNI khq?mBh!?h- ,NMlhoNSBL?Fh?Nh!BGhH F?GBh, jh! , hOK?BhL hGNhM?hFNLM?h, BGBBhLBhL hM?hE L?hBGhI ,?jh,NFhBBhO?SBh, hL KhE hMBG?jhL hM?hMNIBE?SBhCHLhE hI F GMhLBhL mBhE LBhL hM?hE MK?h, MhE?hIE ,?jh- K hL hM?hNKG?LMBh!BGhEH,gh, ,Bh?Bh. Mh, Mh. MhLBjh!?hE hHhOK?F?jhM?hI K L?L,hLBhL?h!N,ihLBh !?O K Mh?LM?jh, ,Bh L h FhL, I MhLBh?Nh!?h, BGBBhENBh7K LG? jh MNG,Bh, G!h Fh! MhI?LM?hI , Mh,Nh?BhLBh?Bh,NhFBG?i"

decriptat, cheia_gasita = cesar_break(text_criptat, alfabet)
print(f"Cheia gasita: {cheia_gasita}")
print(decriptat)