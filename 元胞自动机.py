import time
import random
import datetime

def car_state_change(car,car_front):
    n=random.random()
    if n < p_slow:
        car[1] = max(car[1] - 1, 0)
    else:
        car[1] = min(car[1] + a, v_max,car_front[2] - car[2] -car_len - 1)
    car[2] = car[2] + car[1]
    return [car[0],car[1],car[2]]   

#车出现的概率
p = 1/3
#红灯时间
t_red = 40
#绿灯时间
t_green = 30
#随机慢化概率
p_slow = 1/10
#车长
car_len = 5
#车距
car_between = 2
#车最大速度
v_max = 10
#加速度
a=2

#init
#车流总长
car_amount = int(t_red * p)
L_all = car_amount * (car_len + car_between)

#观察点距离
L_look = v_max * 1 + car_len * 2

car_list= []
for i in range(0,car_amount):
    car_list.append([i+1,0,-1*(car_len + i*(car_len + car_between))])

count_add = 1
print(car_list)
for i in range(30):
    n=random.random()
    if n < p:
        car_list.append([car_amount+count_add,v_max,min(car_list[len(car_list) - 1][2] - v_max - 1 - car_len,-1*(L_all + L_look))])
        count_add+=1
    car_list_last = car_list
    for j in range(len(car_list)):
        if j == 0:
            car_front = [10000,0,999999]
        else:
            car_front = car_list_last[j - 1]
        car_list[j] = car_state_change(car_list_last[j],car_front)
    print(car_list)
    
    
    









