from PIL import Image
import numpy as np
from random import randint
from time import sleep

SQUARE_SIZE = 512
POPULATION_SIZE = 5
CHANGE_RANGE = 100
GENERATION_DEPTH = 1500

image_count = 0
image_list = ["images/root/cat.jpg", "images/root/harry.jpg",
              "images/root/phone.jpg", "images/root/rain.jpg",
              "images/root/sun.jpg"]

image = Image.open(image_list[image_count])
data = np.asarray(image)
H, W = image.size  # height and length of image

reference = data.copy()
solution = np.zeros((H, W, 3))

''' reference constructions
#Image.fromarray(reference).show()
print("-" * 100, solution + reference, end="\n")
print("-" * 100, reference, end="\n")

'''


def main():
  global image_count

  while image_count < len(image_list):
    choose_image()
    run()
    image_count += 1


def run():
  for start_h in range(0, H, SQUARE_SIZE):
    for start_w in range(0, W, SQUARE_SIZE):
      print(start_h, start_w)
      x = genetic( solution[start_h:start_h+SQUARE_SIZE, start_w:start_w+SQUARE_SIZE],
               reference[start_h:start_h+SQUARE_SIZE, start_w:start_w+SQUARE_SIZE])
      solution[start_h:start_h+SQUARE_SIZE, start_w:start_w+SQUARE_SIZE] = x
      Image.fromarray(np.uint8(solution)).save("images/tries/try_0/1.jpg")

def genetic(array1, array2):
  population = []
  for i in range(POPULATION_SIZE):
    current_fitness = fitness(array1, array2)
    population.append([current_fitness, array1.copy()])
  for i in range(GENERATION_DEPTH):
    for j in range(POPULATION_SIZE):
      population.append(mutation(population[j], array2))
    population = selection(population)
    print("sorted 1", [x[0] for x in population])
    print("sorted 2", [fitness(x[1], array2) for x in population])

    Image.fromarray(np.uint8(population[0][1])).save("images/tries/try_0/1.jpg")

  #print(population[0][1])
  print(population[0][0])
  return population[0][1]

def selection(population):
  population_sorted = population.copy()
  for i in range(len(population_sorted)):
    for j in range(i+1, len(population_sorted)):
      if population_sorted[i][0] < population_sorted[j][0]:
        temp = population_sorted[i].copy()
        population_sorted[i] = population_sorted[j].copy()
        population_sorted[j] = temp

  return population_sorted[0:POPULATION_SIZE]

def mutation(chromosome, ref):
  answer = chromosome.copy()[1]
  for i in range(SQUARE_SIZE):
    for j in range(SQUARE_SIZE):
      answer[i][j] = np.array([
        max(min(answer[i][j][0] + randint(-CHANGE_RANGE, CHANGE_RANGE),255), 0),
        max(min(answer[i][j][1] + randint(-CHANGE_RANGE, CHANGE_RANGE),255), 0),
        max(min(answer[i][j][2] + randint(-CHANGE_RANGE, CHANGE_RANGE),255), 0)
      ])
  return [fitness(answer, ref), answer]


def crossover(chromosome1, chromosome2):
  cut = randint(1,SQUARE_SIZE-1)
  answer1 = chromosome1[:cut] + chromosome2[cut:]
  answer2 = chromosome2[:cut] + chromosome1[cut:]
  return [answer1, answer2]


def choose_image():
  global image, data, reference, solution, image_count, H, W

  image = Image.open(image_list[image_count])
  data = np.asarray(image)
  H, W = image.size  # height and length of image

  reference = data.copy()
  solution = np.zeros((H, W, 3), dtype = "int")

def fitness(first, second):
  sum = 0
  for i in range(len(first)):
    for j in range(len(first[0])):
      sum += (first[i][j][0] - second[i][j][0]) ** 2
      sum += (first[i][j][1] - second[i][j][1]) ** 2
      sum += (first[i][j][2] - second[i][j][2]) ** 2
  print(sum)
  return 1e9/sum


main()

# a = [ [4,1] , [5, 2] , [4,5] , [5, 8] , [10, 3] , [50 ,10]]
# print(selection(a))

