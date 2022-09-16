
export windir=/global/cscratch1/sd/xzackli/PSpipe/project/data_analysis/windows/
srun -n 32 -c 1 -u python -u make_act_maps.py $windir/window_dr6_pa4_f150.fits windows
srun -n 32 -c 1 -u python -u make_act_maps.py $windir/window_dr6_pa4_f220.fits windows

srun -n 32 -c 1 -u python -u make_act_maps.py $windir/window_dr6_pa5_f090.fits windows
srun -n 32 -c 1 -u python -u make_act_maps.py $windir/window_dr6_pa5_f150.fits windows

srun -n 32 -c 1 -u python -u make_act_maps.py $windir/window_dr6_pa6_f090.fits windows
srun -n 32 -c 1 -u python -u make_act_maps.py $windir/window_dr6_pa6_f150.fits windows
