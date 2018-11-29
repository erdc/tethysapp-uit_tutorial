#!/usr/bin/env python3

with open('test_job.in', 'r') as f:
    input = f.read().strip()

with open('test_job.out', 'w') as o:
    o.write(input + ' Goodbye!')
