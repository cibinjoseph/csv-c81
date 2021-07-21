""" Code that converts between CSV and C81 """

import c81utils as c81
import numpy as np
from sys import argv
import matplotlib.pyplot as plt
from io import StringIO

args = argv

def usage():
    """ Prints usage details """
    print('Usage: python3 csv-c81.py inputfile')
    print(' Add -p flag for plotting C81 file')

def getTables(infile):
    """ Extracts tables in file separately"""
    with open(infile, 'r') as fh:
        lines = fh.readlines()

    idx = []
    for i, line in enumerate(lines):
        if len(line.split()) == 0:
            idx.append(i)

    if len(idx) == 0:
        # Only 1 table
        tbl_CL = lines
        tbl_CD = None
        tbl_CM = None
    elif len(idx) == 1:
        # 2 tables
        tbl_CL = lines[0 : idx[0]]
        tbl_CD = lines[idx[0]+1 : ]
        tbl_CM = None
    else:
        # 3 tables or more
        tbl_CL = lines[0 : idx[0]]
        tbl_CD = lines[idx[0]+1 : idx[1]]
        tbl_CM = lines[idx[1]+1 : ]

    return tbl_CL, tbl_CD, tbl_CM

def convert2c81(infile):
    """ Converts 3 CSV tables to C81 data """
    tbl_CL, tbl_CD, tbl_CM = getTables(infile)

    # Check whether delimiter is comma or space
    delim = ' '
    for line in tbl_CL:
        if ',' in line:
            delim = ','
            break

    arr_CL = np.loadtxt(tbl_CL, delimiter=delim, dtype='float64', comments='#')
    if tbl_CD:
        arr_CD = np.loadtxt(tbl_CD, delimiter=delim, \
                            dtype='float64', comments='#')
    else:
        arr_CD = 0*arr_CL

    if tbl_CM:
        arr_CM = np.loadtxt(tbl_CM, delimiter=delim, \
                            dtype='float64', comments='#')
    else:
        arr_CM = 0*arr_CL


    # CL
    machL = arr_CL[0, 1:]
    alphaL = arr_CL[1:, 0]
    CL = arr_CL[1:, 1:]

    # CD
    machD = arr_CD[0, 1:]
    alphaD = arr_CD[1:, 0]
    CD = arr_CD[1:, 1:]

    # CM
    machM = arr_CM[0, 1:]
    alphaM = arr_CM[1:, 0]
    CM = arr_CM[1:, 1:]

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

def plotC81(infile):
    """ Plot airfoil tables from C81 file """
    with open(infile, 'r') as fh:
        af = c81.load(fh)

    fig1, ax1 = plt.subplots(1)
    fig2, ax2 = plt.subplots(1)
    fig3, ax3 = plt.subplots(1)

    for i in range(len(af.CL.mach)):
        ax1.plot(af.CL.alpha, af.CL.val[:, i], \
                  label='M ' + str(af.CL.mach[i]))
    for i in range(len(af.CD.mach)):
        ax2.plot(af.CD.alpha, af.CD.val[:, i], \
                  label='M ' + str(af.CD.mach[i]))
    for i in range(len(af.CM.mach)):
        ax3.plot(af.CM.alpha, af.CM.val[:, i], \
                  label='M ' + str(af.CM.mach[i]))

    ax1.set_xlabel('alpha')
    ax1.set_title('CL')
    ax1.legend()

    ax2.set_xlabel('alpha')
    ax2.set_title('CD')
    ax2.legend()

    ax3.set_xlabel('alpha')
    ax3.set_title('CM')
    ax3.legend()

    plt.tight_layout()
    plt.show()


def main():
    # Read input arguments as filenames
    if len(args) == 1:
        usage()
        quit()
    else:
        filenames = args[1:]

    # Check if plotting is requested for single file
    if filenames[0] == '-p' and len(filenames) == 2:
        infile = filenames[1]
        if infile[-4:].upper() != '.C81':
            raise TypeError('Only .C81 files can be plotted. \
                            Convert and try again.')
        else:
            # Plot the contents of the file
            plotC81(infile)

    else:
        # For each filename convert as necessary
        for infile in filenames:
            if infile != '-p':
                if infile[-4:].upper() == '.C81':
                    convert2csv(infile)
                if infile[-4:].upper() == '.CSV':
                    convert2c81(infile)


if __name__ == "__main__":
    main()
