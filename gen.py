from Tkinter import *
import random
import time
root = Tk()
canvas = Canvas(root, width=800, height=800)

bodx=[]
body=[]
lines = []
pocitadlo=0

def shortest_path(places):
    global lines
    population = create_population(places, 5*places)
    lenghts = []
    # trans_prob = 0.6
    mutation_prob = 0.02
    has_not_changed_for = 0
    global_min = [100000000000000000,[]]
    for j in range(200000):
        lenghts = []
        # print j
        for i in range(len(population)):
            lenghts.append([fitness(population[i]), i])
        lenghts = sorted(lenghts, key=lambda x: x[0])
        # print population[lenghts[0][1]]
        if lenghts[0][0]<global_min[0]:
            has_not_changed_for = 0
            global_min[0], global_min[1] = lenghts[0][0], population[lenghts[0][1]]
            print lenghts[0][0], population[lenghts[0][1]]
            draw_solution(population[lenghts[0][1]])
            # time.sleep(3)
            for line in lines:
                canvas.delete(line)
            lines = []
        else:
            has_not_changed_for +=1
        if has_not_changed_for > 80000:
            break
        if j%10000==0:
            print j
        population = new_gen(population, lenghts,mutation_prob)

    print "end", global_min[0]
    draw_solution(global_min[1])

    # lenghts = sorted(lenghts, key = lambda x: x[0])


def new_gen(population, lenghts, mutation_prob):
    all = []
    for par1 in lenghts:
        for par2 in lenghts:
            if par1[1] != par2[1]:
                all.append([(par1[0]+par2[0])/2, [par1[1], par2[1]]])
    all = sorted(all, key=lambda x: x[0])
    new = []
    for pair in all[0:len(population)]:
        child = mate(population[pair[1][0]],population[pair[1][1]], len(population[0]))
        new.append(mutate(child,mutation_prob))
    return new


def mate(par1, par2, solution_len):
    x = random.randint(0, (solution_len-1)/2)
    y = random.randint((solution_len-1)/2, solution_len - 2)
    x, y = min(x,y), max(x,y)
    # print x, y
    # print par1, par2
    part_1 = par1[x:y]
    # print "p1", part_1
    part_2 = []
    # nie uplne dobry sposob
    for i in range(len(par2)-1):
        is_in_1 = False
        for n in part_1:
            if n==par2[i]:
                is_in_1 = True
        if not is_in_1:
            part_2.append(par2[i])
    child = part_2[:x] + part_1 + part_2[x:]
    child.append(child[0])
    # print part_2

    # print child
    return child


def mutate(solution,mutation_prob):
    m = random.uniform(-1, 1)
    if m <= mutation_prob:
        # print "mutate"
        # print "before:", solution
        x = random.randint(0, len(solution)-2)
        y = random.randint(0, len(solution)-2)
        if x == 0:
            solution[x], solution[y] = solution[y], solution[x]
            solution[-1] = solution[y]
        else:
            if y == 0:
                solution[x], solution[y] = solution[y], solution[x]
                solution[-1] = solution[x]

        solution[x], solution[y] = solution[y], solution[x]
        # print "after:", solution
    return solution


def fitness(solution):
    distance = 0
    for i in range(0,len(solution)-1):
        distance += abs((bodx[solution[i]]-bodx[solution[i + 1]])**2 - (body[solution[i]] - body[solution[i + 1]])**2)
    # print distance
    return distance


def create_population(size, population_size):
    population = []
    for i in range(population_size):
        population.append(generate_solution(size))
        # time.sleep(1)

    return population


def input_points():
    global poc
    poc = int(e.get())
    canvas.bind("<Button-1>", funkcia)
    canvas.pack()
    root.update()
    canvas.pack()


def draw_solution(solution):
    print solution
    global bodx,body, lines
    for i in range(len(solution)-1):
        lines.append(canvas.create_line(bodx[solution[i]], body[solution[i]], bodx[solution[i+1]], body[solution[i+1]]))

    canvas.pack()
    root.update()
def generate_solution(size):
    solution = [i for i in range(size)]
    random.shuffle(solution)
    solution.append(solution[0])
    return solution


def vymaz():
    global pocitadlo, bodx, body,pole
    pocitadlo=0
    bodx=[]
    body=[]
    canvas.delete("all")


def funkcia(event):
    global pocitadlo, bodx, body
    x=event.x
    y=event.y
    if pocitadlo<poc:
        bodx.append(x)
        body.append(y)
        pocitadlo=pocitadlo+1
        if(pocitadlo==1):
            a=canvas.create_oval(x-5,y-5,x+5,y+5)
        else:
            a=canvas.create_oval(x-5,y-5,x+5,y+5)
            if(pocitadlo==poc):
                # tazisko()
                #create_population(poc,15)
                shortest_path(poc)
                return 0
def from_input():
    print e1.get()
    draw_solution(list(e1.get()))

def erase_lines():
    global lines
    for line in lines:
        canvas.delete(line)
    lines = []
topFrame = Frame(root)

button=Button(topFrame, text="Najkratsia cesta", command=input_points)
button2=Button(topFrame, text="Vymaz", command=vymaz)
button3=Button(topFrame, text="Draw", command=from_input)
button4=Button(topFrame, text="Erase lines", command=erase_lines)

e = Entry(topFrame)
e1 = Entry(topFrame)
topFrame.pack(side=LEFT)
#label1 = Label(root, text= "Name")
#label1.pack()

button.pack()
button2.pack()
button3.pack()
button4.pack()


e.pack()
e1.pack

canvas.pack()
root.update()
root.mainloop()
