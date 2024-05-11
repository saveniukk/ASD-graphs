from turtle import *
import random
import math

setup(width=1200, height=600)
n1, n2, n3, n4 = 3, 3, 2, 3

vertices_num = 10 + n3
k = 1.0 - n3 * 0.02 - n4 * 0.005 - 0.25
circles_ps = int(vertices_num/4)
radius = 30
margin = (600/(circles_ps) - 2*radius)

directed_matrix = []
undirected_matrix = []

#словник, який зберігає координати вершин
directed_vertices_coord = {}
undirected_vertices_coord= {}

# Cловник для номерів вершин на одній стороні, але не суміжні
directed_vertices_coordon_same_side = {
    1 : [3, 4, 10, 11],
    2 : [4],
    3 : [1],
    4 : [1, 2, 6, 7],
    5 : [7],
    6 : [4],
    7 : [5, 4, 9, 10],
    8 : [10],
    9 : [7],
    10 : [7, 8, 12, 1],
    11 : [1],
    12 : [10]
}

#генерація матриці для напрямленого графа
def directed_matrix_gen():
    random.seed(3323)
    for i in range(vertices_num ):
        row = []

        for j in range(vertices_num):
            random_number = random.uniform(0, 2.0)
            element = random_number*k

            if (element < 1.0): element = 0
            else: element = 1

            row.append(element)
        directed_matrix.append(row)
        print(row)

def undirected_matrix_gen():
    for i in range(vertices_num):
        row = []

        for j in range(vertices_num ):
            if directed_matrix[i][j] == 1 or directed_matrix[j][i] == 1:
                row.append(1)
            else:
                row.append(0)

        undirected_matrix.append(row)
        print(row)

def get_directed_vertices_coordcenters(x, y, dict):
    # Лічильник вершин
    graph_num = 1

    # Обчислення координат вершин графу
    for i in range(1, circles_ps+1, 1):
        dict[graph_num] = (x, y)
        y += margin
        graph_num += 1

    for i in range(circles_ps+1, 2*circles_ps+1, 1):
        dict[graph_num] = (x, y)
        x -= margin
        graph_num += 1

    for i in range(2*circles_ps+1, 3*circles_ps+1, 1):
        dict[graph_num] = (x, y)
        y -= margin
        graph_num += 1

    for i in range(3*circles_ps+1, 4*circles_ps+1, 1):
        dict[graph_num] = (x, y)
        x += margin
        graph_num += 1

#малюємо стрілочки напрямлених графів
def draw_arrow():
    directed_matrix_copied = directed_matrix.copy()
    for i in range (0, vertices_num):
        for j in range (0, vertices_num):
            #подвійні стрілки
            if directed_matrix_copied[i][j] == directed_matrix_copied[j][i] == 1 and i != j:
                start_x, start_y = float(directed_vertices_coord[j + 1][0]), float(directed_vertices_coord[j + 1][1] + 5)
                end_x, end_y = float(directed_vertices_coord[i + 1][0]), float(directed_vertices_coord[i + 1][1] + 5)
                arrow(start_x, start_y, end_x, end_y)

                start_x, start_y = float(directed_vertices_coord[i + 1][0]), float(directed_vertices_coord[i + 1][1] - 5)
                end_x, end_y = float(directed_vertices_coord[j + 1][0]), float(directed_vertices_coord [j + 1][1] - 5)
                arrow(start_x, start_y, end_x, end_y)

                directed_matrix_copied[j][i] = 0

            #Ламані, для тих стрілок, які знаходяться на одній стороні квадрата
            elif directed_matrix_copied[i][j] == 1 and i != j and (i+1 in directed_vertices_coordon_same_side[j+1]) and directed_matrix_copied[i][j] != directed_matrix_copied[j][i]:
                start_x, start_y = float(directed_vertices_coord[i + 1][0]), float(directed_vertices_coord[i + 1][1])
                end_x, end_y = float(directed_vertices_coord[j + 1][0]), float(directed_vertices_coord[j + 1][1])
                if(j <= circles_ps): midle_x, midle_y = (start_x + end_x)/2 + 2*radius, (start_y + end_y)/2 - 4*radius
                if(circles_ps <= j <= circles_ps*2): midle_x, midle_y = (start_x + end_x)/2 - radius, (start_y+end_y)/2 + radius + 10
                if(circles_ps*2 <= j <= circles_ps*3): midle_x, midle_y = (start_x + end_x)/2 - radius-10, (start_y+end_y)/2 + radius
                if(circles_ps*3 <= j <= circles_ps*4): midle_x, midle_y = (start_x + end_x)/2 + radius - radius, (start_y+end_y)/2 - radius - 10
                penup()
                goto(start_x, start_y)
                pendown()
                goto(midle_x, midle_y)
                arrow(midle_x, midle_y, end_x, end_y)

            # Малювання петлі для самонапрямленого графа
            elif directed_matrix_copied[i][j] == 1 and i == j:
                penup()
                setheading(0)
                goto(directed_vertices_coord[i + 1][0]+10, directed_vertices_coord[i + 1][1]+radius-5)

                pendown()
                circle(10, 240)
                arrow_length = 15
                arrow_head_width = 10

                # Малювання arrowhead
                begin_fill()
                forward(arrow_length)
                right(120)
                forward(arrow_head_width)
                right(120)
                forward(arrow_head_width)
                end_fill()

            #Малювання звичайних стрілочок
            elif directed_matrix_copied[i][j] == 1 and i != j and directed_matrix_copied[i][j] != directed_matrix_copied[j][i]:
                start_x, start_y = float(directed_vertices_coord[i + 1][0]), float(directed_vertices_coord[i + 1][1])
                end_x, end_y = float(directed_vertices_coord[j + 1][0]), float(directed_vertices_coord[j + 1][1])
                arrow(start_x, start_y, end_x, end_y)

#Малювання ребер ненапрямленого графа
def draw_lines():
    n = 0
    for i in range (0, vertices_num):
        for j in range (n, vertices_num ):
            #ламані
            if undirected_matrix[i][j] == 1 and i != j and (i+1 in directed_vertices_coordon_same_side[j+1]):
                start_x, start_y = float(undirected_vertices_coord[i + 1][0]), float(undirected_vertices_coord[i + 1][1])
                end_x, end_y = float(undirected_vertices_coord[j + 1][0]), float(undirected_vertices_coord[j + 1][1])
                if(i <= circles_ps): midle_x, midle_y = (start_x + end_x)/2 + 2*radius, (start_y + end_y)/2 - radius-20
                if(circles_ps <= i <= circles_ps*2): midle_x, midle_y = (start_x + end_x)/2 + radius, (start_y+end_y)/2 + radius + 20
                if(circles_ps*2 <= i <= circles_ps*3): midle_x, midle_y = (start_x + end_x)/2 - radius-20, (start_y+end_y)/2 + radius
                if(circles_ps*3 <= i <= circles_ps*4): midle_x, midle_y = (start_x + end_x)/2 + radius - radius, (start_y+end_y)/2 - radius - 20
                penup()
                goto(start_x, start_y)
                pendown()
                goto(midle_x, midle_y)
                goto(end_x, end_y)
            #петлі
            elif undirected_matrix[i][j] == 1 and i == j:
                penup()
                setheading(0)
                goto(undirected_vertices_coord[i + 1][0]+10, undirected_vertices_coord[i + 1][1]+radius-10)

                pendown()
                circle(10, 360)

            #прямі
            elif undirected_matrix[i][j] == 1 and i != j and i+1 not in directed_vertices_coordon_same_side[j+1]:
                start_x, start_y = float(undirected_vertices_coord[i + 1][0]), float(undirected_vertices_coord[i + 1][1])
                end_x, end_y = float(undirected_vertices_coord[j + 1][0]), float(undirected_vertices_coord[j + 1][1])
                penup()
                goto(start_x, start_y)
                pendown()
                goto(end_x, end_y)
        n+=1
    
def draw_vertices(dict):
    i = 1
    for vertex, (x, y) in dict.items():
        penup()
        goto(x, y-radius)
        pendown()
        setheading(0)
        fillcolor("red")
        begin_fill()
        circle(radius)
        end_fill()
        penup()
        goto(x-3, y-10)
        write(i,  font=("Arial", 16, "normal"))
        i += 1
        
def arrow(start_x, start_y, end_x, end_y):
  # Лінія від центру до центру
  penup()
  goto(start_x, start_y)
  pendown()
  goto(end_x, end_y)

  # Повернення черепашки назад
  penup()
  distance_back = radius
  new_end_x = end_x - (distance_back * (end_x - start_x)) / math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
  new_end_y = end_y - (distance_back * (end_y - start_y)) / math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
  goto(new_end_x, new_end_y)
  pendown()

  angle = math.atan2(end_y - start_y, end_x - start_x)
  arrow_length = 15
  arrow_head_width = 10

  # Малювання arrowhead
  begin_fill()
  setheading(math.degrees(angle)-150)
  forward(arrow_length)
  right(120)
  forward(arrow_head_width)
  right(120)
  forward(arrow_head_width)
  end_fill()

def draw_graph():
    print('\n Matrix for directed graph: \n')
    directed_matrix_gen()
    get_directed_vertices_coordcenters(-60, -190, directed_vertices_coord)
    draw_arrow()
    draw_vertices(directed_vertices_coord)

def draw_undirected_graph():
    print('\n Matrix for undirected graph: \n')
    undirected_matrix_gen()
    get_directed_vertices_coordcenters(540, -190, undirected_vertices_coord)
    draw_lines()
    draw_vertices(undirected_vertices_coord)

speed(100)
draw_graph()
draw_undirected_graph()
done()
