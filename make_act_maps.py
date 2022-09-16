# This program converts planck maps to car, outputting:
#  map:  interpolated using harmonic interpolation
#  ivar: the inverse variance in T,Q,U of each pixel using nearest neighbor. All correlations ignored.
#  map0: like map, but using nearest neighbor. Optional
# I didn't expect this to become so involved, though much of the verbosity is status printing.
# It goes to some length to avoid wasting memory.

from __future__ import division, print_function
import argparse, os, sys, time
parser = argparse.ArgumentParser()
parser.add_argument("ifiles", nargs="+")
parser.add_argument("odir")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-n", "--nside",   type=int, default=2048)
parser.add_argument(      "--scalar",  action="store_true")
args = parser.parse_args()
import numpy as np, healpy
from enlib import enmap, utils, curvedsky, coordinates, mpi, memory

unit  = 1
euler = np.array([57.06793215,  62.87115487, -167.14056929])*utils.degree
dtype = np.float32
nside = args.nside
npix  = 12*nside**2
rstep = 100
verbose = args.verbose
utils.mkdir(args.odir)
t0 = time.time()

def progress(msg):
    if verbose:
        print("%6.2f %6.2f %6.2f %s" % ((time.time()-t0)/60, memory.current()/1024.**3, memory.max()/1024.**3, msg))

comm = mpi.COMM_WORLD

shape, wcs = enmap.read_map_geometry(args.ifiles[0])
shape = shape[-2:]

progress("Computing pixel position map")
dec, ra = enmap.posaxes(shape, wcs)
pix  = np.zeros(shape, np.int32)
psi  = np.zeros(shape, dtype)
progress("Computing rotation")
nblock = (shape[-2]+rstep-1)//rstep
for bi in range(comm.rank, nblock, comm.size):
    if bi % comm.size != comm.rank: continue
    i = bi*rstep
    rdec = dec[i:i+rstep]
    ipos = np.zeros((2,len(rdec),len(ra)))
    ipos[0] = rdec[:,None]
    ipos[1] = ra  [None,:]
    # This is unreasonably slow
    opos = coordinates.transform("equ", "gal", ipos[::-1], pol=True)
    pix[i:i+rstep,:] = healpy.ang2pix(nside, np.pi/2-opos[1], opos[0])
    psi[i:i+rstep,:] = opos[2]
    del ipos, opos
for i in range(0, shape[-2], rstep):
    pix[i:i+rstep] = utils.allreduce(pix[i:i+rstep], comm)
    psi[i:i+rstep] = utils.allreduce(psi[i:i+rstep], comm)
for ifile in args.ifiles[comm.rank::comm.size]:
    name = os.path.basename(ifile)
    progress("%s read" % name)

    imap = enmap.zeros((3,) + shape, wcs=wcs)
    _m  = enmap.read_map(ifile)
    imap[0] = _m
    imap[1] = _m
    imap[2] = _m
    
    if not args.scalar:
        progress("%s polrot" % name)
        # Apply polarization rotation
        for i in range(0, shape[-2], rstep):
            imap[1:3,i:i+rstep,:] = enmap.rotate_pol(imap[1:3,i:i+rstep,:], psi[i:i+rstep,:])
    # And accumulate into output map
    progress("%s bin" % name)
    omap  = np.zeros((imap.shape[0],12*nside**2),dtype)
    hits  = np.bincount(pix.reshape(-1), minlength=npix)
    for i in range(len(omap)):
        rhs = np.bincount(pix.reshape(-1), imap[i].reshape(-1), minlength=npix)
        rhs[hits>0] /= hits[hits>0]
        omap[i] = rhs
    del hits, rhs
    omap /= unit
    ofile = args.odir + "/" + os.path.basename(ifile)
    progress("%s write" % name)
    healpy.write_map(ofile, omap, overwrite=True)
    del omap, imap
