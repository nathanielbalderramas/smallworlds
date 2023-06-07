class Organism:
    last_id = 1
    @staticmethod
    def get_new_id():
        new_id = Organism.last_id
        Organism.last_id += 1
        return new_id

    def __init__(self, species_name, navigator, speed, food_need, feeding_range, feeding_chance, offspring_chance):
        self.id = Organism.get_new_id()
        self.species_name = species_name
        self.navigator = navigator
        self.speed = speed
        self.food_need = food_need
        self.feeding_range = feeding_range
        self.feeding_chance = feeding_chance
        self.offspring_chance = offspring_chance


if __name__ == "__main__":
    o1 = Organism()
    o2 = Organism()
    o3 = Organism()
    print(o1.id, o2.id, o3.id)

