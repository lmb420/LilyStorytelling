class Animal(object):
    def __init__(self, pet_type):
        if pet_type == "dog":
            self.type = "dog"
            self.feet = "paws"
            #self.mouth = "mouth"
            self.body_covering = "fur"
            self.bc_plural = "is"
            self.tail = True
            self.eats = "dog food"
            
        elif pet_type == "cat":
            self.type = "cat"
            self.feet = "paws"
            #self.mouth = "mouth"
            self.body_covering = "fur"
            self.bc_plural = "is"
            self.tail = True
            self.eats = "cat food"
        elif pet_type == "fish":
            self.type = "fish"
            self.feet = "fins"
            #self.mouth = "mouth"
            self.body_covering = "scales"
            self.bc_plural = "are"
            self.tail = False
            self.eats = "fish food"
        elif pet_type == "bird":
            self.type = "bird"
            self.feet = "claws"
            #self.mouth = "beak"
            self.body_covering = "feathers"
            self.bc_plural = "are"
            self.tail = False
            self.eats = "seeds"
        elif pet_type == "lizard":
            self.type = "lizard"
            self.feet = "feet"
            #self.mouth = "mouth"
            self.body_covering = "skin"
            self.bc_plural = "is"
            self.tail = True
            self.eats = "cricekts"
        else:
            self.type = "pet"
            self.feet = "feet"
            #self.mouth = "mouth"
            self.body_covering = "body"
            self.bc_plural = "is"
            self.tail = False
            self.eats = "pet food"
