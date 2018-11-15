
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
