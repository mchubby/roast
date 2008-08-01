import os

def process(op):
    f = op.open_output(op.path)
    while True:
        data = op.input.read(8192)
        if not data:
            break
        f.write(data)
    f.close()
