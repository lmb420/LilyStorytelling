from story import Story
from story_node import StoryNode
from player import Player
from activity import Activity
from theater_acts import *
from text_to_speech import *


#create each node in the story
theater = StoryNode("theater")
box_office = StoryNode("box office")
concessions = StoryNode("concessions")
ticket_checker = StoryNode("ticket checker")
movie = StoryNode("movie")

#add connections between nodes
theater.addChild(box_office).addChild(concessions)

concessions.addChild(box_office).addChild(ticket_checker)
box_office.addChild(concessions).addChild(ticket_checker)
ticket_checker.addChild(movie)


#add prerequisites (something that must be completed before moving to this node)
ticket_checker.addPrereq("ticket")

#movies and menu are lists of options for the activity
movies = ["Inside Out", "Tomorrowland", "Minions", "Home"]
menu = ["soda", "popcorn", "candy", "finished"]

#create activities and add them to their corresponding nodes  
theater.setActivity(Activity(theaterActivity))
box_office.setActivity(Activity(boxOfficeActivity, movies))
concessions.setActivity(Activity(concessionsActivity, menu))
ticket_checker.setActivity(Activity(ticketCheckerActivity))
movie.setActivity(Activity(movieActivity))


movie_story_line = [theater, concessions, box_office, ticket_checker, movie]
