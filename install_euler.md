# Installing `instant-ngp` on Euler

## Install `cmake3.22`

```
wget https://cmake.org/files/v3.22/cmake-3.22.3-linux-x86_64.tar.gz
tar -xvf cmake-3.22.3-linux-x86_64.tar.gz
```

## Install NGP

```
env2lmod
module load gcc/8.2.0 python_gpu/3.8.5
module load glew/2.1.0
bsub -R "rusage[ngpus_excl_p=1]" -R "select[gpu_model0==NVIDIAGeForceRTX2080Ti]" -n 20 -W 30 -Ip "bash"
```

Once the interactive job starts, compile NGP:

```
cd instant-ngp
~/cmake-3.22.3-linux-x86_64/bin/cmake .. -DCUDA_NVCC_FLAGS="-ccbin=/cluster/spack/apps/linux-centos7-x86_64/gcc-4.8.5/gcc-8.2.0-6xqov2fhvbmehix42slain67vprec3fs/bin/gcc"
cd build
make -j20
```

The last step (linking) because for some reason `ld` sees the `lib` folders of `gcc4.8.2`.  Running the following command manually should create the missing executable:

```
/cluster/spack/apps/linux-centos7-x86_64/gcc-4.8.5/gcc-8.2.0-6xqov2fhvbmehix42slain67vprec3fs/bin/g++  -fPIC -fopenmp -O3 -DNDEBUG CMakeFiles/testbed.dir/src/main.cu.o -o testbed   -L/cluster/apps/gcc-8.2.0/cuda-11.1.1-s26pftjpbyymk4xg3ndh2tkyvyroe2jq/targets/x86_64-linux/lib/stubs   -L/cluster/spack/apps/linux-centos7-x86_64/gcc-4.8.5/gcc-8.2.0-6xqov2fhvbmehix42slain67vprec3fs/lib64  -L/cluster/spack/apps/linux-centos7-x86_64/gcc-4.8.5/gcc-8.2.0-6xqov2fhvbmehix42slain67vprec3fs/lib  dependencies/glfw/src/CMakeFiles/glfw_objects.dir/context.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/init.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/input.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/monitor.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/vulkan.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/window.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/x11_init.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/x11_monitor.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/x11_window.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/xkb_unicode.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/posix_time.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/posix_thread.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/glx_context.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/egl_context.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/osmesa_context.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/linux_joystick.c.o libngp.a -lGL dependencies/tiny-cuda-nn/src/libtiny-cuda-nn.a -lcuda -lcublas -lcudadevrt -lcudart_static -lrt -lpthread -ldl -lGLEW
```


```
/cluster/spack/apps/linux-centos7-x86_64/gcc-4.8.5/gcc-8.2.0-6xqov2fhvbmehix42slain67vprec3fs/bin/g++ -fPIC  -fPIC -fopenmp -O3 -DNDEBUG -shared -Wl,-soname
,pyngp.cpython-39-x86_64-linux-gnu.so -o pyngp.cpython-39-x86_64-linux-gnu.so CMakeFiles/pyngp.dir/src/python_api.cu.o   -L/cluster/apps/gcc-8.2.0/cuda-11.3
.1-o54iuxgz6jm4csvkstuj5hjg4tvd44h3/targets/x86_64-linux/lib/stubs  dependencies/glfw/src/CMakeFiles/glfw_objects.dir/context.c.o dependencies/glfw/src/CMak
eFiles/glfw_objects.dir/init.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/input.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/monitor.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/vulkan.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/window.c.o dependencies/glfw/src/CMakeFiles/g$fw_objects.dir/x11_init.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/x11_monitor.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/x11_window.$.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/xkb_unicode.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/posix_time.c.o dependencies/glfw/src$CMakeFiles/glfw_objects.dir/posix_thread.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/glx_context.c.o dependencies/glfw/src/CMakeFiles/glfw_object$.dir/egl_context.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/osmesa_context.c.o dependencies/glfw/src/CMakeFiles/glfw_objects.dir/linux_joystick.$.o libngp.a -lGL dependencies/tiny-cuda-nn/src/libtiny-cuda-nn.a -lcuda -lcublas -lcudadevrt -lcudart_static -lrt -lpthread -ldl -lGLEW
```

When in doubt / if the command does not work:

1. Run `make -j20 VERBOSE=1` and catch the `g++` call that fails (similar to the one above)
2. Edit the command by removing the flags that contain `gcc4.8.2`, i.e., `-L/cluster/apps/gcc/4.8.2/lib/gcc/x86_64-unknown-linux-gnu/4.8.2  -L/cluster/apps/gcc/4.8.2/lib64  -L/cluster/apps/gcc/4.8.2/lib`
3. Replace them with the corresponding library folders of `gcc8.2.0`, i.e., ` -L/cluster/spack/apps/linux-centos7-x86_64/gcc-4.8.5/gcc-8.2.0-6xqov2fhvbmehix42slain67vprec3fs/lib64  -L/cluster/spack/apps/linux-centos7-x86_64/gcc-4.8.5/gcc-8.2.0-6xqov2fhvbmehix42slain67vprec3fs/lib`
4. Add the `-lGLEW` flag
5. Re-run the command

## Run NGP

1. Setup [X11 forwarding](https://scicomp.ethz.ch/wiki/X11_forwarding_batch_interactive_jobs)

2. Reconnect to Euler using the `-Y` flag for ssh (e.g., `ssh -Y user@euler.ethz.ch`)

3. ```
   env2lmod
   module load gcc/8.2.0 python_gpu/3.8.5
   module load glew/2.1.0
   module load glfw/3.3.4
   bsub -XF -R "rusage[ngpus_excl_p=1]" -R "select[gpu_model0==NVIDIAGeForceRTX2080Ti]" -n 20 -W 30 -Ip "bash"
   ```

4. Once the job starts, run the example demo with:

   ```
   ./build/testbed --scene data/nerf/fox
   ```