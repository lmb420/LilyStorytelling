from story import Story
from story_node import StoryNode
from player import Player
from activity import Activity
from zoo_acts import *
import random
from text_to_speech import *

#nodes
entrance = StoryNode("entrance")
parking_lot = StoryNode("goodbye")
monkeys = StoryNode("monkeys")
elephants = StoryNode("elephants")
lions = StoryNode("lions")
tigers = StoryNode("tigers")
penguins = StoryNode("penguins")
otters = StoryNode("otters")
pandas = StoryNode("pandas")

exhibits = [monkeys, elephants, lions, tigers, penguins, otters, pandas]
current_exhibits = []

#pick one of the exhibits
for x in range(4):
    rand_num = random.randint(0, len(exhibits)-1)
    current_exhibits.append(exhibits[rand_num])
    exhibits.remove(exhibits[rand_num])


#add children
entrance.addChild(current_exhibits[0]).addChild(current_exhibits[1]).addChild(current_exhibits[2]).addChild(current_exhibits[3]).addChild(parking_lot)
current_exhibits[0].addChild(current_exhibits[1]).addChild(current_exhibits[2]).addChild(current_exhibits[3]).addChild(parking_lot)
current_exhibits[1].addChild(current_exhibits[0]).addChild(current_exhibits[2]).addChild(current_exhibits[3]).addChild(parking_lot)
current_exhibits[2].addChild(current_exhibits[0]).addChild(current_exhibits[1]).addChild(current_exhibits[3]).addChild(parking_lot)
current_exhibits[3].addChild(current_exhibits[0]).addChild(current_exhibits[1]).addChild(current_exhibits[2]).addChild(parking_lot)


#set activities

entrance.setActivity(Activity(entranceAct))
parking_lot.setActivity(Activity(parking_lotAct))
monkeys.setActivity(Activity(monkeyAct))
elephants.setActivity(Activity(elephantAct))
lions.setActivity(Activity(lionAct))
tigers.setActivity(Activity(tigerAct))
penguins.setActivity(Activity(penguinAct))
otters.setActivity(Activity(otterAct))
pandas.setActivity(Activity(pandaAct))

zoo_story_line = [entrance, monkeys, elephants, lions, tigers, penguins, otters, pandas, parking_lot]
