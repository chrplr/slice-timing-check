#! /usr/bin/env python
# Time-stamp: <2016-08-03 16:49:04 cp983411>

""" Generate an EPI containing a sinewave, sampled at different delays on the z axis.
Useful to test slice timing algorithms """

import numpy as np
from numpy import pi, linspace, sin
import nibabel as nib


shape = (32, 32, 40, 100)
nx, ny, nz, nt = shape

TR = 1.  # 1 sec
slices_times = linspace(0, TR - (TR / nz) / nz, nz)  # delays
print('slice times:')
print(slices_times)

scan_times = linspace(0, TR * (nt - 1), nt)
print('scan times:')
print(scan_times)

T_PERIOD = 10.
print('Period:')
print(T_PERIOD)

times = scan_times[:, np.newaxis] - slices_times
print('Times')
print(times)

slices = 1000. + 100. * sin(2. * pi * times / T_PERIOD)

data = np.empty(shape, dtype='<i2')
data[: , :, ...] = slices.T

affine = np.array([[ -3.       ,   0.        ,   0.        ,  92.],
                   [  0.       ,   3.        ,   0.        , -92.],
                   [  0.       ,   0.        ,   3.        , -40.],
                   [  0.       ,   0.        ,   0.        ,   1.]])

new_image = nib.Nifti1Image(data, affine)
nib.save(new_image, "sinewave.nii")
