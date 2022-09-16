module load python intel texlive cray-fftw
export CC=gcc
export LD_LIBRARY_PATH=$FFTW_ROOT/lib:$LD_LIBRARY_PATH
export LIBSHARP=/global/cscratch1/sd/xzackli/act/software/libsharp/auto
export LIBRARY_PATH=$FFTW_ROOT/lib:$LIBRARY_PATH
export CPATH=$LIBSHARP/../libsharp/:$FFTW_ROOT/include/:$CPATH
export CFLAGS="-I /global/cscratch1/sd/xzackli/act/software/libsharp/libsharp/ $CLFAGS"
export LD_LIBRARY_PATH=$LIBSHARP/auto/lib:$LD_LIBRARY_PATH

source activate /global/cscratch1/sd/xzackli/act/pyenv/mnms
export PYTHONPATH=$(pwd)/python/:/global/cscratch1/sd/xzackli/act/software/:$PYTHONPATH
export HDF5_USE_FILE_LOCKING=FALSE
export OMP_NUM_THREADS=4


srun -n 8 -c 4 --cpu_bind=cores -u python -u qprun_npipe.py windows/window_dr6_pa4_f150.fits out/dr6_pa4_f150
srun -n 8 -c 4 --cpu_bind=cores -u python -u qprun_npipe.py windows/window_dr6_pa4_f220.fits out/dr6_pa4_f220

srun -n 8 -c 4 --cpu_bind=cores -u python -u qprun_npipe.py windows/window_dr6_pa5_f090.fits out/dr6_pa5_f090
srun -n 8 -c 4 --cpu_bind=cores -u python -u qprun_npipe.py windows/window_dr6_pa5_f150.fits out/dr6_pa5_f150

srun -n 8 -c 4 --cpu_bind=cores -u python -u qprun_npipe.py windows/window_dr6_pa6_f090.fits out/dr6_pa6_f090
srun -n 8 -c 4 --cpu_bind=cores -u python -u qprun_npipe.py windows/window_dr6_pa6_f150.fits out/dr6_pa6_f150

srun -n 8 -c 4 --cpu_bind=cores -u python -u qp2fits_npipe.py out/QP_dr6_pa4_f150/
srun -n 8 -c 4 --cpu_bind=cores -u python -u qp2fits_npipe.py out/QP_dr6_pa4_f220/

srun -n 8 -c 4 --cpu_bind=cores -u python -u qp2fits_npipe.py out/QP_dr6_pa5_f090/
srun -n 8 -c 4 --cpu_bind=cores -u python -u qp2fits_npipe.py out/QP_dr6_pa5_f150/

srun -n 8 -c 4 --cpu_bind=cores -u python -u qp2fits_npipe.py out/QP_dr6_pa6_f090/
srun -n 8 -c 4 --cpu_bind=cores -u python -u qp2fits_npipe.py out/QP_dr6_pa6_f150/

srun -n 8 -c 4 --cpu_bind=cores -u python -u qp2fits_npipe.py out/QP_fullsky/
