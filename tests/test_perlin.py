from core.perlin import Perlin

def test_perlin():
    perlin = Perlin(4, 4, octaves = 3, seed = 1)
    print(perlin._data)
    print('----')
    sliced = perlin.slice(2, 2, 2, 2)
    print(sliced._data)
    print('----')
    last = sliced.slice(0, 1, 1, 1)
    print(last._data)
    assert perlin.max > 0