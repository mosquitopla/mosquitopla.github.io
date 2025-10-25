class Instrument:
    def play(self):
        return "Інструмент видає звук"
        
    def info(self):
        return "Це просто інструмент"
    
class Guitar(Instrument):
    def play(self):
        return "Гітара видає звук"
    
    def info(self):
        return "Гітара - струнний інструмент"
    
class Piano(Instrument):
    def play(self):
        return "Піаніно видає звук"
    
    def info(self):
        return "Піаніно - клавішний інструмент"
    
def make_sound(instrument):
    print(f"{instrument.info()} грає: {instrument.play()}")
    
    
class MusicTrack:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __add__(self, other):
        return MusicTrack(self.name + " & " + other.name,
                          self.duration + other.duration)

    def __eq__(self, other):
        return self.duration == other.duration

    def __str__(self):
        return f"Трек: {self.name}, тривалість: {self.duration} хв."
    

if __name__ == "__main__":
    Instruments = [Guitar(), Piano(), Instrument()]
    for a in Instruments:
        make_sound(a)
        
    print("-" * 40)
    
    track1 = MusicTrack("Мелодія", 3)
    track2 = MusicTrack("Соната", 5)
    mix = track1 + track2

    print(track1)
    print(track2)
    print("Мікс:", mix)
    print("Чи однакова тривалість?", track1 == track2)
    