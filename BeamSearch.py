from utils import *

def BeamSearch(chessboard, beam_width=3, max_iterations=1000):
    beam = [random_8x8_board() for _ in range(beam_width)]
    path = []
    visited = set()

    for _ in range(max_iterations):
        # Tính conflict của các state trong beam
        scored = [(count_conflicts(state), state) for state in beam]
        scored.sort(key=lambda x: x[0])
        
        best_h, best_state = scored[0]
        path.append(best_state)

        # Nếu đã giải xong
        if best_h == 0:
            chessboard.running = False
            return path

        # Sinh neighbor cho từng state trong beam
        neighbors = []
        for _, state in scored:
            for next_state in chessboard.next_states_2(state):
                # Chuyển state sang tuple để có thể hash
                state_tuple = tuple(map(tuple, next_state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    neighbors.append(next_state)

        # Nếu không có neighbor mới → dừng
        if not neighbors:
            chessboard.running = False
            return path

        # Chọn beam_width state tốt nhất cho vòng tiếp theo
        next_scored = [(count_conflicts(s), s) for s in neighbors]
        next_scored.sort(key=lambda x: x[0])
        beam = [s for _, s in next_scored[:beam_width]]

    # Nếu vượt quá số vòng lặp → coi như thất bại
    chessboard.running = False
    return path
