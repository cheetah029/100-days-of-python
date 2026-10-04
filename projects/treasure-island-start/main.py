print('''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.") 
choice1 = input('You\'re at a crossroad. Where do you want to go? Type "left" or "right"\n').lower()

if choice1 == "left":
  choice2 = input('You\'ve come to a lake. There is an island in the middle of the lake. Type "wait" to wait for a boat. Type "swim" to swim across.\n').lower()
  if choice2 == "wait":
    choice3 = input("You arrive at the island unharmed. There is a house with 3 doors. One red, one yellow and one blue. Which color do you choose?\n").lower()
    if choice3 == "red":
      print("It's a room full of fire. Game Over.")
    elif choice3 == "yellow":
      print("You found the treasure! You Win!")
    elif choice3 == "blue":
      print("You enter a room of beasts. Game Over.")
    else:
      print("You chose a door that doesn't exist. Game Over.")
  elif choice2 == "swim":
    print("Oops! This lake is inhabited by crocodiles. Game Over.")
  else:
    print("You chose an action that can't be done. Game Over.")
elif choice1 == "right":
  house = input('You come across a sign that says "Danger! Monster village ahead." It\'s getting dark and you have to find a place to sleep, but now you\'re lost and have no choice but to ascend along this path. You find two houses ahead, which you must choose between to sleep in. The one on the left is an old and spooky broken-down house that is full of cobwebs. The house on the right is in perfect condition, but, mysteriously, there are no windows. Which house do you choose, the one on the left or the one on the right? Type "left" to sleep in the old broken-down house. Type "right" to sleep in the house with no windows.\n').lower()
  if house == "left":
    door = input('You grow weary and tired and collapse on the dusty bed. You wake up the next morning but find that you are in a room completely different from the room you had slept in last night. In front of you are 3 doors, one of which contains the treasure and leads out. The other two will kill you. The first one has 5 locks, whose keys are weirdly lying right in front of you. The second one looks very normal, like the door of any house you would normally live in. The third door has a sign attatched to it that says "Beware! Man-eating werewolf inside!" Which door do you choose to go into? Type "1" to unlock the first door with the 5 locks. Type "2" to open the second door. Type "3" to open the third door with the sign.\n')
    if door == "1":
      print("You unlock the first door and go inside. There's a massive ruby, shining a splendid bright red. But wait! That's not the treasure you were looking for. Those locks on the door definitely meant that there would be something very valuable inside, but they also meant that it would probably be protected by high-tech surveillance too! You get zapped by a moving laser beam before you can take the ruby. Game Over.")
    elif door == "2":
      print("Surprise surprise! This is the home of a werewolf! Did you really think that that sign on door 3 was actually true? Well, if you did, then you probably didn't think carefully about the fact that if a door looks normal, then there's probably something living in the room behind it! Next time, think carefully before making your decision. Game Over.")
    elif door == "3":
      print("Congratulations! You found the treasure! That sign on the door was just there to trick you so that you wouldn't find the treasure. You happily take the treasure and head home.")
    else:
      print("You chose a door that doesn't exist. Game Over.")
  elif house == "right":
    print("Too bad! This house is inhabited by vampires, did you forget that this is a monster village? But wait! That also reminds you of the fact that vampires hate sunlight. No wonder this house had no windows! The vampires find you and devour you at first sight. Game Over.")
  else:
    print("You chose a house that doesn't exist. Game Over.")
else:
  print("You chose a path that doesn't exist. Game Over.")
  

#https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Treasure%20Island%20Conditional.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1oDe4ehjWZipYRsVfeAx2HyB7LCQ8_Fvi%26export%3Ddownload