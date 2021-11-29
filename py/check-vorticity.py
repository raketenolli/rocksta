import numpy
from math import sin, cos, pi, log, atan2, sqrt

def VOR2DS(gamma, x, z, x0, z0):
    rsq = (x-x0)**2 + (z-z0)**2
    u = gamma / (2*pi*rsq) * (z-z0)
    w = -gamma / (2*pi*rsq) * (x-x0)
    return numpy.array([u, w])

def VOR2DC(gamma, x, z, x1, z1, x2, z2): # only works if x and z are in element coordinates!
    r1sq = (x-x1)**2 + (z-z1)**2
    r2sq = (x-x2)**2 + (z-z2)**2
    u = gamma/(2*pi) * (atan2(z-z2, x-x2) - atan2(z-z1, x-x1))
    w = -gamma/(4*pi) * log(r1sq/r2sq)
    return numpy.array([u, w])

#x1 = 0
#x2 = 1
#z1 = 0
#z2 = 0
x1 = 0.9045
x2 = 0.6545
z1 = -0.0139
z2 = -0.0409

#checkpoints = numpy.array([[0.5, 0.000001], [0.25, 0.000001], [0.75, 0.000001], [0.75, 0.5], [0.25, 0.5], [0.0, 1.0], [1.0, 1.0], [0.5, 1.0]])
checkpoints = numpy.array([[0.9522, -0.0076], [0.7795, -0.0274], [0.5, -0.0502], [0.2205, -0.0528], [0.0477, -0.023], [0.0477, 0.023], [0.2205, 0.0528], [0.5, 0.0502], [0.7795, 0.0274], [0.9522, 0.0076]])

normals = numpy.array([[ 0.13136931, -0.9913335 ], [ 0.10738773, -0.99421722], [ 0.06026658, -0.99818232], [-0.05402412, -0.99853963], [-0.43436338, -0.90073773], [-0.43436338,  0.90073773], [-0.05402412,  0.99853963], [ 0.06026658,  0.99818232], [ 0.10738773,  0.99421722], [ 0.13136931,  0.9913335 ]])

numpy.set_printoptions(precision=3, suppress=True)

#for i in [2, 6, 20, 60, 200]:
for i in [200]:
    print("Number of discrete vortices:", i)
    for p, n in zip(checkpoints, normals):
        #vd = numpy.array([0.0, 0.0])
        #for j in range(i):
            #x0 = x1 + ((x2-x1) * j / (i-1))
            #z0 = z1 + ((z2-z1) * j / (i-1))
            #vd = vd + VOR2DS(1.0/i, p[0], p[1], x0, z0)

        # transform p to element coordinates!
        dl = sqrt((x2-x1)**2 + (z2-z1)**2) # element length

        theta = atan2(z2 - z1, x2 - x1)
        dx = p[0] - x1
        dz = p[1] - z1
        xe = dx * cos(theta) + dz * sin(theta)
        ze = -dx * sin(theta) + dz * cos(theta)

        vc = VOR2DC(1.0, xe, ze, 0, 0, dl, 0)

        # transfer induced velocity to global coordinates!
        vcgx = vc[0] * cos(-theta) + vc[1] * sin(-theta)
        vcgz = -vc[0] * sin(-theta) + vc[1] * cos(-theta)

        print("Checkpoint", p, "ind. vel.", [vcgx, vcgz], "ind. vel. normal comp.", vcgx * n[0] + vcgz * n[1])
        #print("Ind. vel. from disc. vort.", vd, "Ind. vel. from const. vort.", vc)
