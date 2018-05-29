from Tkinter import *
import random
import time
root = Tk()
canvas = Canvas(root, width=800, height=800)

bodx=[]
body=[]
lines = []
pocitadlo=0

def shortest_path():
    global lines
    population = create_population(poc, population_size)
    # trans_prob = 0.6
    # mutation_prob = 0.05
    has_not_changed_for = 0
    global_min = [100000000000000000,[]]
    start_time = time.time()
    for j in range(10000):
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
        if has_not_changed_for > 1000:
            break
        if j%1000==0:
            print j
        population = new_gen(population, lenghts,mutation_prob)

    print "end", global_min[0], time.time()-start_time
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
        distance += ((bodx[int(solution[i])]-bodx[int(solution[i+1])])**2 + (body[int(solution[i])] - body[int(solution[i+1])])**2)**0.5
    # print distance
    return distance


def create_population(size, population_size):
    population = []
    for i in range(population_size):
        population.append(generate_solution(size))
        # time.sleep(1)

    return population


def input_points():
    global poc, population_size, mutation_prob
    poc = int(e.get())
    mutation_prob = float(e1.get())
    population_size = int(e2.get())
    canvas.bind("<Button-1>", funkcia)
    canvas.pack()
    root.update()
    canvas.pack()


def draw_solution(solution):
    print solution
    global bodx,body, lines
    for i in range(len(solution)-1):
        lines.append(canvas.create_line(bodx[int(solution[i])], body[int(solution[i])], bodx[int(solution[i+1])], body[int(solution[i+1])]))

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
                shortest_path()
                return 0
def from_input():
    print e3.get()
    input = list(e3.get())
    print fitness(input)
    draw_solution(input)

def erase_lines():
    global lines
    for line in lines:
        canvas.delete(line)
    lines = []
topFrame = Frame(root)

button=Button(topFrame, text="Shortest path", command=input_points)
button2=Button(topFrame, text="Delete", command=vymaz)
button3=Button(topFrame, text="Draw", command=from_input)
button4=Button(topFrame, text="Erase lines", command=erase_lines)
button5=Button(topFrame, text="Restart, keep points", command=shortest_path)

e = Entry(topFrame)
e1 = Entry(topFrame)
e2 = Entry(topFrame)
e3 = Entry(topFrame)

topFrame.pack(side=LEFT)
#label1 = Label(root, text= "Name")
#label1.pack()

button.pack()
button2.pack()
button3.pack()
button4.pack()
button5.pack()


labelText=StringVar()
labelText.set("Number of towns")
labelDir=Label(topFrame, textvariable=labelText)
labelDir.pack()
e.pack()

labelText1=StringVar()
labelText1.set("Mutation Prob")
labelDir1=Label(topFrame, textvariable=labelText1)
labelDir1.pack()
e1.pack()

labelText2=StringVar()
labelText2.set("Population size")
labelDir2=Label(topFrame, textvariable=labelText2)
labelDir2.pack()
e2.pack()

labelText3=StringVar()
labelText3.set("From input")
labelDir3=Label(topFrame, textvariable=labelText3)
labelDir3.pack()
e3.pack()

canvas.pack()
root.update()
root.mainloop()
