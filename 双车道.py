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

def lane_change(lane_left,lane_right):
    lane_left_last = []
    lane_right_last = []
    for i in range(len(lane_left)):
        lane_left_last.append(lane_left[i])
    for i in range(len(lane_right)):
        lane_right_last.append(lane_right[i])

    #从左向右变道
    left_remove = 0
    right_insert = 0
    for i in range(len(lane_left_last)):
        flag = 0
        #找到右边合适的两车道
        #flag代表找到
        #左边i车介于右边j和j+1车之间
        for j in range(0,len(lane_right_last) - 1):
            if (lane_right_last[j + 1][2] < lane_left_last[i][2] < lane_right_last[j][2]):
                flag = 1
                break
        
        if (flag == 1 and i!= 0):
            gap_left = abs(lane_left_last[i - 1][2] - lane_left_last[i][2]) - car_len - 1
            #if v_max > gap_left and gap_right > gap_left
            if (v_max >  gap_left and lane_left_last[i - 1][2] < lane_right_last[j][2]):
                lane_left.pop(i-left_remove)
                left_remove+=1
                lane_right.insert(j + 1 + right_insert,lane_left_last[i])
                right_insert+=1
                continue
    lane_left_last = sorted(lane_left_last, key=lambda x:x[2],reverse = True)
        #左车随机变道
        n=random.random()
        if (flag == 1 and n < p_change):
            #后车不会与本车碰撞
            if ((abs(lane_left_last[i][2] - lane_right_last[j + 1][2]) - car_len - 1 > lane_right_last[j + 1][1])):
                lane_left.pop(i-left_remove)
                left_remove+=1
                lane_right.insert(j + 1 + right_insert,lane_left_last[i])
                right_insert+=1
                

    right_remove = 0
    left_insert = 0
    for i in range(len(lane_right_last)):
        flag = 0
        for j in range(0,len(lane_left_last)- 1):
            if (lane_left_last[j + 1][2] < lane_right_last[i][2] < lane_left_last[j][2]):
                flag = 1
                break
        if (flag == 1 and i != 0):
            if (v_max > abs(lane_right_last[i - 1][2] - lane_right_last[i][2]) - car_len - 1 and lane_right_last[i - 1][2] < lane_left_last[j][2]):
                lane_right.pop(i + right_insert - right_remove)
                right_remove+=1
                lane_left.insert(j + 1 - left_remove + left_insert,lane_right_last[i])
                left_insert+=1
                continue
        n=random.random()
        if (flag == 1 and n < p_change):
            if ((abs(lane_right_last[i][2] - lane_left_last[j + 1][2]) - car_len - 1 > lane_left_last[j + 1][1])):
                lane_right.pop(i + right_insert - right_remove)
                right_remove+=1
                lane_left.insert(j + 1 - left_remove + left_insert,lane_right_last[i])
                left_insert+=1
    return [lane_left,lane_right]
            

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
#随机变道概率
p_change = 1/4

#init
#车流总长
car_amount = int(t_red * p)
L_all = car_amount * (car_len + car_between)

#观察点距离
L_look = v_max * 1 + car_len * 2

lane_left = []
lane_right = []
for i in range(0,car_amount):
    lane_left.append([str(i+1)+"left",0,-1*(car_len + i*(car_len + car_between))])
    lane_right.append([str(i+1)+"right",0,-1*(car_len + i*(car_len + car_between))])

count_left = 1
count_right = 1
print('left:--------------------------------------------------------------')
print(lane_left)
print('right:--------------------------------------------------------------')
print(lane_right)

for i in range(30):
    lane_left,lane_right = lane_change(lane_left,lane_right)
    n=random.random()
    if n < p:
        lane_left.append([str(car_amount+count_left) + "left",v_max,min(lane_left[len(lane_left) - 1][2] - v_max - 1 - car_len,-1*(L_all + L_look))])
        count_left+=1
    n=random.random()
    if n < p:
        lane_right.append([str(car_amount+count_right) + "right",v_max,min(lane_right[len(lane_right) - 1][2] - v_max - 1 - car_len,-1*(L_all + L_look))])
        count_right+=1
    lane_left_last = lane_left
    for j in range(len(lane_left)):
        if j == 0:
            car_front = [10000,0,999999]
        else:
            car_front = lane_left[j - 1]
        lane_left[j] = car_state_change(lane_left_last[j],car_front)
        
    lane_right_last = lane_right
    for j in range(len(lane_right)):
        if j == 0:
            car_front = [10000,0,999999]
        else:
            car_front = lane_right[j - 1]
        lane_right[j] = car_state_change(lane_right_last[j],car_front)
    print('left:--------------------------------------------------------------')
    print(lane_left)
    print('right:--------------------------------------------------------------')
    print(lane_right)
    
    
    









