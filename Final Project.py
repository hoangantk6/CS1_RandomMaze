"""
A-maze-ing Game
Author: An Nguyen, Bach Le
Instructor: Linh Tran
"""
from sys import argv
import pygame
from pygame.locals import *
import random as r
import time
import dimensions as di

width= 0
height=0
cell_width=65
cell_height=65
clock = pygame.time.Clock()
edges=[]

class Maze:
    def __init__(self, rows, cols):
        """Generate a maze base on Prim's Algorithm"""
        
        """Set Rows and Collumns base on size"""
        self.rows = rows
        self.cols = cols
        self.keep_going = 1
        
        """Make the dictionary: (x,y): {right, bellow, visited}"""
        self.maze={}
        for row in range(rows):
            for col in range(cols):
                #Each Cell have Right wall and Bellow wall, and it not be visited
                cell = {'right':1, 'bellow':1, 'visited':0}
                #Add cell to maze
                self.maze[(row,col)]=cell
    
    def generate_maze(self, root=None, in_tree=[]):
        """Generate maze base on Prim's algorithm"""
        if root == None:
            #root = (self.rows//2,self.cols//2)
            root =(0,0)
        
        """Check the fininsh of the tree"""
        self.check_finished()   
        if not self.keep_going:
            return
        
        """Start a tree from a root"""
        if len(in_tree)==0:
            in_tree.append(root)
            self.maze[root]['visited']=1
            
        """Current vertice is the last vertice of the tree"""
        curr = in_tree[-1]
        
        """Check around the vertice and randomly choose one vertice to add a vertice and a edges"""
        next_vertice = self.neighbors(curr,in_tree)
        
        """Next vertice become the last vertice of the tree"""
        in_tree.append(next_vertice[0])
        
        """Add new edges"""
        edges.append([next_vertice[1], next_vertice[0]])

        curr = next_vertice[1]
        
        """Remove wall cross the edges"""
        self.remove_wall(next_vertice)
        
        """Generate_maze again: new current vertice and new tree"""
        self.generate_maze(curr, in_tree)
    
    def neighbors(self, curr, in_tree):
        """Find the avaialbe neighbor for previous cell"""
        curr_x, curr_y=curr[0],curr[1]
        
        """Create a list of avaiable neighbor"""
        avai_neighbors =[]
        
        """Check around the vertice"""
        UP = (curr_x, curr_y-1)
        BELLOW = (curr_x, curr_y+1)
        RIGHT = (curr_x+1, curr_y)
        LEFT = (curr_x-1, curr_y)
        if UP in self.maze and self.maze[UP]['visited'] == 0:
          avai_neighbors.append([UP,'UP'])
        if BELLOW in self.maze and self.maze[BELLOW]['visited'] == 0:
          avai_neighbors.append([BELLOW,'BELLOW'])
        if RIGHT in self.maze and self.maze[RIGHT]['visited'] == 0:
          avai_neighbors.append([RIGHT,'RIGHT'])
        if LEFT in self.maze and self.maze[LEFT]['visited'] == 0:
          avai_neighbors.append([LEFT,'LEFT'])

        """Get one vertice from random a list of avaiable neighbor"""
        if avai_neighbors != []:
            neighbor=avai_neighbors[r.randint(0,len(avai_neighbors)-1)]
            self.maze[neighbor[0]]['visited'] = 1
            return neighbor[0], curr, neighbor[1]
            #[0]: neighbor, [1]: current vertices, [2]:relation between neighbor and current veritces
        else:
            if self.keep_going:
                """
                    If around vertice do not have any neighbor but the maze is not finished
                    Randomly choose a vertice in tree and check around this vertice
                """
                return self.neighbors(in_tree[r.randint(0, len(in_tree)-1)], in_tree)
        
    def remove_wall(self, neighbor):
        """Check the relatition between current and new vertice to remove the wall cross the edges"""
        if neighbor[2] == 'UP':
            self.maze[neighbor[0]]['bellow'] = 0
        if neighbor[2] == 'BELLOW':
            self.maze[neighbor[1]]['bellow'] = 0
        if neighbor[2] == 'LEFT':
            self.maze[neighbor[0]]['right'] = 0
        if neighbor[2] == 'RIGHT':
            self.maze[neighbor[1]]['right'] = 0
        
    def check_finished(self):
        """If all vertice have been visited, finish generate maze"""
        done = 1
        for k in self.maze:
            if self.maze[k]['visited'] == 0:
                done = 0
                break
        if done:
            self.keep_going = 0

class StartGame:
    def __init__(self):
        """Start screen and choose some option(size, character)"""
        gameDisplay = pygame.display.set_mode((800,600))
        gameDisplay.fill((255,248,235))
        self.width, self.height=0,0

        self.choose_cha="1"
        self.level =0
        
    def load(self,filename):
        """
        This function loads an .png image based on the name input
        Parameters:
            filename - the file's name (without '.png')
        Returns:
            a specific image
        """
        img = pygame.image.load(filename + '.png')
        return img
    
    def begin_screen(self):
        gameDisplay = pygame.display.set_mode((800,600))
        gameDisplay.fill((240,234,220))
        
        #Play button's reference points
        P_LEFT, P_RIGHT, P_UP, P_DOWN = di.get_dimensions('play')
        #Linh button's reference points
        L_LEFT, L_RIGHT, L_UP, L_DOWN = di.get_dimensions('linh')
        #Seb button's reference points
        S_LEFT, S_RIGHT, S_UP, S_DOWN = di.get_dimensions('seb')
        #Graeme button's reference points
        G_LEFT, G_RIGHT, G_UP, G_DOWN = di.get_dimensions('graeme')
        #Easy button's reference points
        E_LEFT, E_RIGHT, E_UP, E_DOWN = di.get_dimensions('easy')
        #Normal button's reference points
        N_LEFT, N_RIGHT, N_UP, N_DOWN = di.get_dimensions('normal')
        #Hard button's reference points
        H_LEFT, H_RIGHT, H_UP, H_DOWN = di.get_dimensions('hard')
        #Close button's reference points
        C_LEFT, C_RIGHT, C_UP, C_DOWN = di.get_dimensions('close')

        #Start screen
        intro = False
        screen = gameDisplay.blit(self.load('start_screen'), (0, 0))
        while not intro:
            pygame.display.update()
            mos = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    quit()
                if P_LEFT <= mos[0] <= P_RIGHT and P_UP <= mos[1] <= P_DOWN:
                    screen = gameDisplay.blit(self.load('start_now'), (0, 0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        intro = True
                else:
                    screen = gameDisplay.blit(self.load('start_screen'), (0, 0))
           
        #Choose the difficulties
        choose_level = False
        screen = gameDisplay.blit(self.load('diff_screen'), (0, 0))
        while not choose_level:
            pygame.display.update()
            screen
            mos = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if E_LEFT <= mos[0] <= E_RIGHT and E_UP <= mos[1] <= E_DOWN:
                    screen = gameDisplay.blit(self.load('diff_easy'), (0, 0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.width = 8
                        self.height = 8
                        self.level=1
                        choose_level = True
                elif N_LEFT <= mos[0] <= N_RIGHT and N_UP <= mos[1] <= N_DOWN:
                    screen = gameDisplay.blit(self.load('diff_nor'), (0, 0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.width = 11
                        self.height = 11
                        self.level=2
                        choose_level = True
                elif H_LEFT <= mos[0] <= H_RIGHT and H_UP <= mos[1] <= H_DOWN:
                    screen = gameDisplay.blit(self.load('diff_hard'), (0, 0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.width = 12
                        self.height = 12
                        self.level=3
                        choose_level = True
                else:
                    screen = gameDisplay.blit(self.load('diff_screen'), (0, 0))

        #Choose the characters to play
        choose_character = False
        screen = gameDisplay.blit(self.load('character_screen'), (0, 0))
        
        while not choose_character:
            pygame.display.update()
            screen
            mos = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if L_LEFT <= mos[0] <= L_RIGHT and L_UP <= mos[1] <= L_DOWN:
                    screen = gameDisplay.blit(self.load('character_linh'), (0, 0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.choose_cha=str(1)
                        choose_character = True
                elif S_LEFT <= mos[0] <= S_RIGHT and S_UP <= mos[1] <= S_DOWN:
                    screen = gameDisplay.blit(self.load('character_seb'), (0, 0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.choose_cha=str(2)
                        choose_character = True
                elif G_LEFT <= mos[0] <= G_RIGHT and G_UP <= mos[1] <= G_DOWN:
                    screen = gameDisplay.blit(self.load('character_graeme'), (0, 0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.choose_cha=str(3)
                        choose_character = True
                else:
                    screen = gameDisplay.blit(self.load('character_screen'), (0, 0))

class Game:
    def __init__(self,width,height, level):
        """Set maze size and choose character"""
        self.size = (width*cell_width,height*cell_height)
        pygame.display.set_caption('Maze Project')
        
        w, h = cell_width - 3, cell_height - 3
        self.rect = 0, 0, w, h
        base = pygame.Surface((w,h))
        base.fill( (240,234,220) )
        pygame.display.set_caption("A-maze-ing")
        
        start_game=StartGame()
        self.cha_name={"1":"Linh","2":"Seb","3":"Graeme"}
        self.level_option={"1":"easy", "2":"normal", "3":"hard"}
        
    def load(self,filename):
        """Load png file"""
        name = pygame.image.load(filename + '.png')
        return name
  
    
    def draw_maze(self):
        """Draw a maze base on generate maze class"""
        self.screen = pygame.display.set_mode(self.size,pygame.RESIZABLE)
        self.screen.fill( (240,234,220) )
        sub = self.screen.subsurface(self.rect)      
        pygame.display.update()

        #Use it when you want to know how to generate a maze
        """Draw all vertices of the maze"""
        for y in range(self.maze_obj.rows):
          for x in range(self.maze_obj.cols):
              pygame.draw.circle(self.screen, (0,0,0),
                             (x*cell_width+cell_width//2,y*cell_height+cell_height//2), 2, 0)
              pygame.display.update()
              
        """Draw the edges of the maze"""
        for k in edges: 
            pygame.draw.line(self.screen, (150,150,150), \
                (k[0][0]*cell_width+cell_width//2, k[0][1]*cell_height+cell_height//2), \
                (k[1][0]*cell_width+cell_width//2, \
                 k[1][1]*cell_height+cell_height//2),1)
            pygame.display.update()
            clock.tick(30)
         
        """Draw the walls of the maze"""
        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                if self.maze_obj.maze[(x,y)]['bellow'] == 1: # draw south wall
                  pygame.draw.line(self.screen, (0,0,0), \
                    (x*cell_width, y*cell_height + cell_height), \
                    (x*cell_width + cell_width, \
                    y*cell_height + cell_height),2)
                if self.maze_obj.maze[(x,y)]['right'] == 1: # draw east wall
                  pygame.draw.line(self.screen, (0,0,0), \
                    (x*cell_width + cell_width, y*cell_height), \
                    (x*cell_width + cell_width, y*cell_height + \
                    cell_height),2 )
                pygame.display.update()
                #clock.tick(30)
        
        """Set a end point of a game"""
        self.endpoint = pygame.image.load(self.cha_name[start_game.choose_cha]+' kiss.png')
        self.screen.blit(self.endpoint, ((width-1)*cell_width+15, \
            (height-1)*cell_height+5))
        pygame.display.update()
        
        """Screen shot a maze"""
        self.screenshot=pygame.Surface.copy(self.screen).convert()
        pygame.display.update()
                
    def reset_player(self):
        """Draw character at the begin"""
        self.surface_1 = pygame.image.load(self.cha_name[start_game.choose_cha]+' Right 1.png')
        self.surface_2 = pygame.image.load(self.cha_name[start_game.choose_cha]+' Right 2.png')
        
        """Set a start point"""
        self.cx = self.cy = 0
        self.curr_cell = self.maze_obj.maze[(self.cx, self.cy)]
        
        """Set last move"""
        self.last_move = None # For last move fun

    
    def loop(self):
        """Game loop, control character"""
        self.clock = pygame.time.Clock()
        self.keep_going = 1
        
        """When we press key"""
        while self.keep_going:
            moved = 0
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.keep_going = 0
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.keep_going = 0
                    if event.key == K_r:
                        self.reset_player()
                    if event.key == K_DOWN or event.key == K_s:
                        self.move_player('d')
                        moved = 1
                    if event.key == K_UP or event.key == K_w:
                        self.move_player('u')
                        moved = 1
                    if event.key == K_LEFT or event.key == K_a:
                        self.move_player('l')
                        moved = 1
                        self.surface_1 = pygame.image.load(self.cha_name[start_game.choose_cha]+' Left 1.png')
                        self.surface_2 = pygame.image.load(self.cha_name[start_game.choose_cha]+' Left 2.png')
                    if event.key == K_RIGHT or event.key == K_d:
                        self.move_player('r')
                        moved = 1
                        self.surface_1 = pygame.image.load(self.cha_name[start_game.choose_cha]+' Right 1.png')
                        self.surface_2 = pygame.image.load(self.cha_name[start_game.choose_cha]+' Right 2.png')
            keys = pygame.key.get_pressed()
            if not moved:
                if keys[K_DOWN]:
                    self.move_player('d')
                if keys[K_UP]:
                    self.move_player('u')
                if keys[K_LEFT]:
                    self.move_player('l')
                if keys[K_RIGHT]:
                    self.move_player('r')
            
            """Draw character after change its position"""
            self.draw_player_1()
            pygame.display.update()
            
            self.draw_player_2()
            pygame.display.update()

    def move_player(self, dir):
        """Check wall around character to know where it can go"""
        no_move = 0
        try:
          if dir == 'u':
            if not self.maze_obj.maze[(self.cx, self.cy-1)]['bellow']:
              self.cy -= 1
            else: no_move = 1
          elif dir == 'd':
            if not self.maze_obj.maze[(self.cx, self.cy)]['bellow']:
              self.cy += 1
            else: no_move = 1
          elif dir == 'l':
            if not self.maze_obj.maze[(self.cx-1, self.cy)]['right']:
              self.cx -= 1
            else: no_move = 1
          elif dir == 'r':
            if not self.maze_obj.maze[(self.cx, self.cy)]['right']:
              self.cx += 1
            else: no_move = 1
          else:
            no_move = 1
        except KeyError: # Tried to move outside screen
          no_move = 1
        
        if not no_move:
          self.last_move = dir
          self.curr_cell = self.maze_obj.maze[(self.cx, self.cy)]
        
        """Check victory"""
        if self.cx + 1 == self.maze_obj.cols and self.cy + 1 == self.maze_obj.rows:
            pygame.display.update()
            self.keep_going = 0

    def draw_player_1(self):
        """Draw character in status 1"""
        self.screen.blit(self.screenshot,(0,0))
        self.screen.blit(self.surface_1, (self.cx*cell_width+5, \
            self.cy*cell_height+5))
        pygame.display.update()
    
    def draw_player_2(self):
        """Draw character in status 2"""
        self.screen.blit(self.screenshot,(0,0))
        self.screen.blit(self.surface_2, (self.cx*cell_width+5, \
            self.cy*cell_height+5))
        pygame.display.update()
    
    def start(self):
        """Start draw the maze, get width and height base on start screen"""
        self.maze_obj= Maze(width, height)
        start_game=StartGame()
        """Generate maze and draw maze"""
        self.maze_obj.generate_maze()
        self.draw_maze()
        
        """Draw player and control it"""
        self.reset_player()
        start = time.time()
        self.loop()
        end = time.time()
        
        """Count time to know win or lose"""
        time_play=int(end-start)
        result=''
        
        if self.level_option[str(level)] == "easy":
            if time_play <= int(4):
                result='win'
            else:
                result='lose'
                
        if self.level_option[str(level)] == "normal":
            if time_play <= int(8):
                result='win'
            else:
                result='lose'
                
        if self.level_option[str(level)] == "hard":
            if time_play <= int(12):
                result='win'
            else:
                result='lose'
                
        gameDisplay = pygame.display.set_mode((800,600))
        
        if result=="win":
            gameDisplay.blit(self.load('win_screen'), (0, 0))
            pygame.display.update()
        if result == "lose":
            gameDisplay.blit(self.load('lose_screen'), (0, 0))
            pygame.display.update()
        
        """Print time player control each game"""
        print(time_play," seconds")
        
if __name__ == '__main__':
    """Run the game"""
    """Get width, height"""
    start_game=StartGame()
    start_game.begin_screen()
    width,height = start_game.width, start_game.height
    level = start_game.level
    
    g = Game(width, height, level)
    """Start game"""
    g.start()