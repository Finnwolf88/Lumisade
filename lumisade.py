import pygame
import random
from datetime import datetime

pygame.init()
pygame.display.set_caption("Joulu on tulossa!!!")
KOKO = (800, 600)
naytto = pygame.display.set_mode(KOKO)

class Hiutale:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sade = 1
        self.y_nopeus = random.uniform(0.3, 0.9) # Putoamisnopeus
        self.x_nopeus = random.uniform(-0.1, 0.1) # Sivuttaisliike
        self.putoaa = True
        self.laskeutunut = False  # Onko laskeutunut

    def paivita(self, maa, hiutaleet, lahjapaketit):
        if self.putoaa:
            self.y += self.y_nopeus
            self.x += self.x_nopeus

        if not self.laskeutunut:
            # Tarkista koskeeko muihin hiutaleisiin
            for hiutale in hiutaleet:
                if hiutale != self and hiutale.laskeutunut:
                    etaisyys = ((self.x - hiutale.x) ** 2 + (self.y - hiutale.y) ** 2) ** 0.5
                    if etaisyys < 2 * self.sade:
                        self.putoaa = False
                        if hiutale.laskeutunut:
                            self.laskeutunut = True
                        break

            # Tarkista koskeeko maahan
            if self.y >= maa:
                self.y = maa
                self.putoaa = False
                self.laskeutunut = True

            for lahjapaketti in lahjapaketit:
                if (
                    self.x + self.sade >= lahjapaketti.x
                    and self.x - self.sade <= lahjapaketti.x + lahjapaketti.leveys
                    and self.y + self.sade >= lahjapaketti.y
                    and self.y - self.sade <= lahjapaketti.y + lahjapaketti.korkeus
                ):
                    self.putoaa = False
                    self.laskeutunut = True

    def piirra(self, naytto):
        pygame.draw.circle(naytto, (255, 255, 255), (int(self.x), int(self.y)), self.sade)

class Lahjapaketti:
    def __init__(self, kuvake, x, y):
        self.kuva = pygame.image.load(kuvake)
        self.x = x
        self.y = y
        self.leveys = self.kuva.get_width()
        self.korkeus = self.kuva.get_height()

    def collider(self, hiutaleet):
        for hiutale in hiutaleet:
            if (
                hiutale.x + hiutale.sade <= self.x
                and hiutale.x - hiutale.sade <= self.x + self.leveys
                and hiutale.y + hiutale.sade >= self.y
                and hiutale.y - hiutale.sade <= self.y + self.korkeus
                and hiutale.laskeutunut
            ):
                hiutale.putoaa = False
                hiutale.laskeutunut = True
        
    def piirra(self, naytto):
        naytto.blit(self.kuva, (self.x, self.y))


def kello_renderi(aika_jouluun):
    aikaa = ""
    if aika_jouluun > 1:
        aikaa = f"{aika_jouluun} päivää"
    elif aika_jouluun == 1:
        aikaa = f"{aika_jouluun} päivä"
    else:
        aikaa = "Joulu on nyt!!!"
    fontti = pygame.font.Font(None, 36)
    teksti = fontti.render(f"Aikaa jouluun: {aikaa}", True, (200, 0, 0))
    naytto.blit(teksti, (260, 60))

hiutaleet = []
lumen_korkeus = [0] * KOKO[0]  # Pidä kirjaa lumen korkeudesta

lahjapaketit = [Lahjapaketti("paketti1.png", 100, 572), Lahjapaketti("paketti2.png", 153, 572),
                Lahjapaketti("paketti3.png", 207, 572), Lahjapaketti("paketti4.png", 260, 572),
                Lahjapaketti("paketti5.png", 110, 543), Lahjapaketti("paketti4.png", 168, 543),
                Lahjapaketti("paketti1.png", 245, 543), Lahjapaketti("paketti3.png", 141, 514),
                Lahjapaketti("paketti4.png", 205, 514), Lahjapaketti("paketti2.png", 170, 485)]

kello = pygame.time.Clock()
maksimi_hiutaleet = 400  # Hiutaleiden maksimimäärä

valmis = False
while not valmis:
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            valmis = True
    
    aika_nyt = datetime.now()
    jouluaatto = datetime(aika_nyt.year, 12, 24)
    aika_jouluun = (jouluaatto - aika_nyt).days

    naytto.fill((0, 0, 0))

    if len(hiutaleet) < maksimi_hiutaleet and random.randint(1, 100) <= 20: # Lumisateen intensiteetti
        x = random.randrange(0, 800)
        hiutaleet.append(Hiutale(x, -10))

    poistettavat_hiutaleet = []
    for hiutale in hiutaleet:
        hiutale.paivita(600, hiutaleet, lahjapaketit)
        hiutale.piirra(naytto)

        if hiutale.laskeutunut and hiutale.y >= 600:
            x = int(hiutale.x)
            if 0 <= x < KOKO[0]:
                lumen_korkeus[x] += 1  # Kasvata lumen korkeutta

        if not hiutale.putoaa and hiutale.laskeutunut and (hiutale.x <= 0 or hiutale.x >= KOKO[0] or hiutale.y <= 0 or hiutale.y >= KOKO[1]):
            poistettavat_hiutaleet.append(hiutale)

    for hiutale in poistettavat_hiutaleet:
        hiutaleet.remove(hiutale)

    for lahjapaketti in lahjapaketit:
        lahjapaketti.collider(hiutaleet)
        lahjapaketti.piirra(naytto)

    # Piirrä lumi maahan
    for x, korkeus in enumerate(lumen_korkeus):
        if korkeus > 0:
            pygame.draw.line(naytto, (255, 255, 255), (x, 600), (x, 600 - korkeus), 2)

    kello_renderi(aika_jouluun)

    pygame.display.flip()
    kello.tick(60)

pygame.quit()
