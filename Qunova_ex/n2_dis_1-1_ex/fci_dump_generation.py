import numpy as np
import pyscf
from pyscf import cc, mcscf, mp, scf
from itertools import combinations
#from mpi4py import MPI  # Import MPI for parallel processing
import os,sys,subprocess
from pyscf.tools import fcidump

geometry = f'N 0.00000 0.00000 0.00000; N 0.00000 0.00000 1.100'
basis = "cc-pVDZ"
active_orbitals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
frozen_orbitals = []

mol = pyscf.gto.M(atom=geometry,
                  basis=basis,
                  )
mol.verbose = 4
checkfile='n2_1-1.chk'

if not os.path.exists(checkfile):
    mf = scf.RHF(mol)
    mf.chkfile =checkfile
    mf.kernel()
    mo_occ = mf.mo_occ
    mo_coeff = mf.mo_coeff

else:
    mf = scf.RHF(mol)
    mf.chkfile = checkfile
    mf.init_guess = 'chk'
    mf.kernel()
    mo_occ = mf.mo_occ
    mo_coeff = mf.mo_coeff

mo_idx = [idx for idx,mo in enumerate(mo_occ)]

ncas, nelecas = 20,14
#active_orbitals = np.arange(101,113)
mc = mcscf.CASCI(mf,ncas,nelecas)
orbs = mcscf.addons.sort_mo(mc, mo_coeff, active_orbitals, base=0)
h1, energy_core = mc.get_h1eff(orbs)
#fcidump.from_integrals("rhf.FCIDUMP", h1, mc.get_h2eff(), mc.ncas, mc.nelecas, energy_core)

fcidump.from_scf(mf, 'rhf_full.FCIDUMP')
