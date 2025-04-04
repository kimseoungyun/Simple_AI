"""8queen logic

게임판 만들기

8자리 문자열을 이용해서 자리 표현 -> 문자열이라 인덱스 사용 가능

적합도 함수는 28 - h 이다. 이를 이용해서 이전의 적합도 함수보다 낮아지는 쪽으로 움직이도록 루프 설정.
|x변화량|=|y변화량|을 이용해서 h 결정.

돌연변이 연산도 추가해서 전역 최적화가 가능하게 한다. 대신 돌연변이 확률을 잘 정해야한다. + 임의의 0과 1 한개씩을 교첸하는 방법 사용.

2점 교차 연산도 추가한다. 적합도 함수가 가장 높은 두가지를 2점을 임의로 잡아서 교체한다.

"""
import random

POPULATION_SIZE = 4		# 개체 집단의 크기
MUTATION_RATE = 0.1			# 돌연 변이 확률
SIZE = 8				# 하나의 염색체에서 유전자 개수		
Sample_Size = 1       # 평균을 내기 위한 표본의 수

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            i = 0
            random_arr = [0, 1, 2, 3, 4, 5, 6, 7]
            while i<SIZE:
                a = random.choice(random_arr)
                self.genes.append(a)
                random_arr.remove(a)
                i += 1
    
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 0
        value = 0
        for i in range(SIZE):
            for k in range(i+1, SIZE):
                if abs(float(self.genes[i]-self.genes[k])/float(i-k))==1:
                    value += 1
        self.fitness = 28 - value
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

# 선택 연산
def select(pop):
    max_value  = sum([c.cal_fitness() for c in population])
    pick    = random.uniform(0, max_value)
    current = 0
    
    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.cal_fitness()
        print(current, pick)
        if current > pick:
            return c

# 교차 연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = random.randint(1, SIZE - 2)
    child1 = father.genes[:index] + mother.genes[index:] 
    child2 = mother.genes[:index] + father.genes[index:] 
    return (child1, child2)
    
# 돌연변이 연산
def mutate(c):
    for k in range(POPULATION_SIZE):
        if random.random() < MUTATION_RATE:
            i = 0
            random_arr = [0, 1, 2, 3, 4, 5, 6, 7]
            while i<SIZE:
                a = random.choice(random_arr)
                c.genes[i] = a
                random_arr.remove(a)
                i += 1

# 메인 프로그램
cycle = 0
Sample_Arr = []
while cycle <= Sample_Size:
    population = []
    i=0

    # 초기 염색체를 생성하여 객체 집단에 추가한다. 
    while i<POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count=0
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)

    while population[0].cal_fitness() < 28:
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
        print("세대 번호=", count)
        print_p(population)
        count += 1
        if count > 200 :break
    cycle += 1
    Sample_Arr.append(count-1)

print("최적화가 되기 위한 평균 세대 수 : ", sum(Sample_Arr)/Sample_Size, " ", Sample_Arr)