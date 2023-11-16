from fileinput import filename
import os
import random


class Agent:
    name=""
    def move(self, opponent_last_move: str):
        return
    
# move = "+" if agent cooperats, "-" if agent cheats
class MrGood(Agent):
    name="Mr. Good"
    def move(self, opponent_last_move: str):
        return "+"

class MrEvil(Agent):
    name="Mr. Evil"
    def move(self, opponent_last_move: str):
        return "-"

class MrRandom(Agent):
    name="Mr. Random"
    def move(self, opponent_last_move:str):
        return random.choice(['+', '-'])
    
class MrCopy(Agent):
    name="Mr. Copy"
    def move(self, opponent_last_move: str):
        if opponent_last_move == None:
            return "+"
        else:
            return opponent_last_move

class MrGrudge(Agent):
    name="Mr. Grudge"
    cheated = False
    def move(self, opponent_last_move: str):
        if opponent_last_move == "-":
            self.cheated = True
        if self.cheated:
            return "-"
        else:
            return "+"
        
class MrSherlock(Agent):
    name="Mr. Sherlock"
    cheated = False
    round = 0
    premoves = ["+","-","+", "+"]
    def move(self, opponent_last_move: str):
        # how opponent acts in first 4 rounds?
        if self.round <= 4:            
            if opponent_last_move == "-":
                self.cheated = True        
        if self.round < 4:
            move = self.premoves[self.round]           
        else:
            if self.cheated:
                move = opponent_last_move                
            else:
                move = "-"        
        self.round = self.round+1
        return move
            
class Tournament:
    agent_list = [] 
    agent_rewards = [] 
    rounds = 0
    results = {("+","+"):(2,2), ("+","-"):(-1,3),("-","+"):(3,-1),("-","-"):(0,0)}
    # points for al posible situations of the match

    def Match(self,agent1_number:int, agent2_number:int):
        score1 = 0
        score2 = 0

        agent1_history = None # just his previous move
        agent2_history = None

        agent1 = self.agent_list[agent1_number]() 
        agent2 = self.agent_list[agent2_number]()

        for i in range(self.rounds):
            move1 = agent1.move(agent2_history) # his move might depend on opponents' previous move
            move2 = agent2.move(agent1_history)
            moves = (move1,move2) # we use this in results to give the right amount of points to both agents

            agent1_history = move1
            agent2_history = move2

            score1 += self.results[moves][0]
            score2 += self.results[moves][1]

        self.agent_rewards[agent1_number]+=score1
        self.agent_rewards[agent2_number]+=score2

    def DoMatch(self): # does match for all combinations of agents from the list
        for i in range(len(self.agent_list)):
            for j in range(len(self.agent_list)):
                if i<j: # each agent plays with all other agents just once
                    self.Match(i,j)

    def __init__(self, number_of_rounds:int, agent_list):
        self.rounds = number_of_rounds
        self.agent_list = agent_list
        self.agent_rewards = [0]*len(agent_list)

    def Print_score(self):
        filename = "Game_results6.csv"
                
        with open(filename,"a") as file:
            is_file_empty = os.stat(filename).st_size == 0 # if the file is empty, create a header at first
            if is_file_empty:
                header = "Number of rounds,Agent name,Agent score\n"
                file.write(header)
            
            for i in range(len(self.agent_list)):
                line = str(self.rounds)+","+str(self.agent_list[i].name)+","+ str(self.agent_rewards[i])+"\n"
                file.write(line)
            
agents = [MrCopy, MrEvil, MrGood, MrGrudge, MrRandom, MrSherlock] # list of all defined agents
agent_list=[] 

def multiple_append(agent, number): 
    for i in range(number):
        agent_list.append(agent)

print("There are 6 types of agents: Mr. Copy, Mr. Evil, Mr. Good, Mr. Grudge, Mr. Random and Mr. Sherlock. You can choose how many agents of each type will participate this game.")
for i in range(len(agents)):
    line= "Number of {} in game: ".format(str(agents[i].name))
    num = int(input(line))
    multiple_append(agents[i],num)

# do match for a given number of rounds
for i in range(1,11):
    match1 = Tournament(i, agent_list)
    match1.DoMatch()
    match1.Print_score()
print(str(filename) + "was saved")