import programs as prog
from kernels import QKKernel
import numpy as np
import pyopencl as cl

mf = cl.mem_flags
local_size = (8, 8,)


class DqktGPGPU:

    def __init__(self, kernel=QKKernel):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)
        self.kernel_buffer = cl.Buffer(
            self.ctx,
            mf.READ_ONLY | mf.COPY_HOST_PTR,
            hostbuf=np.array(kernel).astype(np.float32)
        )
        self.program = cl.Program(self.ctx, prog.DQKT).build()

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
