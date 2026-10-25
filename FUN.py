import numpy as np
import matplotlib.pyplot as plt
def fun(x0,lk,r):
    x = x0
    x_lista = []
    q = np.linspace(1,lk,lk)
    for i in range(lk):
        x_lista.append(x)
        x = r*x*(1-x)
        if x<0 or x>1:
            print(f'Liczba nr. {i+1}: {x:.5} jest poza zakresem dla r = {r}')
            break
    plt.scatter(q, x_lista)
    plt.title(str(r))
    plt.show()
    # print(x_lista)


# x0 = float(input('Podaj x0: '))
# lk = int(input('Podaj liczbe krokow: '))
r = float(input('Podaj parametr r: '))
x0 = 0.1
lk = 1000

# fun(x0,lk,r)

r_wart = np.linspace(3.4,3.7,20)

for r1 in r_wart:
    fun(x0,lk,float(r1))

