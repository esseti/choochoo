

__author__ = 'stefano'


def sottrai(da, cosa):
    return da[(da.index(cosa) + len(cosa)):]


def sottostringa(da, inizio, fine=None):
    if fine:
        return da[(da.index(inizio) + len(inizio)):da.index(fine)]
    else:
        return da[(da.index(inizio) + len(inizio)):]
