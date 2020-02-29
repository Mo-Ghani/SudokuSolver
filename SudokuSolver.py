import os
from PIL import Image, ImageDraw, ImageFont
import itertools
import copy

for img in os.listdir("sudoku"):
    os.remove("sudoku/" + img)
f = open("p096_sudoku.txt", "r").read().splitlines()
grids = []

for i in range(50):
    grids.append(list([int(k) for k in f[i * 10 + j]] for j in range(1, 10)))

totsum = 0
loopnum = 1

completeFam = {1, 2, 3, 4, 5, 6, 7, 8, 9}

for grid in grids:

    framenum = 0
    def drawgrid(gridx, frame):

        global x_start, y_start, step_size, loop, image, draw

        # Draws an empty grid template
        height = 595
        width = 595
        image = Image.new(mode='RGB', size=(height, width), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        y_start = 0
        y_end = image.height
        step_size = int(image.width / 9)

        for x in range(0, image.width, step_size):
            if (x / step_size) % 3 == 0 or x == (image.width - step_size):
                line = ((x, y_start), (x, y_end))
                draw.line(line, fill=0, width=3)
            else:
                line = ((x, y_start), (x, y_end))
                draw.line(line, fill=0)

        x_start = 0
        x_end = image.width

        for y in range(0, image.height, step_size):
            if (y / step_size) % 3 == 0 or y == (image.width - step_size):
                line = ((x_start, y), (x_end, y))
                draw.line(line, fill=0, width=3)
            else:
                line = ((x_start, y), (x_end, y))
                draw.line(line, fill=0)

        # Fills empty grid with known info
        font = ImageFont.truetype("calibril.ttf", 80)
        for i in range(9):
            for j in range(9):
                x = x_start + i * step_size + 14
                y = y_start + j * step_size
                if gridx[j][i] != 0:
                    draw.text(xy=(x, y), text=str(gridx[j][i]), font=font, fill=0)

        if loopnum < 10:
            loop = "0" + str(loopnum)
        else:
            loop = str(loopnum)
        if frame < 10:
            image.save("sudoku/" + loop + "0000" + str(frame) + ".PNG")
        elif frame < 100:
            image.save("sudoku/" + loop + "000" + str(frame) + ".PNG")
        elif frame < 1000:
            image.save("sudoku/" + loop + "00" + str(frame) + ".PNG")
        elif frame < 10000:
            image.save("sudoku/" + loop + "0" + str(frame) + ".PNG")
        else:
            image.save("sudoku/" + loop + str(frame) + ".PNG")

    drawgrid(grid, framenum)
    framenum += 1

    change = []
    for i, j in itertools.product(range(9), range(9)):
        if grid[i][j] == 0:
            change.append((i, j))
    allnope = {}


    def nopefinder(coords):
        nopefunc = set([])
        ifunc = coords[0]
        jfunc = coords[1]
        # Creates list of forbidden values
        for xfunc in grid[ifunc]:
            if xfunc != 0:
                nopefunc.add(xfunc)
        for kfunc in range(9):
            yfunc = grid[kfunc][jfunc]
            if yfunc != 0:
                nopefunc.add(yfunc)
        mfunc = (ifunc // 3) * 3
        nfunc = (jfunc // 3) * 3
        for xfunc in range(3):
            for yfunc in range(3):
                kfunc = grid[mfunc + xfunc][nfunc + yfunc]
                if kfunc != 0:
                    nopefunc.add(kfunc)
        return nopefunc


    def candidatefinder(coords):
        if coords in allnope:
            nopefunc = allnope[coords]
        else:
            nopefunc = nopefinder(coords)
        candidatesfunc = completeFam - nopefunc
        return candidatesfunc


    def solve(gridfunc, changefunc):

        global framenum
        global altchangenum
        for coord in changefunc:

            changenum = 0
            i = coord[0]
            j = coord[1]
            m = (i // 3) * 3
            n = (j // 3) * 3

            subgridchange = []
            for x in range(3):
                for y in range(3):
                    k = gridfunc[m + x][n + y]
                    if k == 0:
                        if (x + m, y + n) != (i, j):
                            subgridchange.append((x, y))
            rowchange = []
            for x in range(9):
                if gridfunc[i][x] == 0 and x != j:
                    rowchange.append((i, x))
            columnchange = []
            for y in range(9):
                if gridfunc[y][j] == 0 and y != i:
                    columnchange.append((y, j))

            if coord in allnope:
                nope = nopefinder(coord) | allnope[coord]
            else:
                nope = nopefinder(coord)

            if len(nope) == 8:
                solved = completeFam - nope
                (gridfunc[i][j],) = solved
                changefunc.remove(coord)
                changenum = 1
                altchangenum = 1

            # Attempt to deduce value based on other empty squares in sector
            if changenum == 0:
                othernope = []
                for t in subgridchange:
                    othernope.append(nopefinder((t[0] + m, t[1] + n)))
                if len(othernope) >= 1:
                    remain = set.intersection(*othernope)
                    for rem in remain:
                        if rem not in nope and changenum == 0:
                            gridfunc[i][j] = rem
                            changefunc.remove(coord)
                            changenum = 1
                            altchangenum = 1
            if changenum == 0:
                othernope = []
                for t in rowchange:
                    othernope.append(nopefinder(t))
                if len(othernope) >= 1:
                    remain = set.intersection(*othernope)
                    for rem in remain:
                        if rem not in nope and changenum == 0:
                            gridfunc[i][j] = rem
                            changefunc.remove(coord)
                            changenum = 1
                            altchangenum = 1
            if changenum == 0:
                othernope = []
                for t in columnchange:
                    othernope.append(nopefinder(t))
                if len(othernope) >= 1:
                    remain = set.intersection(*othernope)
                    for rem in remain:
                        if rem not in nope and changenum == 0:
                            gridfunc[i][j] = rem
                            changefunc.remove(coord)
                            changenum = 1
                            altchangenum = 1
            allnope[coord] = nope
            if coord not in change:
                del allnope[coord]

            # Plots and saves grid with changes
            font = ImageFont.truetype("calibril.ttf", 80)
            for i in range(9):
                for j in range(9):
                    x = x_start + i * step_size + 14
                    y = y_start + j * step_size
                    if grid[j][i] != 0:
                        draw.text(xy=(x, y), text=str(grid[j][i]), font=font, fill=0)
            if framenum < 10:
                image.save("sudoku/" + loop + "0000" + str(framenum) + ".PNG")
            elif framenum < 100:
                image.save("sudoku/" + loop + "000" + str(framenum) + ".PNG")
            elif framenum < 1000:
                image.save("sudoku/" + loop + "00" + str(framenum) + ".PNG")
            elif framenum < 10000:
                image.save("sudoku/" + loop + "0" + str(framenum) + ".PNG")
            else:
                image.save("sudoku/" + loop + str(framenum) + ".PNG")
            framenum += 1

        # Block and column/row interactions
        if altchangenum == 0:
            for num in range(1, 10):
                for m in range(3):
                    m *= 3
                    for n in range(3):
                        n *= 3
                        if all(num != gridfunc[o + m][p + n] for o, p in itertools.product(range(3), range(3))) \
                                is True and any(gridfunc[o + m][p + n] == 0 for o, p in
                                                itertools.product(range(3), range(3))) is True:
                            candidates = []
                            coordins = []
                            for o, p in itertools.product(range(3), range(3)):
                                cellblock = gridfunc[o + m][p + n]
                                if cellblock == 0:
                                    candidates.append(candidatefinder((o + m, p + n)))
                                    coordins.append((o + m, p + n))
                            interactions = {}
                            for scan in range(1, 10):
                                elem = []
                                for k in range(len(candidates)):
                                    if scan in candidates[k]:
                                        elem.append(k)
                                if len(elem) > 1:
                                    interactions[scan] = elem
                            for scan in interactions:
                                possindex = interactions[scan]
                                posscells = []
                                for index in possindex:
                                    posscells.append(coordins[index])
                                if all(posscells[u][1] == posscells[0][1] for u in range(len(posscells))) is True:
                                    colnum = posscells[0][1]
                                    for f in range(9):
                                        if gridfunc[f][colnum] == 0:
                                            if (f, colnum) in allnope and all(f != o + m for o in range(3)) is True:
                                                oldnope = allnope[(f, colnum)]
                                                if scan not in oldnope:
                                                    oldnope.add(scan)
                                                    altchangenum = 1
                                                allnope[(f, colnum)] = oldnope
                                if all(posscells[u][0] == posscells[0][0] for u in range(len(posscells))) is True:
                                    rownum = posscells[0][0]
                                    for f in range(9):
                                        if gridfunc[rownum][f] == 0:
                                            if (rownum, f) in allnope and all(f != p + n for p in range(3)) is True:
                                                oldnope = allnope[(rownum, f)]
                                                if scan not in oldnope:
                                                    oldnope.add(scan)
                                                    altchangenum = 1
                                                allnope[(rownum, f)] = oldnope


    while len(change) > 0:
        altchangenum = 0
        solve(grid, change)
        if altchangenum == 0:
            break

    backupgrid = {}
    backupallnope = {}
    backupchange = {}
    backup = 0
    # guess and test
    while len(change) > 0:
        backupgrid[backup] = copy.deepcopy(grid)
        backupallnope[backup] = copy.deepcopy(allnope)
        backupchange[backup] = copy.deepcopy(change)

        guesscell = max(allnope, key=lambda co: len(allnope[co]))
        (i, j) = guesscell
        candidates = completeFam - allnope[guesscell]
        guessnum = 1
        for guess in candidates:
            grid[i][j] = guess
            change.remove(guesscell)
            del allnope[guesscell]
            solve(grid, change)
            while altchangenum != 0:
                altchangenum = 0
                solve(grid, change)
            if len(change) > 0:
                newmax = max(allnope, key=lambda co: len(allnope[co]))
                if len(allnope[newmax]) == 9:
                    if len(candidates) == guessnum:
                        backup -= 1
                    guessnum += 1
                    grid = copy.deepcopy(backupgrid[backup])
                    allnope = copy.deepcopy(backupallnope[backup])
                    change = copy.deepcopy(backupchange[backup])
                    drawgrid(grid, framenum)
                    allnope[guesscell].add(guess)
                    framenum += 1
                    continue
                else:
                    backup += 1
                    break
            else:
                backup += 1
                break

    add = str(grid[0][0]) + str(grid[0][1]) + str(grid[0][2])
    totsum += int(add)
    print(str(loopnum) + "/50")
    loopnum += 1

print(totsum)
