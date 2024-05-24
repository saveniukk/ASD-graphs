from turtle import *
import random
import math
import copy

setup(width=1200, height=600)

n1, n2, n3, n4 = 3, 3, 2, 3
k1 = 1.0 - n3 * 0.01 - n4 * 0.01 - 0.3
k2 = 1.0 - n3 * 0.005 - n4 * 0.005 - 0.27

vertices_num = 10 + n3
circles_ps = int(vertices_num/4)
radius = 30
margin = (600/(circles_ps) - 2*radius)

directed_matrix = []
undirected_matrix = []

#словник, який зберігає координати вершин
directed_vertices_coord = {}
undirected_vertices_coord= {}

# Cловник для номерів вершин на одній стороні
vertices_on_same_side = {
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

def directed_matrix_gen(k):
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

def undirected_matrix_gen(k):
    for i in range(vertices_num):
        row = []

        for j in range(vertices_num ):
            if directed_matrix[i][j] == 1 or directed_matrix[j][i] == 1:
                row.append(1)
            else:
                row.append(0)

        undirected_matrix.append(row)
        print(row)

def get_directed_vertices_coordcenters(x, y, dict, n):
    graph_num = 1

    # Обчислення координат вершин графу
    for i in range(1, n+1, 1):
        dict[graph_num] = (x, y)
        y += margin
        graph_num += 1

    for i in range(n+1, 2*n+1, 1):
        dict[graph_num] = (x, y)
        x -= margin
        graph_num += 1

    for i in range(2*n+1, 3*n+1, 1):
        dict[graph_num] = (x, y)
        y -= margin
        graph_num += 1

    for i in range(3*n+1, 4*n+1, 1):
        dict[graph_num] = (x, y)
        x += margin
        graph_num += 1

def draw_arrow():
    directed_matrix_copied = copy.deepcopy(directed_matrix)
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
            elif directed_matrix_copied[i][j] == 1 and i != j and (i+1 in vertices_on_same_side[j+1]) and directed_matrix_copied[i][j] != directed_matrix_copied[j][i]:
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


def draw_lines():
    n = 0
    for i in range (0, vertices_num):
        for j in range (n, vertices_num ):
            #ламані
            if undirected_matrix[i][j] == 1 and i != j and (i+1 in vertices_on_same_side[j+1]):
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
            elif undirected_matrix[i][j] == 1 and i != j and i+1 not in vertices_on_same_side[j+1]:
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

def draw_graph(k):
    print('\n Matrix for directed graph: \n')
    directed_matrix_gen(k)
    get_directed_vertices_coordcenters(-60, -190, directed_vertices_coord, circles_ps)
    draw_arrow()
    draw_vertices(directed_vertices_coord)

    print('\n Matrix for undirected graph: \n')
    undirected_matrix_gen(k)
    get_directed_vertices_coordcenters(540, -190, undirected_vertices_coord, circles_ps)
    draw_lines()
    draw_vertices(undirected_vertices_coord)

##########  L   A   B   A   -----    4  ##########################################################

def first_part_of_the_lab():
    draw_graph(k1)

    directed_vertices_degrees = {}
    undirected_vertices_degrees = {}

    print('\n Степені вершин напрямленого графу: \n')
    for i in range(vertices_num):
        out_degree = directed_matrix[i].count(1)
        in_degree = 0

        # Напівстепінь виходу
        for j in range(vertices_num):
            if directed_matrix[j][i] == 1:
                in_degree += 1

    
        total_degree = out_degree + in_degree
        directed_vertices_degrees[i+1] = total_degree

        print(f"Степінь вершини {i+1}: {total_degree} (напівстепінь виходу {out_degree}, напівстепінь входу: {in_degree})")

    if all(value == list(directed_vertices_degrees.values())[0] for value in directed_vertices_degrees.values()):
        print(f">>>> Граф однорідний, степінь однорідності: {total_degree}")
    else:
        print(">>>> Граф неоднорідний")

    for key, value in directed_vertices_degrees.items():
        if value == 1:
            print(f'>>>> Вершина {key} висяча')

        if value == 0:
            print(f'>>>> Вершина {key} ізольована')

    print('\n Степені вершин ненапрямленого графу: \n')

    # Степені вершин ненапрямленого графа
    for i in range(vertices_num):
        degree = 0
        for j in range(vertices_num):
            if undirected_matrix[i][j] == 1 and i != j:
                degree += 1

            elif undirected_matrix[i][j] == 1 and i == j:
                degree += 2

        undirected_vertices_degrees[i+1] = degree
        print(f"Степінь вершини {i+1}: {degree}")

    if all(value == list(undirected_vertices_degrees.values())[0] for value in undirected_vertices_degrees.values()):
        print(f">>>> Граф однорідний, степінь однорідності: {degree}")
    else:
        print(">>>> Граф неоднорідний")

    for key, value in undirected_vertices_degrees.items():
        if value == 1:
            print(f'>>>> Вершина {key} висяча')

        if value == 0:
            print(f'>>>> Вершина {key} ізольована')

def second_part_of_the_lab():
    print('\n Matrix for directed graph: \n')
    directed_matrix_gen(k2)


    setup(width=1200, height=600)
    get_directed_vertices_coordcenters(-60, -190, directed_vertices_coord, circles_ps)
    draw_arrow()
    draw_vertices(directed_vertices_coord)

    #Півстепені вершин графу
    print('\n Степені орграфу: \n')
    for i in range(vertices_num):
        out_degree = directed_matrix[i].count(1)
        in_degree = 0

        for j in range(vertices_num):
            if directed_matrix[j][i] == 1:
                in_degree += 1

        print(f"напівстепінь виходу {out_degree}, напівстепінь входу: {in_degree}")

    def matrix_multiplication (matrix_1, matrix_2):
        result = []
        for i in range(vertices_num):
            row = []
            for j in range(vertices_num):
                value = 0
                for k in range(vertices_num):
                    value += matrix_1[i][k] * matrix_2[k][j]
                row.append(value)
            result.append(row)

        return result

    matrix_pow2 = matrix_multiplication (directed_matrix, directed_matrix)
    matrix_pow3 = matrix_multiplication (matrix_pow2, directed_matrix)

    #Усі шляхи довжиною 2 та 3
    print('\nУсі шляхи довжиною 2:')
    for i in range(vertices_num):
        for j in range(vertices_num):
            if matrix_pow2[i][j] > 0:
                # Вивести шлях (i, j) разом із проміжними вершинами
                print(f"Шлях від вершини {i+1} до вершини {j+1}:")
                for k in range(vertices_num):
                    if directed_matrix[i][k] == 1 and directed_matrix[k][j] == 1:
                        print(f"{i+1} -> {k+1} -> {j+1}")

    # Виведення усіх шляхів довжиною 3
    print("\n Усі шляхи довжиною 3:")
    for i in range(vertices_num):
        for j in range(vertices_num):
            if matrix_pow3[i][j] > 0:
                # Вивести шлях (i, j) разом із проміжними вершинами
                print(f"Шлях від вершини {i+1} до вершини {j+1}:")
                for k in range(vertices_num):
                    if directed_matrix[i][k] == 1:
                        for l in range(vertices_num):
                            if directed_matrix[k][l] == 1 and directed_matrix[l][j] == 1:
                                print(f"{i+1} -> {k+1} -> {l+1} -> {j+1}")

    #Матриця досяжності
    def identity_matrix(size):
        matrix = [[0] * size for _ in range(size)]

        for i in range(size):
            matrix[i][i] = 1
    
        return matrix
    
    def zero_matrix(size):
        matrix = [[0] * size for _ in range(size)]
        return matrix

    matrix_pow4 = matrix_multiplication(matrix_pow3, directed_matrix)
    matrix_pow5 = matrix_multiplication(matrix_pow4, directed_matrix)
    matrix_pow6 = matrix_multiplication(matrix_pow5, directed_matrix)
    matrix_pow7 = matrix_multiplication(matrix_pow6, directed_matrix)
    matrix_pow8 = matrix_multiplication(matrix_pow7, directed_matrix)
    matrix_pow9 = matrix_multiplication(matrix_pow8, directed_matrix)
    matrix_pow10 = matrix_multiplication(matrix_pow9, directed_matrix)
    matrix_pow11 = matrix_multiplication(matrix_pow10, directed_matrix)

    matrices = [
        identity_matrix(vertices_num), directed_matrix, matrix_pow2,
        matrix_pow3, matrix_pow5, matrix_pow6,
        matrix_pow7, matrix_pow8, matrix_pow9,
        matrix_pow10, matrix_pow11,
    ]

    def sum_matrix():
        result = zero_matrix(vertices_num)
        for matrix in matrices:
            for i in range(vertices_num):
                for j in range(vertices_num):
                    result[i][j] += matrix[i][j]

        return result
    
    matrices_sum = sum_matrix()

    def get_reachability_matrix():
        result = []
        print('\nМатриця досяжності: ')
        for i in range (vertices_num):
            row = []
            for j in range (vertices_num):
                if matrices_sum[i][j] == 0: 
                    row.append(0)
                else: row.append(1)
            print(row)
            result.append(row)
        return result
        
    reachable_matrix = get_reachability_matrix()

    #Матриця сильної зв'язності

    def transpose_matrix(matrix):
        transposed_matrix = [[0 for _ in range(vertices_num)] for _ in range(vertices_num)]

        for i in range(vertices_num):
            for j in range(vertices_num):
                transposed_matrix[j][i] = matrix[i][j]

        return transposed_matrix
    
    transposed_matrix = transpose_matrix(reachable_matrix)

    def elementwise_matrix_multiply(matrix1, matrix2):
        print("\nМатриця сильної зв'яності: ")
        result = []
        for i in range(len(matrix1)):
            row = []
            for j in range(len(matrix1[0])):
                row.append(matrix1[i][j] * matrix2[i][j])
            result.append(row)
            print(row)
        return result
    
    strong_connectivity_matrix = elementwise_matrix_multiply(reachable_matrix, transposed_matrix)

    def find_strong_components (matrix):
        matrix_dict = {}
        components_arr = []
        for i, arr in enumerate(matrix):
            array_key = tuple(arr)
            if array_key in matrix_dict:
                matrix_dict[array_key].append(i+1)
            else:
                matrix_dict[array_key] = [i+1]

        for value in matrix_dict.values():
            components_arr.append(value)
            print("компонента:", value)

        return components_arr

    print("\nКомпоненти сильної зв'язності: ")
    strong_components = find_strong_components(strong_connectivity_matrix)

    # Граф конденсації
    def build_condensation_graph(reachable_matrix, strong_components):
        num_components = len(strong_components)
        condensation_graph = [[0] * num_components for _ in range(num_components)]

        for i in range(num_components):
            for j in range(num_components):
                if i != j:
                    for node_i in strong_components[i]:
                        for node_j in strong_components[j]:
                            if directed_matrix[node_i - 1][node_j - 1] == 1:
                                condensation_graph[i][j] = 1
                                break

        return condensation_graph

    def condensation_graph_draw():
        c_vertices_num = len(strong_components)
        circles_count = int(c_vertices_num/4)
        radius = 30
        margin = (600/(circles_count) - 6*radius)
        c_vertices_coord = {}
        condensation_matrix = build_condensation_graph(reachable_matrix, strong_components)

        def get_vertices_centers(x, y, dict, n):
            graph_num = 1

            # Обчислення координат вершин графу
            for i in range(1, n+1, 1):
                dict[graph_num] = (x, y)
                y += margin
                graph_num += 1

            for i in range(n+1, 2*n+1, 1):
                dict[graph_num] = (x, y)
                x -= margin
                graph_num += 1

            for i in range(2*n+1, 3*n+1, 1):
                dict[graph_num] = (x, y)
                y -= margin
                graph_num += 1

            for i in range(3*n+1, 4*n+1, 1):
                dict[graph_num] = (x, y)
                x += margin
                graph_num += 1

        def draw_arrows():
            for i in range(c_vertices_num):
                for j in range(c_vertices_num):
                    if (condensation_matrix[i][j] == 1):
                        start_x, start_y = float(c_vertices_coord[i + 1][0]), float(c_vertices_coord[i + 1][1])
                        end_x, end_y = float(c_vertices_coord[j + 1][0]), float(c_vertices_coord[j + 1][1])
                        arrow(start_x, start_y, end_x, end_y)

        get_vertices_centers(540, -190, c_vertices_coord, circles_count)
        draw_arrows()
        draw_vertices(c_vertices_coord)

    condensation_graph_draw ()


speed(0)

print('Який граф малюємо? Введіть цифру: \n 1. Напрямлений та ненапрямлений графи з першої частини \n 2. Орграф з другої частини лаби та граф конденсації')
answer = input(" ")

if answer == '1': first_part_of_the_lab()
elif answer == '2': second_part_of_the_lab()

done()
