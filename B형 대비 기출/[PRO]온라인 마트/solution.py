'''
상품: ID, 품목, 제조사, 가격
품목 = 1 ~ 5
제조사 = 1 ~ 5

같은 품목과 제조사를 가진 상품들에 대해 가격을 특정 금액 만큼 할인가능
ex) 품목 1, 제조사 2인 상품에 대해 5만큼 할인 -> (ID, 1, 2, price) -> (ID, 1, 2, price - 5)
할인되어 가격이 <= 0 가 된다면 판매가 종료된다.

사용자에게 조건을 만족하는 상품에 대해 가격이 낮은 순서로 최대 5개 상품을 검색해서 보여준다.
조건 : 전체 상품, 특정 품목, 특정 제조사 (3가지)
같은경우 : 가격이 같다면, 상품 ID가 낮은것이 우선이다.

  mID : 추가할 자료의 ID (1 ≤ mID ≤ 1,000,000,000)
  mCategory : 상품의 품목 (1 ≤ mCategory ≤ 5)
  mCompany : 상품의 제조사 (1 ≤ mCompany ≤ 5)
  mPrice : 상품의 가격 (1 ≤ mPrice ≤ 1,000,000)

2. 각 테스트 케이스에서 sell() 함수의 호출 횟수는 50,000 이하이다.
3. 각 테스트 케이스에서 closeSale() 함수의 호출 횟수는 5,000 이하이다.
4. 각 테스트 케이스에서 discount() 함수의 호출 횟수는 10,000 이하이다.
5. 각 테스트 케이스에서 show() 함수의 호출 횟수는 1,000 이하이다.

'''
from collections import defaultdict
import heapq
import copy

'''
ID를 key값으로 defaultdict를 쓰자.
같은 품목과 제조사를 가진 판매중인 상품의 개수도 똑같이. 튜플을 키로 쓰고 value에 +cnt를 해주자.
'''


#####solution.py
class RESULT:
    def __init__(self, cnt, IDs):
        self.cnt = cnt
        self.IDs = IDs  # [int] * 5

def init() -> None:
    global ID_list, cnt_list, Key_list
    ID_list = defaultdict(list)
    cnt_list = defaultdict(int)
    Key_list = defaultdict(list)

def sell(mID : int, mCategory : int, mCompany : int, mPrice : int) -> int:
    # print("sell")
    ID_list[mID] = [mCategory, mCompany, mPrice, mID]
    cnt_list[(mCategory, mCompany)] += 1
    # 같은 품목과 제조사를 가진 상품의 개수 cnt 증가.
    Key_list[(mCategory, mCompany)].append(mID)
    # 품목, 제조사로 접근하면 해당 상품 mID가 나옴.
    # print(Key_list[(mCategory, mCompany)])
    # 품목이 mCategory이고 제조사 mCompany인 모든 상품의 가격을 mAmount 만큼 낮춘다. 를 위한 구문
    # print(f"sell({cnt_list[(mCategory, mCompany)]})")
    return cnt_list[(mCategory, mCompany)]

def closeSale(mID : int) -> int:
    # print("closeSale")
    price = 0
    if mID in ID_list.keys():
        Item_info = ID_list[mID]
        price = Item_info[2]
        cnt_list[(Item_info[0], Item_info[1])] -= 1
        Key_list[(Item_info[0], Item_info[1])].remove(mID)
        del ID_list[mID]
    if price:
        if price > 0:
            # print(price)
            return price
        else:
            # print(-1)
            return -1
    else:
        # print(-1)
        return -1

def close(mID : int) -> int:
    # print("close")
    if mID in ID_list.keys():
        Item_info = ID_list[mID]
        cnt_list[(Item_info[0], Item_info[1])] -= 1
        Key_list[(Item_info[0], Item_info[1])].remove(mID)
        del ID_list[mID]


def discount(mCategory : int, mCompany : int, mAmount : int) -> int:
    buffer = copy.deepcopy(Key_list[(mCategory, mCompany)])
    # print("discount")
    for id_V in buffer:
        ID_list[id_V][2] -= mAmount
        if ID_list[id_V][2] <= 0:
            close(id_V)
    return cnt_list[(mCategory, mCompany)]


def show(mHow : int, mCode : int) -> RESULT:
    buffer_ID = []
    cash = []
    rank = 0
    result = []
    a = 0
    # print("show")
    if mHow == 0:
        rank = heapq.nsmallest(5, ID_list.values(), key=lambda x: (x[2], x[3]))
        a = len(rank)
    if mHow == 1:
        for i in range(1, 6):
            buffer_ID.extend((Key_list[(mCode, i)]))
        for j in buffer_ID:
            if j:
                if a < 5:
                    a += 1
            cash.append(ID_list[j])

        rank = heapq.nsmallest(5, cash, key=lambda x: (x[2], x[3]))
    if mHow == 2:
        for i in range(1, 6):
            buffer_ID.extend(Key_list[(i, mCode)])
        for j in buffer_ID:
            if j:
                if a < 5:
                    a += 1
            cash.append(ID_list[j])
        rank = heapq.nsmallest(5, cash, key=lambda x: (x[2], x[3]))

    if rank:
        for i in rank:
            result.append(i[3])

    return RESULT(a, result)
