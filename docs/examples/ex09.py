from skfem import *
from skfem.models.poisson import *
import numpy as np

p = np.linspace(0, 1, 16)
m = MeshTet.init_tensor(p, p, p)

e = ElementTetP1()
map = MappingAffine(m)
basis = InteriorBasis(m, e, map)

A = asm(laplace, basis)
b = asm(unit_load, basis)

I = m.interior_nodes()

x = 0*b

if __name__ == "__main__":
    verbose = True
else:
    verbose = False
# run conjugate gradient with the default preconditioner
x[I] = solve(*condense(A, b, I=I), solver=solver_iter_pcg(verbose=verbose))

# run conjugate gradient with the incomplete LU preconditioner
Aint, bint = condense(A, b, I=I)
x[I] = solve(Aint, bint, solver=solver_iter_pcg(pc=build_pc_ilu(Aint), verbose=verbose))

if verbose:
    m.save("ex09.vtk", x)
