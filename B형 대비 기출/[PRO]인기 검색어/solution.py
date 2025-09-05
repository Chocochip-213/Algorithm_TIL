# ------------------의사 코드-----------------------
# add 할 때 길이별로 비교할 범주를 만들면 좋을듯함.
# 최대 검색어는 10000개이다.
# 입력받을 때, 해당 문자열의 길이를 키로 딕셔너리의 리스트에 append한다. ( default dict 함수 사용 Keyerror 미발생 )
# 최근검색어의 범위를 지정하는 것은 검색어를 저장할 각 딕셔너리의 리스트에, 공용 cnt + 1 하며 값을 함께 저장
# 튜플로 저장한다. ex) (cnt값, 검색어 문자열)
# 딕셔너리 리스트에 추가할 때 bisect.insort로 애초부터 cnt값을 기준으로 정렬하며 삽입한다.
# cnt 값에서 cnt - N 사이의 값만 추출 순회하면 해당 범위가 된다.
# -> 리스트를 순회하다가 N보다 작은 값이 나오면 탈출하면 나머지는 순회하지 않아도 된다.
# 노드 간선 연결을 어떻게 처리해야할까.
# 어차피 대표 검색어를 쓸꺼면, 대표 검색어 기준으로 유사도를 시작하면 되지 않을까?
# aaaa, aaaa, aaaa, aaab, aacb, aadb, ascb는 전부 유사 검색어인데,
# counter를 써서 aaaa를 가져오고, 그걸 기반으로 탐색을 들어간다.
# counter는 많이나온 순대로 보여주고, 몇개가 있는지도 보여주는것이다.
# 각 딕트 순회마다 카운팅 배열을 6개 생성
# 탐색 중 유사 검색어를 발견하면 해당 검색어를 또 유사검색어 list에 저장하고, dfs를 통해 쭉 계속 들어간다.
# 유사검색어의 유사검색어를 계속 탐색
# 유사검색어는 카운팅 배열을 사용, set형으로 저장한다. Top1의 유사검색어들은
# 각 딕트의 고유한 카운팅 배열의 1번째에 저장, counter 결과의 Top1의 유사검색어 탐색이 끝났으면,
# counter결과의 Top2와 set내부의 문자열을 비교한다. set안에 Top2..N이 있으면
# set와 비교 중 동일한 값이 있으면 그 값의 중복 수(몇개가 있는지)를 가져온 후 카운팅 배열에 더해준다.
# 또한 동일값이라면 visited를 또 만들어서 다음 탐색때는 탐색할 필요없도록 만든다.
# 먼저 글로벌 rank_list를 501개 배열(N <= 500)을 만들고, 각Dict를 순회하며 유사검색어를 찾으면 항상
# 각 Dict의 키 값과, 각 Dict리스트에서 몇번째 idx(몇번째 대표 검색어)의 유사검색어 인지(idx값)를 넣고, cnt를 증가시킨다.
# 이 건 새로운 대표검색어가 나올때마다 공통으로 공유하는 cnt를 +1 하면서 rank_list의 인덱스를 순회하며 값을 넣는다.
# 이거 반복(5개가 나오거나 dict순회를 끝마칠때 까지)
# 모든 dict를 순회한다.(만약 가지치기가 필요하면, 모든 dict에 counter를 날렸을때)
# 각 dict counter의 최소값의 5개보다 작은 dict 길이를 가지고 있는 dict(검색어가 애초에 작은 dict)는 이후에는 제외해도됨.
# 모든 dict를 순회한 후
# rank_list를 heapq를 이용하여
# Top 5개를 뽑는다.
# 5개의 dict 키값과 해당 키값의 인덱스 번호를 가져오고,
# 리스트에 문자열을 검색어를 넣은 뒤, cnt가 같은 경우 해당 문자열들만 슬라이싱을 통해 sort해준다.
# 끝
# 제출 시 solution.py 부분만 변경하여 제출해 주세요.


# __ AI 코드입니다. 의사코드 넣어서 생성함."
import collections
import bisect

from typing import List

# 전역 변수 선언
N = 0
global_counter = 0
# { 길이: [(추가 순서, "키워드"), ...] }
keywords_by_len = collections.defaultdict(list)
parent = {}


# --- Union-Find Helper Functions ---
def find(word: str) -> str:
    """word가 속한 그룹의 대표(루트)를 찾는다 (경로 압축 최적화 포함)."""
    if parent[word] == word:
        return word
    parent[word] = find(parent[word])
    return parent[word]


def union(word1: str, word2: str) -> None:
    """word1과 word2가 속한 두 그룹을 합친다."""
    root1 = find(word1)
    root2 = find(word2)
    if root1 != root2:
        # 사전순으로 앞서는 단어를 루트로 설정
        if root1 < root2:
            parent[root2] = root1
        else:
            parent[root1] = root2


# ------------------------------------

def is_similar(s1: str, s2: str) -> bool:
    """두 문자열이 한 글자만 다른지 확인한다."""
    diff = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            diff += 1
        if diff > 1:
            return False
    return diff == 1


def init(n_val: int) -> None:
    """테스트 케이스 초기화"""
    global N, global_counter, keywords_by_len
    N = n_val
    global_counter = 0
    keywords_by_len.clear()


def addKeyword(mKeyword: str) -> None:
    """새로운 키워드 추가"""
    global global_counter
    global_counter += 1
    length = len(mKeyword)
    # (추가 순서, 키워드) 튜플을 순서에 맞게 삽입 (bisect_left + insert 보다 insort가 편리)
    bisect.insort(keywords_by_len[length], (global_counter, mKeyword))


def top5Keyword(mRet: List[str]) -> int:
    """최근 N개 키워드 기준 Top 5 인기 검색어 반환"""

    # 1. 최근 N개 키워드 필터링 및 빈도수 계산
    cutoff_cnt = global_counter - N
    recent_keywords_counts = collections.Counter()
    unique_recent_keywords_by_len = collections.defaultdict(list)

    for length, keyword_list in keywords_by_len.items():
        # N개 범위의 시작 인덱스 찾기
        start_idx = bisect.bisect_left(keyword_list, (cutoff_cnt + 1, ''))

        # 유니크 키워드를 임시 set에 저장하여 중복 제거
        temp_unique_set = set()
        for i in range(start_idx, len(keyword_list)):
            keyword = keyword_list[i][1]
            recent_keywords_counts[keyword] += 1
            temp_unique_set.add(keyword)

        if temp_unique_set:
            unique_recent_keywords_by_len[length] = list(temp_unique_set)

    # 2. 유사 검색어 그룹핑 (Union-Find)
    global parent
    parent.clear()
    all_unique_keywords = []
    for length in unique_recent_keywords_by_len:
        all_unique_keywords.extend(unique_recent_keywords_by_len[length])

    # parent 딕셔너리 초기화
    for keyword in all_unique_keywords:
        parent[keyword] = keyword

    for length, keywords in unique_recent_keywords_by_len.items():
        # 길이가 같은 키워드 쌍에 대해서만 유사도 검사
        for i in range(len(keywords)):
            for j in range(i + 1, len(keywords)):
                word1 = keywords[i]
                word2 = keywords[j]
                if is_similar(word1, word2):
                    union(word1, word2)

    # 3. 그룹별 정보 집계
    groups = collections.defaultdict(lambda: {'total_count': 0, 'members': []})
    for keyword in all_unique_keywords:
        root = find(keyword)
        groups[root]['total_count'] += recent_keywords_counts[keyword]
        groups[root]['members'].append(keyword)

    # 4. 대표 검색어 선정 및 최종 순위 계산
    ranked_groups = []
    for root, data in groups.items():
        representative = ""
        max_freq = -1

        # 그룹 멤버들을 순회하며 대표 검색어 선정
        for member in sorted(data['members']):  # 사전순 정렬로 동일 빈도 처리 간소화
            freq = recent_keywords_counts[member]
            if freq > max_freq:
                max_freq = freq
                representative = member

        # (총점수, 대표검색어) 튜플로 저장
        ranked_groups.append((data['total_count'], representative))

    # 5. Top 5 추출 및 반환
    # 정렬: 1. 총점수(내림차순), 2. 대표검색어(오름차순)
    ranked_groups.sort(key=lambda x: (-x[0], x[1]))

    # mRet 초기화 후 결과 저장
    mRet.clear()
    count = min(5, len(ranked_groups))
    for i in range(count):
        mRet.append(ranked_groups[i][1])

    return count