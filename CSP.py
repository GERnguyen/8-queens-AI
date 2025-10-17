import numpy as np
import time
import random
from collections import deque

N = 8
count_bt = 0
count_fc = 0
count_ac3 = 0

def consistent(assignment, value):
    """
    Kiểm tra xem việc gán value có consistent với assignment hiện tại không
    value = (row, col)
    Quân hậu không được trùng hàng, cột, hoặc đường chéo
    """
    r1, c1 = value
    for (r2, c2) in assignment:
        # Trùng hàng hoặc trùng cột
        if r1 == r2 or c1 == c2:
            return False
        # Trùng đường chéo
        if abs(r1 - r2) == abs(c1 - c2):
            return False
    return True

def backtracking(assignment):
    global count_bt

    board = np.array([[1 if (r, c) in assignment else 0 for c in range(N)] for r in range(N)])
    yield board, assignment[:]

    if len(assignment) == N:
        return

    r = len(assignment)  # Hàng tiếp theo cần đặt
    domain = [(r, c) for c in range(N)]
    random.shuffle(domain)

    for value in domain:
        if consistent(assignment, value):
            count_bt += 1
            yield from backtracking(assignment + [value])

def forwardchecking(assignment, domains):
    global count_fc

    board = np.array([[1 if (r, c) in assignment else 0 for c in range(N)] for r in range(N)])
    yield board, assignment[:]

    if len(assignment) == N:
        return

    var = len(assignment)  # Hàng tiếp theo
    domain_var = domains[var][:]
    random.shuffle(domain_var)

    for value in domain_var:
        if consistent(assignment, value):
            count_fc += 1
            r, c = value

            # Tạo domain mới cho các biến chưa gán
            new_domains = {k: v[:] for k, v in domains.items()}
            valid = True
            
            # Loại bỏ các giá trị không khả thi từ domain của các hàng tiếp theo
            for future_var in range(var + 1, N):
                new_domains[future_var] = [
                    (fr, fc)
                    for (fr, fc) in new_domains[future_var]
                    if fc != c  # Không cùng cột
                    and abs(fr - r) != abs(fc - c)  # Không cùng đường chéo
                ]
                
                # Nếu domain rỗng -> dead end
                if not new_domains[future_var]:
                    valid = False
                    break

            if valid:
                yield from forwardchecking(assignment + [value], new_domains)

def consistent_ac3(vi, vj):
    """
    Kiểm tra hai giá trị có consistent với nhau không
    vi, vj = (row, col)
    """
    r1, c1 = vi
    r2, c2 = vj
    # Không trùng hàng, cột, đường chéo
    return not (r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2))

def solve_from_domains(domains):
    """
    Giải bài toán sau khi đã có domain bị thu hẹp từ AC-3
    """
    order = sorted(range(N), key=lambda r: len(domains[r]))
    used_cols = set()
    assignment = [None] * N

    def dfs(idx):
        if idx == N:
            return True
        r = order[idx]
        
        for (_, c) in sorted(domains[r], key=lambda x: x[1]):
            if c in used_cols:
                continue
            
            # Kiểm tra đường chéo với các quân hậu đã đặt
            valid = True
            for prev_r in range(N):
                if assignment[prev_r] is not None:
                    prev_r_pos, prev_c = assignment[prev_r]
                    if abs(prev_r_pos - r) == abs(prev_c - c):
                        valid = False
                        break
            
            if not valid:
                continue
                
            assignment[r] = (r, c)
            used_cols.add(c)
            
            if dfs(idx + 1):
                return True
            
            used_cols.remove(c)
            assignment[r] = None
        return False

    ok = dfs(0)
    if not ok:
        return None
    return [assignment[r] for r in range(N)]

def ac3(domains):
    """
    AC-3 (Arc Consistency Algorithm 3)
    Đảm bảo arc consistency cho tất cả các cặp biến
    """
    global count_ac3
    
    # Tạo queue chứa tất cả các arc (Xi, Xj)
    queue = deque([(xi, xj) for xi in range(N) for xj in range(N) if xi != xj])
    queue = deque(random.sample(list(queue), len(queue)))

    board = np.zeros((N, N), dtype=int)
    yield board, []

    while queue:
        xi, xj = queue.popleft()
        count_ac3 += 1
        removed = False
        new_domain_xi = []

        # Với mỗi giá trị trong domain của Xi
        # Kiểm tra xem có tồn tại giá trị trong domain của Xj thỏa mãn constraint không
        for vi in domains[xi]:
            if any(consistent_ac3(vi, vj) for vj in domains[xj]):
                new_domain_xi.append(vi)

        # Nếu domain bị thu hẹp
        if len(new_domain_xi) < len(domains[xi]):
            domains[xi] = new_domain_xi
            removed = True

        # Nếu domain rỗng -> không có nghiệm
        if not domains[xi]:
            board = np.zeros((N, N), dtype=int)
            yield board, []
            return

        # Nếu domain thay đổi, thêm các arc liên quan vào queue
        if removed:
            for xk in range(N):
                if xk != xi and xk != xj:
                    queue.append((xk, xi))

        # Visualize: hiển thị board với các giá trị có thể
        board = np.zeros((N, N), dtype=int)
        temp_assignment = []

        for r, vals in domains.items():
            if len(vals) == 1:
                # Nếu domain chỉ có 1 giá trị -> đặt chắc chắn
                _, c = vals[0]
                board[r, c] = 1
                temp_assignment.append((r, c))
            elif len(vals) > 1:
                # Nếu có nhiều giá trị -> chọn random để hiển thị
                vi = random.choice(vals)
                _, c = vi
                board[r, c] = 1

        yield board, temp_assignment

    # Sau khi hết queue, giải bài toán với domain đã thu hẹp
    sol = solve_from_domains({k: v[:] for k, v in domains.items()})
    
    if sol is None or len(sol) < N:
        board = np.zeros((N, N), dtype=int)
        yield board, []
        return

    # Kiểm tra solution có hợp lệ không
    rows = [r for (r, c) in sol]
    cols = [c for (r, c) in sol]
    
    # Kiểm tra đường chéo
    valid = True
    for i in range(N):
        for j in range(i + 1, N):
            r1, c1 = sol[i]
            r2, c2 = sol[j]
            if abs(r1 - r2) == abs(c1 - c2):
                valid = False
                break
        if not valid:
            break
    
    if len(set(rows)) == N and len(set(cols)) == N and valid:
        board = np.zeros((N, N), dtype=int)
        for (r, c) in sol:
            board[r, c] = 1
        yield board, sol[:]
    else:
        board = np.zeros((N, N), dtype=int)
        yield board, []

def run_algorithm(algorithm="bt", visualize=False):
    global count_bt, count_fc, count_ac3
    count_bt = count_fc = count_ac3 = 0

    start = time.time()
    found = False
    total_states = 0
    last_state, last_path = None, None

    if algorithm == "bt":
        steps = backtracking([])
        name = "BACKTRACKING"
    elif algorithm == "fc":
        domains = {r: [(r, c) for c in range(N)] for r in range(N)}
        steps = forwardchecking([], domains)
        name = "FORWARD CHECKING"
    elif algorithm == "ac3":
        domains = {r: [(r, c) for c in range(N)] for r in range(N)}
        steps = ac3(domains)
        name = "AC-3 (Arc Consistency)"
    else:
        raise ValueError("Thuật toán không hợp lệ!")

    if visualize:
        return steps

    # Chạy không visualize
    try:
        for state, path in steps:
            last_state, last_path = state, path
            total_states += 1
            if algorithm != "ac3" and len(path) == N:
                found = True
                break
    except StopIteration:
        pass

    elapsed = time.time() - start

    if algorithm == "bt":
        count = count_bt
    elif algorithm == "fc":
        count = count_fc
    else:
        count = count_ac3

    print(f"=== {name} ===")
    print(f"Thời gian chạy: {elapsed:.4f}s")
    print(f"Số trạng thái duyệt: {count}")
    
    if last_state is not None and last_path and len(last_path) == N:
        print("\n✓ Tìm thấy nghiệm!")
        print("\nBoard kết quả:")
        print(last_state)
        print("\nVị trí các quân hậu:")
        for r, c in sorted(last_path):
            print(f"  Hàng {r}: Cột {c}")
    else:
        print("\n✗ Không tìm thấy nghiệm!")

    return last_state, last_path, elapsed