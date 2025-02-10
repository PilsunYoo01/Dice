import os
import sys
import time

from pyscf import ao2mo, tools
import numpy as np
from dice_func import solve_dice

from qiskit_addon_sqd.counts import generate_counts_uniform, counts_to_arrays
from qiskit_addon_sqd.configuration_recovery import recover_configurations
from qiskit_addon_sqd.fermion import solve_fermion
from qiskit_addon_sqd.subsampling import postselect_and_subsample
from qiskit_addon_sqd.fermion import (
    bitstring_matrix_to_ci_strs,
    flip_orbital_occupancies,
    _check_ci_strs,
)

def seperated_bitstring_sym(bitstrings):
    converted_list = []
    for bitstring in bitstrings:
        bitstring2array = [bit for bit in bitstring]
        alpha_bits = list([bitstring2array[idx] for idx in range(0,len(bitstring2array),2)])
        beta_bits = list([bitstring2array[idx] for idx in range(1,len(bitstring2array),2)])
        converted_list.append("".join(alpha_bits+beta_bits))
        if "".join(beta_bits+alpha_bits) not in converted_list:
            converted_list.append("".join(beta_bits+alpha_bits))
       
    return converted_list

def seperated_bitstring(bitstrings):
    converted_list = []
    for bitstring in bitstrings:
        bitstring2array = [bit for bit in bitstring]
        alpha_bits = list(reversed([bitstring2array[idx] for idx in range(0,len(bitstring2array),2)]))
        beta_bits = list(reversed([bitstring2array[idx] for idx in range(1,len(bitstring2array),2)]))
        converted_list.append("".join(alpha_bits+beta_bits))
    return converted_list


def decimal_strings(bitstrings):
    converted_alpha_list = []
    converted_beta_list = []
    for bitstring in bitstrings:
        bitstring2array = [bit for bit in bitstring]
        alpha_bits = list(reversed([bitstring2array[idx] for idx in range(0,len(bitstring2array)//2)]))
        beta_bits = list(reversed([bitstring2array[idx] for idx in range(len(bitstring2array)//2,len(bitstring2array))]))
        converted_alpha_list.append(int("".join(alpha_bits),2))
        converted_beta_list.append(int("".join(beta_bits),2))
    return np.array(converted_alpha_list), np.array(converted_beta_list)



# Specify molecule properties
open_shell = False
spin_sq = 0
Dice = True
ncores = "14"
max_davidson_cycles = 200


# Read in molecule from disk
#active_space_path = os.path.join(
#    os.path.abspath(os.path.dirname(__file__)), "molecules", "n2_fci.txt"
#)
active_space_path = os.path.abspath('rhf_n2.FCIDUMP')

print( active_space_path )

mf_as = tools.fcidump.to_scf(active_space_path)
num_orbitals = mf_as.mol.nao
num_elec_a = num_elec_b = mf_as.mol.nelectron // 2

hcore = mf_as.get_hcore()
eri = ao2mo.restore(1, mf_as._eri, num_orbitals)
nuclear_repulsion_energy = mf_as.mol.energy_nuc()


# Read hivqe sampled states
with open('hivqe_run.json','r') as f:
    lines = f.readlines()

rand_seed = 42
start_time = 0

i = -1
json_data = lines[i]
json = eval(json_data)

current_basis_states = json["current_basis_states"]
iteration_res_basis_states = json["iteration_res_basis_states"]

for new_states in iteration_res_basis_states:
	if new_states not in current_basis_states:
		current_basis_states.append(new_states)

sym_current_basis_states = seperated_bitstring_sym(current_basis_states)
ci_strs = decimal_strings(sym_current_basis_states)
print(len(ci_strs[0]))

energy_sci, wf_mags, avg_occs = solve_dice(
	ci_strs,
	active_space_path,
	os.path.abspath('.'),
	spin_sq=spin_sq,
	max_davidson=max_davidson_cycles,
	clean_working_dir=False,
	mpirun_options=["-n", ncores],
)

print(energy_sci + nuclear_repulsion_energy)
mf_as.kernel()
print(mf_as.e_tot)

