'''
 N : 도시의 한 변의 길이 (10 ≤ N ≤ 10,000)
 M : 택시의 개수 (100 ≤ M ≤ 2,000)
 L : 택시가 호출을 받을 수 있는 최대 거리 (L = N / 10)
 mXs : 택시의 x축 위치들 (0 ≤ mXs[] ≤ N – 1)
 mYs : 택시의 y축 위치들 (0 ≤ mYs[] ≤ N – 1)
'''

#####solution.py
from typing import List
import heapq
taxi = 0
all_taxi = []
city = 0
length = 0


class Result:
    def __init__(self, mX, mY, mMoveDistance, mRideDistance):
        self.mX = mX
        self.mY = mY
        self.mMoveDistance = mMoveDistance
        self.mRideDistance = mRideDistance

def init(N : int, M : int, L : int, mXs : List[int], mYs : List[int]):
    global taxi, city, length, all_taxi
    taxi = M
    city = N
    length = L
    all_taxi = [[0, 0, 0, 0, 2001]] * (taxi+1)
    for i in range(1, taxi + 1):
        all_taxi[i] = [mXs[i-1], mYs[i-1], 0, 0, i, 0]


def pickup(mSX : int, mSY : int, mEX : int, mEY : int):
    # 출발지는 (mSX, mSY)이고 목적지는 (mEX, mEY)
    min_dist = length
    can_pickup = []
    # print(all_taxi)
    # 최대 호출 거리
    for idx, taxi in enumerate(all_taxi):
        if idx == 0:
            continue
        dist = abs(taxi[0] - mSX) + abs(taxi[1] - mSY)
        if dist <= min_dist:
            total_dist = abs(mSX - mEX) + abs(mSY - mEY)
            all_dist = dist + total_dist
            can_pickup.append([dist, idx, all_dist, total_dist])
    if can_pickup:
        sorted_pickup = min(can_pickup, key=lambda x:(x[0],x[1]))
        taxi_num = sorted_pickup[1]
        all_taxi[taxi_num][0] = mEX
        all_taxi[taxi_num][1] = mEY
        all_taxi[taxi_num][2] += sorted_pickup[1]
        all_taxi[taxi_num][3] += sorted_pickup[3]
        all_taxi[taxi_num][5] += sorted_pickup[2]
        # print(f"dist : {dist} 손님 : {total_dist} 전체이동 : {all_dist}")
        # print(f"pickup : {taxi_num}")
        return taxi_num
    # print('pickup : -1')
    return -1

def reset(mNo : int):
    a = all_taxi[mNo][0]
    b = all_taxi[mNo][1]
    c = all_taxi[mNo][5]
    d = all_taxi[mNo][3]

    all_taxi[mNo][3] = 0
    all_taxi[mNo][5] = 0
    # print(f"reset : {a, b, c, d}")
    return Result(a, b, c, d)


def getBest(mNos: List[int]):
    # heapq.nsmallest를 사용해 정렬 기준(key)에 맞는 상위 5개의 택시만 효율적으로 추출
    # 전체 리스트를 정렬하지 않으므로 시간 복잡도가 개선됨
    best_5_taxis = heapq.nsmallest(5, all_taxi, key = lambda x: (-x[3], x[4]))

    # 결과 리스트 mNos에 택시 번호(x[4])를 할당
    for i in range(5):
        mNos[i] = best_5_taxis[i][4]

