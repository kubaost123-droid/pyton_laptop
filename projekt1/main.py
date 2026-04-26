from abc import ABC, abstractmethod

class Simulation():
    def __init__(self,config,stan_poczatkowy,regula,analizator,wyniki,rysowanie,statystyki_kroku,analizator_finalnych_statystyk,finalne_statystyki):
        self.config = config
        self.obecny_stan = stan_poczatkowy
        self.regula = regula
        self.analizator = analizator
        self.wyniki = wyniki
        self.rysowanie = rysowanie
        self.statystyki_kroku = statystyki_kroku
        self.analizator_finalnych_statystyk = analizator_finalnych_statystyk
        self.finalne_statystyki = finalne_statystyki
    
    def start(self):
        self.wyniki.config = self.config
        for krok in range(1,self.config.liczba_krokow+1):

            nowy_stan = self.regula.nastepny_krok(self.obecny_stan)
            
            self.wyniki.historia_stanow.append(nowy_stan)
            self.statystyki_kroku = self.analizator.analiza(nowy_stan)
            self.wyniki.historia_statystyk.append(self.statystyki_kroku)

            self.obecny_stan = nowy_stan
        self.finalne_statystyki = self.analizator_finalnych_statystyk.wyznaczenie_finalnych_statystyk(self.wyniki.historia_statystyk)
        self.wyniki.statystyki_koncowe = self.finalne_statystyki
        
        self.rysowanie.rysuj(self.wyniki)


class StepRule(ABC):
    def __init__(self,config):
        self.config = config

    @abstractmethod
    def nastepny_krok(self,obecny_stan):
        pass


class StepAnalyzer(ABC):
    @abstractmethod
    def analiza(self,obecny_stan):
        pass


class FinalAnalyzer(ABC):
    @abstractmethod
    def wyznaczenie_finalnych_statystyk(self,historia_stanow):
        pass


class Visualizer(ABC):
    def rysuj(self,wyniki):
        pass