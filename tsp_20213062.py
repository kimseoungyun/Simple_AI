import random
import matplotlib.pyplot as plt

POPULATION_SIZE = 100	# 개체 집단의 크기
MUTATION_RATE = 0.1		# 돌연 변이 확률
SIZE = 8				# 하나의 염색체에서 유전자 개수		
Sample_Size =1
cost_data = [
            [0,30,140,75,168,237,303,325,268],
            [30,0,140,105,198,247,315,334,257],
            [140,140,0,173,205,119,190,200,141],
            [75,105,173,0,102,238,293,323,313],
            [168,198,205,102,0,213,247,287,340],
            [237,247,119,238,213,0,71,88,173],
            [303,315,190,293,247,71,0,44,222],
            [325,334,200,323,287,88,44,0,202],
            [268,257,141,313,340,173,222,202,0]] # 도시간 이동 거리

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            i = 0
            random_arr = list(range(1, SIZE+1))
            while i<SIZE:
                a = random.choice(random_arr)
                self.genes.append(a)
                random_arr.remove(a)
                i += 1
    
    
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 0
        value = 0            
        last_city = 1
        for current_city in self.genes:
            value += cost_data[last_city][current_city]
            last_city = current_city 
        value += cost_data[last_city][1]
        self.fitness = 10000-value
        return self.fitness

    def __str__(self):
        return self.genes.__str__()

# 염색체와 적합도를 출력한다. 
def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", x, "적합도=", x.cal_fitness())
        i += 1
    print("")





# function1 선택 연산
def select(pop):
    max_value  = sum([c.cal_fitness() for c in population])
    pick    = random.uniform(0, max_value)
    current = 0
    
    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c

# function2 교차 연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    # 더미 인덱스 설정
    index = random.randint(0, SIZE - 4)

    # 인덱스 크기에 들어가지 않는 숫자들을 배열로 생성
    arr1 = []
    arr2 = []
    for _ in mother.genes:
        if _ not in father.genes[index:index+3]:
            arr2.append(_)
    
    for _ in father.genes:
        if _ not in mother.genes[index:index+3]:
            arr1.append(_)    

    # 인덱스 크기만큼 교체 
    father.genes[index:index+3], mother.genes[index:index+3] = mother.genes[index:index+3], father.genes[index:index+3]

    # 나머지 채우기
    father.genes[:index] = arr1[:index]
    father.genes[index+3:] = arr1[index:]
    mother.genes[:index] = arr2[:index]
    mother.genes[index+3:] = arr2[index:]

    # 유전
    child1 = father.genes
    child2 = mother.genes
    return (child1, child2)
    


# function3 돌연변이 연산
def mutate(c):
    if random.random() < MUTATION_RATE:
        a, b = random.sample(range(SIZE), k=2)
        c.genes[a], c.genes[b] = c.genes[b], c.genes[a]




# 메인 프로그램
population = []
i=0

# 초기 염색체를 생성하여 객체 집단에 추가한다. 
cycle = 0
Sample_Arr = []
arr = []
arr_x = []
arr_y = []
while cycle <= Sample_Size:
    population = []
    i=0

    # 초기 염색체를 생성하여 객체 집단에 추가한다. 
    while i<POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count=0
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    if population[0].cal_fitness() > 8950:
        arr.append(population[0].cal_fitness())
    arr_x.append(count)
    arr_y.append(population[0].cal_fitness())
    print("세대 번호=", count)
    print_p(population)
    count +=1

    # population[0].cal_fitness() < 28
    while 1:
        new_pop = []

        # 선택과 교차 연산
        for _ in range(POPULATION_SIZE//2):
            c1, c2 = crossover(population);
            new_pop.append(Chromosome(c1));
            new_pop.append(Chromosome(c2));

        # 자식 세대가 부모 세대를 대체한다. 

        # 깊은 복사를 수행한다. 
        population = new_pop.copy();    
        
        # 돌연변이 연산
        for c in population: mutate(c)

        # 출력을 위한 정렬
        population.sort(key=lambda x: x.cal_fitness(), reverse=True)
        if population[0].cal_fitness() > 8950:
            arr.append(population[0].cal_fitness())
        arr_x.append(count)
        arr_y.append(population[0].cal_fitness())
        print("세대 번호=", count)
        print_p(population)
        count += 1
        if count > 500 :break
    cycle += 1
    Sample_Arr.append(count-1)

print("최적화가 되기 위한 평균 세대 수 : ", sum(Sample_Arr)/Sample_Size)
print("최적화 값", arr)
plt.plot(arr_x, arr_y, 'ro')
# 3 4 5 6 7 8 2 1 9