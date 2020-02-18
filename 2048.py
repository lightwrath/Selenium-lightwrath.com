from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCon
from selenium.webdriver.common.by import By

import time

driver = webdriver.Firefox(executable_path="/mnt/RAID/personal/Code/Selenium/geckodriver")

def launch():
   driver.get('https://2048game.com/')
   time.sleep(5)

def getGridData():
   
   #init array 4x4 grid
   grid = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
   for y in range(4):
      for x in range(4):
         cssGridPos = ".tile-position-{}-{}".format(x+1, y+1)
         try:
            gridTmpLocation = driver.find_element_by_css_selector(cssGridPos)
            try:
               cssGridMerge = cssGridPos + ".tile-merged"
               gridMergeLocation = driver.find_element_by_css_selector(cssGridMerge)
               grid[y][x] = gridMergeLocation.text
            except:
               grid[y][x] = gridTmpLocation.text
         except: 
            grid[y][x] = 0

   for a in range(4):
      grid[a] = list(map(int, grid[a]))
      grid[a] = tuple(grid[a])
   grid = tuple(grid)
   return grid

def lineCalc(line):
   lineScore = 0
   for a in range(line.count(0)):
      line.remove(0)
   for b in range(len(line) - 1):
      if line[b] == line[b + 1]:
         lineScore = lineScore + line[b] + line[b + 1]
   return lineScore

def rowCalc(grid):
   rowScore = 0
   for a in range(4):
      line = list(grid[a])
      rowScore = rowScore + lineCalc(line)
   
   return rowScore

def colCalc(grid):
   colScore = 0
   line = []
   for a in range(4):
      for b in range(4):
         line.append(grid[b][a])
      colScore = colScore + lineCalc(line)
      line.clear()
   
   return colScore

def calcMove(grid):
   #gameWindow = driver.find_element_by_tag_name('body')
   rowScore = rowCalc(grid)
   colScore = colCalc(grid)
   print("Right score is: ", rowScore, " - Up score is: ", colScore)
   if rowScore > colScore:
      return "right"
   if colScore > rowScore:
      return "up"
   else: 
      return False

def gridChangeCheck(oldGrid, newGrid):
   gridSumOld = 0
   gridSumNew = 0
   for a in range(4):
      for b in range(4):
         gridSumOld = gridSumOld + oldGrid[a][b]
   newGrid = getGridData()
   for a in range(4):
      for b in range(4):
         gridSumNew = gridSumNew + newGrid[a][b]
   if gridSumOld != gridSumNew:
      return True
   else: 
      return False

def stuckMove(attempt):
   gameWindow = driver.find_element_by_tag_name('body')
   if attempt == 0:
      print("Stuck, Sending Up")
      gameWindow.send_keys(Keys.ARROW_UP)
   if attempt == 1:
      print("Stuck, Sending Right")
      gameWindow.send_keys(Keys.ARROW_RIGHT)
   if attempt == 2:
      print("Stuck, Sending Left")
      gameWindow.send_keys(Keys.ARROW_LEFT)
   if attempt == 3:
      print("Stuck, Sending Down") 
      gameWindow.send_keys(Keys.ARROW_DOWN)
   time.sleep(1)

def gameRestart():
   tryAgain = driver.find_element_by_css_selector(".game-message")
   if tryAgain.is_displayed():
      retryBtn = driver.find_element_by_css_selector(".retry-button")
      retryBtn.click()
      time.sleep(5)
      print("Whoops!")

#MAIN
launch()
gridDataOld = getGridData()
while True:
   gridData = getGridData()
   print(" ", gridData[0], "\n", gridData[1], "\n", gridData[2], "\n", gridData[3])
   for attempt in range(4):
      if gridChangeCheck(gridDataOld, gridData) == True:
         break
      else: 
         stuckMove(attempt)
   moveResult = calcMove(gridData)
   if moveResult == "up":
      gameWindow = driver.find_element_by_tag_name('body')
      print("Sending Up")
      gameWindow.send_keys(Keys.ARROW_UP)
      time.sleep(1)
   if moveResult == "right":
      gameWindow = driver.find_element_by_tag_name('body')
      print("Sending Right")
      gameWindow.send_keys(Keys.ARROW_RIGHT)
      time.sleep(1)
   gridDataOld = gridData
   del gridData
   gameRestart()




#grid11 = driver.find_element_by_css_selector('.tile-position-1-1 div')
#grid11Content = grid11.text
#print(grid11Content)