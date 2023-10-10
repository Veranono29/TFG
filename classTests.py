from dataclasses import dataclass
from functools import partial
import timeit

@dataclass(slots=False)
class Person:
    name:str
    address:str
    email:str

@dataclass(slots=True)
class PersonSlots:
    name:str
    address:str
    email:str

def get_set_del(person:Person|PersonSlots):
    person.name
    person.name = "12 Colorado, España"
    person.address="2323"



def main():
    print("main")
    person = Person(name="Gerardo",address="Madrid, España",email="email@email.com")
    personSlots = PersonSlots("Gerardo","Madrid, España","email@email.com")
    slots = min(timeit.repeat(partial(get_set_del,personSlots),number=100000))
    noSlots = min(timeit.repeat(partial(get_set_del,person),number=100000))
    

    print(f"No Slots: {(noSlots)}")
    print(f"Slots: {(slots)}")
    print(f"Improve: {(noSlots-slots)/noSlots:.2%}")
    

if __name__ == "__main__":
    main()