from dataclasses import dataclass,field
from typing import Any
from main import *

@dataclass
class OscillatorConfig:
    liczba_krokow: int = 1000
    dt: float  = 0.01
    k: float = 1
    m: float = 2.5
    c: float = 0.3


@dataclass
class OscillatorState:
    numer_kroku: int = 0
    x: float = 0
    v: float = 1


@dataclass
class OscillatorStatistics:
    x: float = 0
    v: float = 0
    E_k: float = 0
    E_p: float = 0
    

@dataclass
class FinalOscillatorStatistics:
    max_v: float = 0
    max_E_k: float = 0
    max_E_p: float = 0


@dataclass
class OscillatorResult:
    config: OscillatorConfig = None
    historia_stanow: list[OscillatorState] = field(default_factory=list)
    historia_statystyk: list[OscillatorStatistics] = field(default_factory=list)
    statystyki_koncowe: FinalOscillatorStatistics = None


##############################################################################

class OscillatorRule(StepRule):
    def __init__(self,config):
        self.config = config
    def nastepny_krok(self, obecny_stan):
        k = self.config.k
        m = self.config.m
        dt = self.config.dt
        c = self.config.c

        x = obecny_stan.x
        v = obecny_stan.v
        a = -(k/m)*x - (c/m)*v
        new_v = v + a*dt
        new_x = x + new_v*dt
        return OscillatorState(obecny_stan.numer_kroku+ 1, x= new_x,v = new_v)
    
class OscillatorAnalyzer(StepAnalyzer):
    def __init__(self,config):
        self.config = config
    def analiza(self,stan):
        self.E_k = self.config.m*stan.v*stan.v*0.5
        self.E_p = self.config.k*stan.x*stan.x*0.5
        return OscillatorStatistics(stan.x,stan.v,self.E_k,self.E_p)

class Rysowanie(Visualizer):
    def __init__(self,config):
        self.config = config
    def rysuj(self,wyniki):
        kroki_tab = np.arange(1,self.config.liczba_krokow+1)*0.01

        x = [stat.x for stat in wyniki.historia_statystyk]
        v = [stat.v for stat in wyniki.historia_statystyk]
        E_k = [stat.E_k for stat in wyniki.historia_statystyk]
        E_p = [stat.E_p for stat in wyniki.historia_statystyk]

        plt.subplot(2,2,1)
        plt.plot(kroki_tab,x)
        plt.grid()
        plt.title('x(t)')
        plt.xlabel('t[s]')

        plt.subplot(2,2,2)
        plt.plot(kroki_tab,v)
        plt.grid()
        plt.title('v(t)')
        plt.xlabel('t[s]')

        plt.subplot(2,2,3)
        plt.title('Energia kinetyczna')
        plt.plot(kroki_tab,E_k)
        plt.grid()
        plt.xlabel('t[s]')

        plt.subplot(2,2,4)
        plt.title('Energia potencjalna')
        plt.plot(kroki_tab,E_p)
        plt.grid()
        plt.xlabel('t[s]')
        
        plt.tight_layout(h_pad=3.0, w_pad=3.0)

        plt.savefig('wykresy.png', dpi=300, bbox_inches='tight')
        plt.show()

class AnalizerFinalnychStatystyk(FinalAnalyzer):
    def wyznaczenie_finalnych_statystyk(self,historia_statystyk):
        lista_v = [stat.v for stat in historia_statystyk]
        lista_E_k = [stat.E_k for stat in historia_statystyk]
        lista_E_p = [stat.E_p for stat in historia_statystyk]
        
        max_v = max(np.abs(lista_v))
        max_E_k = max(lista_E_k)
        max_E_p = max(lista_E_p)
        print('##########################')
        print(f'Maksymalna predkosc: {max_v}')
        print(f'Maksymalna energia kinetyczna: {max_E_k}')
        print(f'Maksymalna energia potencjalna: {max_E_p}')
        print('##########################')
        return FinalOscillatorStatistics(max_v,max_E_k,max_E_p)

    
print('Podaj ile sekund ma trwać symulacja:')
ile_sekund_input = int(input()) 
print('Podaj współzcynnik k sprężyny:')
k_input = float(input())
print('Podaj masę obiektu:')
m_input = float(input())
print('Podaj współczynnik tłumienia:')
c = float(input())

print('Podaj początkowe wychylenie ciężarka:')
x0_input = float(input())
print('Podaj początkową prędkość ciężarka:')
v0_input = float(input())


config = OscillatorConfig(int(ile_sekund_input/0.01),0.01,k_input,m_input,c)
stan_poczatkowy = OscillatorState(0,x0_input,v0_input)
regula = OscillatorRule(config)
analizator = OscillatorAnalyzer(config)
wyniki = OscillatorResult()
rysowanie = Rysowanie(config)
statystyki_kroku = OscillatorStatistics()
finalne_statystyki = FinalOscillatorStatistics()
analizator_finalnych_statystyk = AnalizerFinalnychStatystyk()

sim = Simulation(config,stan_poczatkowy,regula,analizator,wyniki,rysowanie,statystyki_kroku,analizator_finalnych_statystyk,finalne_statystyki)
sim.start()