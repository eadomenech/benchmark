# import programs as prog
# from kernels import QKKernel
import numpy as np
import pyopencl as cl

mf = cl.mem_flags
local_size = (8, 8,)

DQKT = """
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable

    __constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE |
        CLK_ADDRESS_CLAMP | CLK_FILTER_NEAREST;

    __kernel void directa(read_only image2d_t in,
    __global const float *k, write_only image2d_t out)
    {
        int x = get_global_id(0);
        int y = get_global_id(1);
        int2 coord = (int2)(x, y);
        double c_temp = 0.0;
        float4 pixel = read_imagef(in, sampler, coord);
        for(int a = 0; a < 8; a++){
            for(int b = 0; b < 8; b++){
                float4 p = read_imagef(in, sampler, (int2)(a, b));
                c_temp += (k[a * 8 + x] * k[b * 8 + y] * p.x);
            }
        }
        pixel.x = c_temp;
        write_imagef(out, coord, pixel);
    }

    __kernel void inversa(read_only image2d_t in,
    __global const float *k, write_only image2d_t out)
    {
        int x = get_global_id(0);
        int y = get_global_id(1);
        int2 coord = (int2)(x, y);
        double c_temp = 0.0;
        float4 pixel = read_imagef(in, sampler, coord);
        for(int a = 0; a < 8; a++){
            for(int b = 0; b < 8; b++){
                float4 p = read_imagef(in, sampler, (int2)(a, b));
                c_temp += (k[x * 8 + a] * k[y * 8 + b] * p.x);
            }
        }
        pixel.x = c_temp;
        write_imagef(out, coord, pixel);
    }
"""

# Krawtchouk
QKKernel = [
    0.0147885, -0.059767, 0.158129, -0.311834, 0.476334, -0.563607, 0.497054, -0.286974,
    0.059767, -0.192251, 0.378225, -0.488673, 0.353587, 0.0464855, -0.45096, 0.497054,
    0.158129, -0.378225, 0.474875, -0.223586, -0.252437, 0.41582, 0.0464855, -0.563607,
    0.311834, -0.488673, 0.223586, 0.298509, -0.330481, -0.252437, 0.353587, 0.476334,
    0.476334, -0.353587, -0.252437, 0.330481, 0.298509, -0.223586, -0.488673, -0.311834,
    0.563607, 0.0464855, -0.41582, -0.252437, 0.223586, 0.474875, 0.378225, 0.158129,
    0.497054, 0.45096, 0.0464855, -0.353587, -0.488673, -0.378225, -0.192251, -0.059767,
    0.286974, 0.497054, 0.563607, 0.476334, 0.311834, 0.158129, 0.059767, 0.0147885
]

class DqktGPGPU:

    def __init__(self, kernel=QKKernel):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)
        self.kernel_buffer = cl.Buffer(
            self.ctx,
            mf.READ_ONLY | mf.COPY_HOST_PTR,
            hostbuf=np.array(kernel).astype(np.float32)
        )
        self.program = cl.Program(self.ctx, DQKT).build()

    def dqkt_r(self, block):
        input = BlockInput(block, self.ctx)
        exec_evt = self.program.directa(
            self.queue,
            (8, 8,),
            None,
            input.orig_buffer,
            self.kernel_buffer,
            input.dest_buffer
        )
        return self._exec_event(exec_evt, buffer=input.dest_buffer, host_buffer=input.dest)

    def idqkt_r(self, image_orig):
        input = BlockInput(image_orig, self.ctx)
        exec_evt = self.program.inversa(
            self.queue,
            (8, 8),
            None,
            input.orig_buffer,
            self.kernel_buffer,
            input.dest_buffer
        )
        return self._exec_event(exec_evt, buffer=input.dest_buffer, host_buffer=input.dest)

    def _exec_event(self, evt, buffer=None, host_buffer=None):
        evt.wait()
        cl.enqueue_copy(self.queue, host_buffer, buffer, origin=(0, 0), region=(8, 8))
        return host_buffer


class BlockInput:
    def __init__(self, block, ctx):
        self.dest = np.empty_like(block)
        self.orig_buffer = cl.image_from_array(ctx, block, num_channels=1)
        self.dest_buffer = cl.image_from_array(ctx, self.dest, num_channels=1, mode="w")
