import sqlite3
import odev


def benzerlik_hesapla(metin1, metin2, sample_size):
    frekans_metin1 = odev.letter_frequency_analysis(metin1, sample_size)
    frekans_metin2 = odev.letter_frequency_analysis(metin2, sample_size)
    
    print("Frequency of metin1:", frekans_metin1)
    print("Frequency of metin2:", frekans_metin2)
    
    benzerlik_orani = 0
    for char in frekans_metin1:
        if char in frekans_metin2:
            benzerlik_orani += min(frekans_metin1[char], frekans_metin2[char]) / max(frekans_metin1[char], frekans_metin2[char])
    
    return benzerlik_orani


conn = sqlite3.connect('metinler.db')
c = conn.cursor()



def jaccard_similarity(text1, text2):
    # Metinleri kelimelere ayır
    words_text1 = set(text1.split())
    words_text2 = set(text2.split())
    
    # Ortak kelimelerin ve toplam farklı kelimelerin sayısını bul
    intersection = len(words_text1 & words_text2)
    union = len(words_text1 | words_text2)
    
    # Jaccard benzerlik indeksini hesapla
    if union == 0:
        return 0.0
    else:
        return float(intersection) / float(union)



