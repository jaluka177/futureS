from math import *

#d = [-0.81, -0.096, 0.0256, -0.1075, 176.87, 144.22, 29.07, 2.74, 0, 4.74, 5.66, 0.69, 20]
'''
def gepModel(d):

    ROUNDING_THRESHOLD = 0.5

    G1C0 = -5.690949
    G1C1 = -3.150848
    G1C2 = -4.25711
    G1C3 = -5.990784
    G1C4 = 6.049987
    G1C5 = -7.254089
    G1C6 = -2.393585
    G1C7 = 6.991181
    G1C8 = -1.261688
    G1C9 = 1.579712
    G2C0 = -5.690949
    G2C1 = -6.584931
    G2C2 = 3.780091
    G2C3 = -5.990784
    G2C4 = 5.753327
    G2C5 = -7.254089
    G2C6 = -2.393585
    G2C7 = 2.429291
    G2C8 = -1.261688
    G2C9 = 1.579712
    G3C0 = -5.690949
    G3C1 = -6.584931
    G3C2 = -4.25711
    G3C3 = -5.990784
    G3C4 = 5.753327
    G3C5 = -7.254089
    G3C6 = 1.465363
    G3C7 = 2.429291
    G3C8 = -1.261688
    G3C9 = 1.579712
    G4C0 = -5.690949
    G4C1 = -6.584931
    G4C2 = -4.25711
    G4C3 = -5.990784
    G4C4 = 6.049987
    G4C5 = 2.818512
    G4C6 = -2.393585
    G4C7 = 2.429291
    G4C8 = -1.261688
    G4C9 = 1.579712

    varTemp = 0.0

    varTemp = ((d[0]+d[9])*(G1C4*G1C5))
    varTemp = varTemp + (gepGOE2G(gepGOE2E(d[1],(d[0]*d[9])),d[3])*(gepGOE2E(gepGOE2E(d[6],d[12]),d[0])+pow(d[9],3.0)))
    varTemp = varTemp + pow(((d[1]+gepGOE2E((d[9]*d[0]),d[1]))*gepGOE2E(pow(d[0],3.0),d[3])),3.0)
    varTemp = varTemp + (gepAND2(d[12],G4C7)*d[6])

    if (varTemp >= ROUNDING_THRESHOLD):
        return 1
    else:
        return 0


def gepAND2(x, y):
    if ((x >= 0.0) and (y >= 0.0)):
        return 1.0
    else:
        return 0.0

def gepGOE2E(x, y):
    if (x >= y):
        return (x+y)
    else:
        return (x*y)

def gepGOE2G(x, y):
    if (x >= y):
        return (x+y)
    else:
        return atan(x*y)
'''
def gepModel(d):

    ROUNDING_THRESHOLD = 0.5

    G1C0 = 5.40274
    G1C1 = -8.273407
    G1C2 = -6.634216
    G1C3 = 0.580597
    G1C4 = 3.20755
    G1C5 = 3.502502
    G1C6 = 8.254059
    G1C7 = -6.341919
    G1C8 = -6.79068
    G1C9 = 8.377167
    G2C0 = -7.944397
    G2C1 = -8.273407
    G2C2 = -6.634216
    G2C3 = 4.167572
    G2C4 = 3.20755
    G2C5 = -1.766938
    G2C6 = -9.979798
    G2C7 = 0.024902
    G2C8 = -6.79068
    G2C9 = 2.589417
    G3C0 = 5.40274
    G3C1 = -8.273407
    G3C2 = -8.653687
    G3C3 = 9.172424
    G3C4 = 3.20755
    G3C5 = -1.766938
    G3C6 = -7.868348
    G3C7 = -6.341919
    G3C8 = -6.79068
    G3C9 = 0.409637
    G4C0 = 5.40274
    G4C1 = -8.273407
    G4C2 = -6.634216
    G4C3 = 0.580597
    G4C4 = 3.20755
    G4C5 = 3.502502
    G4C6 = 8.254059
    G4C7 = -6.341919
    G4C8 = -6.79068
    G4C9 = 8.377167

    varTemp = 0.0

    varTemp = pow(pow(d[5],3.0),3.0)
    varTemp = varTemp + (d[11]+pow(d[8],3.0))
    varTemp = varTemp + (pow(gepLT2E(d[0],d[8]),3.0)+pow(gepLT2E(d[12],G3C6),3.0))
    varTemp = varTemp + (pow((d[0]*d[8]),3.0)+pow(gepLT2E(d[12],G4C5),3.0))

    if (varTemp >= ROUNDING_THRESHOLD):
        return 1
    else:
        return 0


def gepLT2E(x, y):
    if (x < y):
        return (x+y)
    else:
        return (x*y)
#print(gepModel(d))