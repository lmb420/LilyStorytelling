from story import Story
from story_node import StoryNode
from player import Player
from activity import Activity
from text_to_speech import *
from _vault_acts import *

#Nodes
main = StoryNode("main")
left = StoryNode("left")
right = StoryNode("right")

#Children
main.addChild(left).addChild(right)
right.addChild(main)
left.addChild(main)

#Activities
main.setActivity(Activity(main_act))
left.setActivity(Activity(left_act))
right.setActivity(Activity(right_act))

#Storyline
vault_story_line = [main, left, right]
