from pixlib import *
def build():
    g = blank()
    B = (21, 43); T = (55, 9)          # blade runs base -> tip, up and right
    ux, uy = 0.7071, -0.7071           # along the blade
    px, py = 0.7071,  0.7071           # across it
    # grip, below the guard, then the pommel on the end of it
    gx, gy = B[0] - ux*12, B[1] - uy*12
    haft(g, B[0]-ux*2, B[1]-uy*2, gx, gy, 5)
    wrap(g, B[0]-ux*2, B[1]-uy*2, gx, gy, 5, 4)
    disc(g, B[0]-ux*15.5, B[1]-uy*15.5, 3.4, 'C')
    put(g, B[0]-ux*16.4, B[1]-uy*16.4-1, 'W')
    # blade
    blade(g, B[0], B[1], T[0], T[1], 9, 2.0, 7)
    fuller(g, B[0], B[1], T[0], T[1])
    # crossguard over the blade root, with a brass knuckle at each end
    taper(g, B[0]-px*8, B[1]-py*8, B[0]+px*8, B[1]+py*8, 4.2, 4.2, 'C')
    stud(g, B[0]-px*8.4, B[1]-py*8.4, 2.1)
    stud(g, B[0]+px*8.4, B[1]+py*8.4, 2.1)
    line_on(g, B[0]-px*8, B[1]-py*8-1, B[0]+px*8, B[1]+py*8-1, 'c', 'C')
    return dump(outline(g))
if __name__ == '__main__':
    show(build())
