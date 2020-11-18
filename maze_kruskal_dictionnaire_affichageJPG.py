import time
from random import choice
from itertools import product
import copy
from PIL import Image, ImageDraw


def make_maze(num, name):
    print("Start : %s" % time.ctime())
    w = num
    m = w*w
    vis = []
    vis2 = [m*65//100,m*9//10]
    print(vis2)
    count = 0
    for i in range(0, w):
        liste = []
        while len(liste) > 0:
            liste.pop()
        for i in range(count, count + w):
            liste.append(i)
            count += 1
        vis.append(liste)

    idmatrix = list(product(range(0, w), range(0, w)))
    dictionary = dict(zip(list(range(m)), idmatrix))
    listofwalls = list(product(range(0, w - 1), range(0, w - 1), range(2)))
    for i in range(w - 1):
        listofwalls.append(((w-1), i, 0))
        listofwalls.append((i, (w-1), 1))
    ver = (
        [[".."] + ["#."] * (w - 1) + ["#"]]
        + [["#."] * w + ["#"] for _ in range(w - 2)]
        + [["#."] * (w) + ["."]]
        + [[]]
    )
    hor = (
        [[".#"] + ["##"] * (w - 1) + ["#"]]
        + [["##"] * w + ["#"] for _ in range(w - 1)]
        + [["#"] * (2 * w - 1) + ["#."]]
    )
    print("Matrix created")

    def debugPrint():
        s = ""
        for (a, b) in zip(hor, ver):
            s += "".join(a + ["\n"] + b + ["\n"])
        print(s)

    def cellidchanger2(l, k):
        element1 = dictionary[k]
        element2 = dictionary[l]
        liste = []
        if k < l:
            if type(element1) is list:
                for i in range(len(element1)):
                    z = element1[i]
                    liste.append(z)
            else:
                liste.append(dictionary[k])
            if type(element2) is list:
                for i in range(len(element2)):
                    z = element2[i]
                    x = z[0]
                    y = z[1]
                    vis[x][y] = k
                    liste.append(z)
            else:
                liste.append(dictionary[l])
                z = dictionary[l]
                x = z[0]
                y = z[1]
                vis[x][y] = k
            dictionary[k] = liste
            del dictionary[l]
        else:
            if type(element1) is list:
                for i in range(len(element1)):
                    z = element1[i]
                    x = z[0]
                    y = z[1]
                    vis[x][y] = l
                    liste.append(z)
            else:
                z = dictionary[k]
                x = z[0]
                y = z[1]
                vis[x][y] = l
                liste.append(dictionary[k])
            if type(element2) is list:
                for i in range(len(element2)):
                    z = element2[i]
                    liste.append(z)
            else:
                liste.append(dictionary[l])
            dictionary[l] = liste
            del dictionary[k]
        

    def walk(x, y, vh):
        i = 0
        while i < w**2:
            if len(listofwalls) > 0:
                (x, y, vh) = choice(listofwalls)
                k = vis[y][x]
                if vh == 0:
                    l = vis[y + 1][x]
                else:
                    l = vis[y][x + 1]
                if l == k:
                    try:
                        listofwalls.remove((x, y, vh))
                    except:
                        continue
                elif vh == 0:
                    hor[y + 1][x] = "#."
                    cellidchanger2(l, k)
                    i = i+1
                else:
                    ver[y][x + 1] = ".."
                    cellidchanger2(l, k)
                    i = i+1
                try:
                    listofwalls.remove((x, y, vh))
                except:
                    continue
                # if i in vis2:
                #     wallcleaner()
            else:
                # debugPrint()
                mazeWrite(name)
        else:
            # debugPrint()
            mazeWrite(name)

    def wallcleaner():
        liste = copy.deepcopy(listofwalls)
        # print("1", len(listofwalls))
        for (j, i, vh) in liste:
            k = vis[i][j]
            try:
                l = vis[i][j + 1]
                if k == l:
                    try:
                        listofwalls.remove((j, i, 1))
                        # print(j, i, 1, "erased")
                    except:
                        continue
            except:
                continue
        for (j, i, vh) in liste:
            k = vis[i][j]
            try:
                m = vis[i + 1][j]
                if k == m:
                    try:
                        listofwalls.remove((j, i, 0))
                        # print(j, i, 0, "erased")
                    except:
                        continue
            except:
                continue
        # print("2", len(listofwalls))

    def mazeWrite(name):
        print("End : %s" % time.ctime())
        s = ""
        ths = open(f"{name}.txt", "a")
        for (a, b) in zip(hor, ver):
            s += "".join(a + ["\n"] + b + ["\n"])
        # print(dictionary)
        ths.write(s)
        ths.close()
        createJPG()
        # print(listofwalls)
        # debugPrint()
        # for line in vis:
        #     print(line)
        exit()

    def createJPG():
        large = 3*(w)
        img = Image.new('RGB', (large, large), (255, 255, 255))
        t = large//w
        draw = ImageDraw.Draw(img)
        draw.line((large-1, 0, large-1, large), fill=(0, 0, 0), width=1)
        draw.line((0, large-1, large, large-1), fill=(0, 0, 0), width=1)
        draw.line((0, 0, large, 0), fill=(0, 0, 0), width=1)
        draw.line((0, 0, 0, large), fill=(0, 0, 0), width=1)

        for y in range(w):
            for x in range(w):
                try:
                    if ver[y][x] == "#.":
                        draw.line((t*x, t*y, t*x, t*y+t),
                                  fill=(0, 0, 0), width=1)
                    if hor[y][x] == "##":
                        draw.line((t*x, t*y, t*x+t, t*y),
                                  fill=(0, 0, 0), width=1)
                except:
                    pass
        img.show()
        img.save(f"{name}.jpg")

    (x, y, vh) = choice(listofwalls)
    walk(x, y, vh)


num = int(input("Entrer la taille de maze: "))
name = input("Entrer le nom de maze: ")
make_maze(num, name)