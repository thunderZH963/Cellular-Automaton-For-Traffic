# -*- coding: utf-8 -*-
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


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


def car_state_change(car,car_front):
    n=random.random()
    if n < p_slow:
        car[1] = max(car[1] - 1, 0)
    else:
        car[1] = min(car[1] + a, v_max,car_front[2] - car[2] -car_len - 1)
        if (car[1] < 0):
            car[1] = 0
    car[2] = car[2] + car[1]
    return [car[0],car[1],car[2]]

def lane_change(lane_left_last,lane_right_last):

    #从左向右变道
    left_remove = 0
    right_insert = 0
    len1= len(lane_left_last)
    i = 0
    while i < len1:
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
                lane_left_last.pop(i)
                i-=1
                len1-=1
                left_remove+=1
                lane_right_last.insert(j + 1,lane_left_last[i])
                right_insert+=1
                continue   
        i+=1
    lane_left_last = sorted(lane_left_last, key=lambda x:x[2],reverse = True)

    
    #从右向左变道
    right_remove = 0
    left_insert = 0
    i = 0
    len2 = len(lane_right_last)
    while i < len2:
        flag = 0
        for j in range(0,len(lane_left_last)- 1):
            if (lane_left_last[j + 1][2] < lane_right_last[i][2] < lane_left_last[j][2]):
                flag = 1
                break
        if (flag == 1 and i != 0):
            if (v_max > abs(lane_right_last[i - 1][2] - lane_right_last[i][2]) - car_len - 1 and lane_right_last[i - 1][2] < lane_left_last[j][2]):
                lane_right_last.pop(i)
                i-=1
                len2-=1
                right_remove+=1
                lane_left_last.insert(j + 1,lane_right_last[i])
                left_insert+=1
                continue
        i+=1

    lane_right_last = sorted(lane_right_last, key=lambda x:x[2],reverse = True)

    #随机变左道
    left_remove = 0
    right_insert = 0
    len1= len(lane_left_last)
    i = 0
    while i < len1:
        flag = 0
        for j in range(0,len(lane_right_last) - 1):
            if (lane_right_last[j + 1][2] < lane_left_last[i][2] < lane_right_last[j][2]):
                flag = 1
                break
        n=random.random()
        if (flag == 1 and n < p_change):
            #后车不会与本车碰撞
            if ((abs(lane_left_last[i][2] - lane_right_last[j + 1][2]) - car_len - 1 > lane_right_last[j + 1][1])):
                lane_left_last.pop(i)
                i-=1
                len1-=1
                left_remove+=1
                lane_right_last.insert(j + 1,lane_left_last[i])
                right_insert+=1
        
        i+=1
    lane_left_last = sorted(lane_left_last, key=lambda x:x[2],reverse = True)
        
    #随机变右道
    right_remove = 0
    left_insert = 0
    i = 0
    len2 = len(lane_right_last)
    while i < len2:
        flag = 0
        for j in range(0,len(lane_left_last)- 1):
            if (lane_left_last[j + 1][2] < lane_right_last[i][2] < lane_left_last[j][2]):
                flag = 1
                break
        n=random.random()
        if (flag == 1 and n < p_change):
            if ((abs(lane_right_last[i][2] - lane_left_last[j + 1][2]) - car_len - 1 > lane_left_last[j + 1][1])):
                lane_right_last.pop(i)
                i-=1
                len2-=1
                right_remove+=1
                lane_left_last.insert(j + 1,lane_right_last[i])
                left_insert+=1
        i+=1
    lane_right_last = sorted(lane_right_last, key=lambda x:x[2],reverse = True)

    return [lane_left_last,lane_right_last]
            

lane_left_all = []
lane_right_all = []
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
lane_left_all.append(lane_left)
lane_right_all.append(lane_right)

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
    lane_left_all.append(lane_left)
    lane_right_all.append(lane_right)

print("\n\n30s后:\n")
print("左车道：")
string_left = ""
count1 = 0
for i in range(len(lane_left)):
    if (lane_left[i][2] >= 0):
        count1+=1
    string_left = string_left + "车" + str(i + 1) + ": 速度 = " + str(lane_left[i][1]) + "m/s " + "位置 : " + str(lane_left[i][2]) + " "
print(string_left)


count2 = 0
print("\n右车道:")
string_right = ""
for i in range(len(lane_right)):
    if (lane_right[i][2] >= 0):
        count2+=1
    string_right = string_right + "车" + str(i + 1) + ": 速度 = " + str(lane_right[i][1]) + "m/s " + "位置 : " + str(lane_right[i][2]) + " "
print(string_right)

print("\n")
print("左车道通过:"+str(count1)+"辆")
print("右车道通过:"+str(count2)+"辆")
print("共通过:"+str(count1 + count2)+"辆")

font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)  

plt.title(u'左车道车辆分布图', FontProperties=font)

plt.xlabel(u'position/m')
plt.ylabel('time/s')


for i in range(0,len(lane_left_all)):
    for j in range(len(lane_left_all[i])):
        plt.scatter(lane_left_all[i][j][2],i)

plt.show()

plt.title(u'右车道车辆分布图', FontProperties=font)
plt.xlabel(u'position/m')
plt.ylabel(u'time/s')

for i in range(0,len(lane_right_all)):
    for j in range(len(lane_right_all[i])):
        plt.scatter(lane_right_all[i][j][2],i)

plt.show()
    
    
    









