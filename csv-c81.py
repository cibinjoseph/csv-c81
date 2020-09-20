""" Code that converts between CSV and C81 """

import c81utils as c81
import numpy as np
from sys import argv

args = argv

def usage():
    """ Prints usage details """
    print('Usage: python3 csv-c81.py inputfile')

def convert2c81(infile):
    """ Converts CSV file to C81 """
    # Check delimiter
    with open(infile, 'r') as fh:
        line = fh.readline()
    if ',' in line:
        data = np.loadtxt(infile, delimiter=',', dtype='float64')
    else:
        data = np.loadtxt(infile, dtype='float64')

    neg180s = np.where(data[:, 0] == -180)[0]
    pos180s = np.where(data[:, 0] ==  180)[0]

    if len(neg180s) != len(pos180s):
        raise ValueError('No. of -180s and 180s do not match')

    if len(pos180s) == 1:
        machL = data[0, 1:]
        alphaL = data[1:, 0]
        CL = data[1:, 1:]

        alphaD = alphaL
        machD = machL
        CD = CL*0.0

        alphaM = alphaL
        machM = machL
        CM = CL*0.0

    elif len(pos180s) == 2:
        machL = data[neg180s[0]-1, 1:]
        alphaL = data[neg180s[0]:pos180s[0]+1, 0]
        CL = data[neg180s[0]:pos180s[0]+1, neg180s[0]:]

        machD = data[neg180s[1]-1, 1:]
        alphaD = data[neg180s[1]:pos180s[1]+1, 0]
        CD = data[neg180s[1]:pos180s[1]+1, neg180s[1]:]

        alphaM = alphaL
        machM = machL
        CM = CL*0.0

    elif len(pos180s) == 3:
        machL = data[neg180s[0]-1, 1:]
        alphaL = data[neg180s[0]:pos180s[0]+1, 0]
        CL = data[neg180s[0]:pos180s[0]+1, neg180s[0]:]

        machD = data[neg180s[1]-1, 1:]
        alphaD = data[neg180s[1]:pos180s[1]+1, 0]
        CD = data[neg180s[1]:pos180s[1]+1, neg180s[1]:]

        machM = data[neg180s[2]-1, 1:]
        alphaM = data[neg180s[2]:pos180s[2]+1, 0]
        CM = data[neg180s[2]:pos180s[2]+1, neg180s[2]:]

    af = c81.C81(infile[:-4], \
                alphaL, machL, CL, \
                alphaD, machD, CD, \
                alphaM, machM, CM)

    outfile = infile[:-4] + '.C81'
    with open(outfile, 'w') as fh:
        c81.dump(af, fh)

    print(outfile + ' created')

def convert2csv(infile):
    """ Converts C81 file to CSV """
    with open(infile, 'r') as fh:
        af = c81.load(fh)

    # Construct large 2d array for writing out
    alphaL = np.insert(af.CL.alpha, 0, 0.0)
    CLarray = np.insert(af.CL.val, 0, af.CL.mach, axis=0)
    CLarray = np.insert(CLarray, 0, alphaL, axis=1)

    alphaD = np.insert(af.CD.alpha, 0, 0.0)
    CDarray = np.insert(af.CD.val, 0, af.CD.mach, axis=0)
    CDarray = np.insert(CDarray, 0, alphaD, axis=1)

    alphaM = np.insert(af.CM.alpha, 0, 0.0)
    CMarray = np.insert(af.CM.val, 0, af.CM.mach, axis=0)
    CMarray = np.insert(CMarray, 0, alphaM, axis=1)

    outArray = np.block([[CLarray], [CDarray], [CMarray]])

    outfile = infile[:-4] + '.CSV'
    np.savetxt(outfile, outArray, fmt='%9.4f', delimiter=',')
    print(outfile + ' created')


def main():
    # Read input arguments as filenames
    if len(args) == 1:
        usage()
        quit()
    else:
        filenames = args[1:]

    # For each filename convert as necessary
    for infile in filenames:
        if infile[-4:].upper() == '.C81':
            convert2csv(infile)
        if infile[-4:].upper() == '.CSV':
            convert2c81(infile)


if __name__ == "__main__":
    main()
