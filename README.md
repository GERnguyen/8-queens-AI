# 8 Queens Visualizer

Chương trình minh họa các thuật toán tìm kiếm để giải bài toán 8 quân hậu (8 Queens Problem).

## Giới thiệu

Bài toán 8 quân hậu là bài toán cổ điển trong khoa học máy tính: đặt 8 quân hậu trên bàn cờ 8x8 sao cho không quân nào ăn được quân nào.

Project này cài đặt và trực quan hóa nhiều thuật toán AI khác nhau để giải quyết bài toán này.

## Các thuật toán đã cài đặt

### Thuật toán tìm kiếm không thông tin
- **BFS** (Breadth-First Search): Duyệt theo chiều rộng
- **DFS** (Depth-First Search): Duyệt theo chiều sâu
- **IDS** (Iterative Deepening Search): Duyệt lặp với độ sâu tăng dần
- **UCS** (Uniform Cost Search): Tìm kiếm theo chi phí đồng nhất

### Thuật toán tìm kiếm có thông tin
- **Greedy**: Tìm kiếm tham lam
- **A***: Kết hợp giữa chi phí và heuristic

### Thuật toán tìm kiếm cục bộ
- **Hill Climbing**: Leo đồi
- **Simulated Annealing**: Mô phỏng luyện kim
- **Beam Search**: Tìm kiếm chùm tia

### Thuật toán CSP (Constraint Satisfaction Problem)
- **Backtracking**: Quay lui
- **Forward Checking**: Kiểm tra trước
- **AC-3**: Arc Consistency

## Cài đặt

### Yêu cầu
- Python 3.x
- Pygame
- NumPy

### Cài đặt thư viện
```bash
pip install pygame numpy
```

## Cách chạy

```bash
python main.py
```

## Hướng dẫn sử dụng

1. Chạy chương trình
2. Chọn thuật toán bằng cách click vào các button tương ứng
3. Quan sát quá trình tìm kiếm trên bàn cờ
4. Nhấn nút **SKIP** để chuyển thẳng đến kết quả cuối cùng

## Cấu trúc project

- `main.py`: File chính, xử lý giao diện và vòng lặp game
- `ChessBoard.py`: Class quản lý bàn cờ và các thao tác
- `BFS.py`, `DFS.py`, `IDS.py`, `UCS.py`: Các thuật toán tìm kiếm không thông tin
- `Greedy.py`, `AStar.py`: Các thuật toán tìm kiếm có thông tin
- `HillClimbing.py`, `SimulatedAnnealing.py`, `BeamSearch.py`: Các thuật toán tìm kiếm cục bộ
- `CSP.py`: Các thuật toán CSP
- `utils.py`: Các hàm hỗ trợ (heuristic, đếm xung đột, ...)
- `button.py`: Class nút bấm
- `const.py`: Các hằng số (màu sắc, kích thước, ...)

## Ghi chú

- Khi bàn cờ có viền xanh lá nghĩa là đã tìm thấy lời giải
- Tốc độ hiển thị có thể điều chỉnh bằng cách thay đổi giá trị `wait` trong file `main.py`
- Một số thuật toán (Hill Climbing, Simulated Annealing, Beam Search) có thể không tìm được lời giải do tính chất ngẫu nhiên

