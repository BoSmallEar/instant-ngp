env2lmod
module load gcc/8.2.0 python_gpu/3.9.9 cuda/11.3.1 eth_proxy glfw/3.3.4 glew/2.1.0
tar -xf $HOME/temp_data/scene0000_00.tar  -C $TMPDIR
cp transforms_t*.json $TMPDIR/scene0000_00/
