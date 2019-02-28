#!/usr/bin/env python

with open('test_job.in', 'r') as f:
    input = f.read().strip()

with open('interim.out', 'w') as i:
    for n in range(0, 3):
        i.write(str(n))


with open('test_job.out', 'w') as o:
    o.write(input + ' Goodbye!')
