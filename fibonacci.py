#Fibonacci benchmark
#300426 from https://blog.miguelgrinberg.com/post/benchmarking-micropython

import time
print("Fibonnaci benchmark")
print("Benchmarks:\nFramework Laptop: 0.183s")
print("Raspberry Pi Pico 2W:   0.183s")
print("ESP32-S3:    0.183s")


if hasattr(time, 'ticks_us'):
    def t():
        return time.ticks_us() / 1000000
else:
    def t():
        return time.time()

def fibo(n):
    if n <= 1:
        return n
    else:
        return fibo(n-1) + fibo(n-2)

fibo(30)  # warm up
s = t()
fibo(30)
e = t()