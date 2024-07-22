import heapq
import sys

def distra(start, end):
    distances = {node: sys.maxsize for node in graph} # 초기 배열 설정 (딕셔너리)
    course = [[0, 'A'],[0, 'B'],[0, 'C'],[0, 'D'],[0, 'E'],[0, 'F']]
    end_path = []
    distances[start] = 0 # 시작 노드의 거리는 0으로 설정
    queue = [] # (리스트)
    heapq.heappush(queue, (distances[start], start)) # 시작 노드부터 탐색 시작 (거리, 노드) - 힙큐 모듈에서 첫 번째 데이터를 기준으로 정렬하기 때문에 노드, 거리 순으로 넣으면 힙이 예상한대로 정렬되지 않음

    while queue: # 우선 순위 큐에 데이터가 하나도 없을 때까지 반복
        current_distance, node = heapq.heappop(queue) # 가장 낮은 거리를 가진 노드와 거리를 추출
        if distances[node] < current_distance: # 이미 저장된 거리와 추출한 거리를 비교 → 저장된 거리가 더 작다면 비교하지 않음
            continue
            
            # items 함수는 Key와 Value의 쌍을 튜플로 묶은 값을 객체로 돌려줌 : adjacency_node - 키, distance - 값
        for adjacency_node, distance in graph[node].items(): # 대상인 노드에서 인접한 노드와 거리를 순회
            weighted_distance = current_distance + distance # 현재 노드에서 인접한 노드를 지나갈 때까지의 거리를 더함

            if weighted_distance < distances[adjacency_node]: # 배열에 저장된 거리보다 위의 가중치가 더 작으면 해당 노드의 거리 변경
                distances[adjacency_node] = weighted_distance # 배열에 저장된 거리보다 가중치가 더 작으므로 변경
                for x in course:
                    if x[1] == adjacency_node:                 
                        if len(x) > 2:
                            del x[-1] # 배열에 저장된 거리보다 가중치가 더 작으므로, 기존에 있던 거리는 최단거리X → 마지막 하나를 삭제
                        x.append(node) # 다음으로 탐색할 지점 리스트에 지금 있는 지점을 추가
                heapq.heappush(queue, (weighted_distance, adjacency_node)) # 다음 인접 거리를 계산하기 위해 우선 순위 큐에 삽입

    end_path.append(end) # 최종 경로에 목적지 추가
    for x1 in course:
        if x1[1] == end:
            last = x1[-1]
            end_path.append(last) # 목적지에 있는 리스트 중 마지막 지점을 추가
            
    while last != start: # 리스트의 마지막 지점에 출발지라면, 반복 종료
        for x2 in course:
            if x2[1] == last:
                last = x2[-1]
                end_path.append(last) # 추가된 마지막 지점의 리스트 중 마지막 지점을 추가 → 반복
                break
                
    #del end_path[-1]
    #print(course)
    end_path.reverse() # 목적지부터 출발지까지 거꾸로 경로를 넣었으므로, 다시 뒤집음        
    return distances, end_path
    
graph = { # 딕셔너리 immutable한 키와 mutable한 값으로 맵핑되어있는 순서가 없는 집합 → 인덱스로 접근할 수 없음
    'A': {'B': 4, 'C': 4, 'E': 10},
    'B': {'A': 4, 'C': 3, 'D': 3, 'E': 5},
    'C': {'A': 4, 'B': 3, 'D': 5},
    'D': {'B': 3, 'C': 5, 'F': 3},
    'E': {'A': 10, 'B': 5, 'F': 2},
    'F': {'D': 3, 'E': 2}
}

start = input('출발점을 입력하세요 : ')
end = input('도착점을 입력하세요 : ')

def path(start, end):   
    result, course = distra(start, end)
    print(f'{start}로부터 각 지점까지 최단경로 : {result}\n{start}부터 {end}까지 경로 : {course}')
    return course


a = path(start, end)