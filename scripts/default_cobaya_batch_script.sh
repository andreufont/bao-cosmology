#!/bin/bash
#SBATCH -N {NUMNODES}
#SBATCH -q {QUEUE}
#SBATCH -J {JOBNAME}
#SBATCH -C cpu
#SBATCH -t {WALLTIME}

#OpenMP settings:
export OMP_NUM_THREADS={OMP}
export OMP_PLACES=threads
export OMP_PROC_BIND=spread
export COBAYA_USE_FILE_LOCKING=False

###set things to be used by the python script, which extracts text from here with ##XX: ... ##
### command to use for each run in the batch
##RUN: time srun -n {NUMMPI} -c {OMP} --cpu_bind=cores {PROGRAM} {INI} > {JOBSCRIPTDIR}/{INIBASE}.log 2>&1 ##
### defaults for this script
##DEFAULT_qsub: sbatch ##
##DEFAULT_qdel: scancel ##
##DEFAULT_cores_per_node: 256 ##
##DEFAULT_chains_per_node: 4 ##
##DEFAULT_program: cobaya-run -r ##
##DEFAULT_walltime: 00:30:00##
##DEFAULT_queue: regular##

cd {ROOTDIR}

source /global/common/software/desi/users/adematti/cosmodesi_environment.sh main

{COMMAND}

wait
