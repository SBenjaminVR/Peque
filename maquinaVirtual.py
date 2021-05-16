from memoriaVirtual import MemoriaVirtual

ds = []
cs = []
ss = []
es = []

memoriaVirtual = MemoriaVirtual(ds, cs, ss, es)

def AsignarMemoriaGlobal(numero):
    memoriaVirtual.ds.append(numero)
