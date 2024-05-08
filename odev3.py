class Personel:
    def __init__(self, adi, departman, calisma_yili, maas):
        self.adi = adi
        self.departman = departman
        self.calisma_yili = calisma_yili
        self.maas = maas

class Firma:
    def __init__(self):
        self.personel_listesi = []

    def personel_ekle(self, personel):
        self.personel_listesi.append(personel)

    def personel_listele(self):
        for personel in self.personel_listesi:
            print("Adı:", personel.adi)
            print("Departmanı:", personel.departman)
            print("Çalışma Yılı:", personel.calisma_yili)
            print("Maaşı:", personel.maas)
            print()

    def maas_zammi(self, personel, zam_orani):
        personel.maas *= (1 + zam_orani / 100)

    def personel_cikart(self, personel):
        self.personel_listesi.remove(personel)


