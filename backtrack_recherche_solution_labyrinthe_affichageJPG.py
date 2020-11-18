from PIL import Image, ImageDraw
import time


def mazesolverBacktrack(name):
    print("Start : %s" % time.ctime())
    labyrinthe = []
    ListeDonees = open(f"{name}.txt").read().split()

    for ligne in ListeDonees:
        Listecaratere = []
        for caractere in ligne:
            Listecaratere.append(caractere)
        labyrinthe.append(Listecaratere)
    visited = [[0] * len(labyrinthe) for _ in range(len(labyrinthe))]

    class Noeuds:
        def __init__(self, position, parent):
            self.position = position
            self.parent = parent

        def __eq__(self, autre):
            return self.position == autre.position

    def test_validite(i, j):
        return (i >= 0 and i <= (len(labyrinthe)-1)) and (j >= 0 and j <= (len(labyrinthe)-1))

    def recheche_chemin_court(labyrinthe, entree, sortie):

        ListeCellulesAvisiter = []
        noeud_entree = Noeuds(entree, None)
        noeud_sortie = Noeuds(sortie, None)
        ListeCellulesAvisiter.append(noeud_entree)

        while len(ListeCellulesAvisiter) > 0:
            noeud_actuel = ListeCellulesAvisiter.pop(0)
            (a, b) = noeud_actuel.position
            visited[a][b] = 1
            if noeud_actuel == noeud_sortie:
                solution = []
                while noeud_actuel is not None:
                    solution.append(noeud_actuel.position)
                    noeud_actuel = noeud_actuel.parent
                return solution[::-1]
            (x, y) = noeud_actuel.position
            ListeVoisins = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for element in ListeVoisins:
                (i, j) = element
                if test_validite(i, j):
                    if(labyrinthe[i][j] == '#'):
                        continue
                    noeud_enfant = Noeuds(element, noeud_actuel)
                    (c, d) = noeud_enfant.position
                    if visited[c][d] == 1:
                        continue
                    ListeCellulesAvisiter.append(noeud_enfant)

    entree = (0, 0)
    sortie = (len(labyrinthe)-1, len(labyrinthe)-1)
    solution = recheche_chemin_court(labyrinthe, entree, sortie)
    if len(solution) == 0:
        print("no path found!")

    for path in solution:
        (x, y) = path
        labyrinthe[x][y] = 'o'

    for i in range(len(labyrinthe)):
        for j in range(len(labyrinthe)):
            if labyrinthe[i][j] == '.':
                labyrinthe[i][j] = '*'

   

    def mazeWrite(name):
        s = ""
        ths = open(f"{name}solution.txt", "a")
        for line in labyrinthe:
            s += "".join(line + ["\n"])
        ths.write(s)
        ths.close()
        createJPG()

    def createJPG():
        w = len(labyrinthe)
        large = 3*(w)
        img = Image.new('RGB', (large, large), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for y in range(w):
            for x in range(w):
                try:
                    if labyrinthe[y][x] == "#" and y % 2 == 1:
                        draw.line((3*x, 3*(y-1), 3*x, 3*(y+1)),
                                  fill=(0, 0, 0), width=1)
                    if labyrinthe[y][x] == "#" and y % 2 == 0 and x % 2 != 0:
                        draw.line((3*(x-1), 3*y, 3*(x+1), 3*y),
                                  fill=(0, 0, 0), width=1)
                    if labyrinthe[y][x] == "o" and x % 2 != 0:
                        draw.rectangle((3*(x-1), 3*(y-1), 3*(x+1), 3*(y+1)),
                                       fill=(175, 0, 175), width=1)

                except:
                    pass
        img.show()
        img.save(f"{name} solution.jpg")

    print("End : %s" % time.ctime())
    mazeWrite(name)


name = input("Entrer le nom de maze: ")
mazesolverBacktrack(name)