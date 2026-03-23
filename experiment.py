# experiment.py
import time
from src import (
    EightPuzzle,
    generate_random_state,
    BreadthFirstSearch,
    AStarSearch,
    HammingHeuristic,
    ChebyshevSumHeuristic,
)
    
def run_demo():
    print("=" * 60)
    print("TRÌNH GIẢI 8-PUZZLE")
    print("=" * 60)

    initial_state = generate_random_state(steps=15)
    problem = EightPuzzle(initial_state)
    
    print(f"\n[Trạng thái bắt đầu]\n{initial_state}")
    print(f"\nChọn heuristic: BFS or (Chebyshev/2) or (Hamming/2)")
    print("1. BFS\n2. A* (Chebyshev/2)\n3. A* (Hamming/2)")
    choice = int(input("Nhập lựa chọn : "))
    
    if choice == 1:
        print("\nĐang tìm đường đi bằng BFS...")
        solver = BreadthFirstSearch()
    elif choice == 2:
        print("\nĐang tìm đường đi bằng A* (Chebyshev/2)...")
        solver = AStarSearch(ChebyshevSumHeuristic())
    elif choice == 3:
        print("\nĐang tìm đường đi bằng A* (Hamming/2)...")
        solver = AStarSearch(HammingHeuristic())
    else:
        print("Lựa chọn không hợp lệ. Sử dụng A* (Chebyshev/2) mặc định.")
        solver = AStarSearch(ChebyshevSumHeuristic())
        

    t0 = time.perf_counter()
    result = solver.search(problem)
    elapsed = time.perf_counter() - t0

    if result:
        print(f"Đã giải xong trong {elapsed:.4f} giây!")
        print(f"Cost: {result.cost} | Nodes Expanded: {result.nodes_expanded} | Max Frontier: {result.max_frontier_size}")
        
        print(f"\n[Đường đi chi tiết - {len(result.actions)} bước]")
        for i, state in enumerate(result.path):
            action = result.actions[i - 1] if i > 0 else "BẮT ĐẦU"
            print(f"\nBước {i} [{action}]")
            for line in str(state).split("\n"):
                print(f"  {line}")

    else:
        print("\nKhông tìm thấy đường đi.")

def run_experiments(num_trials=5, shuffle_steps=15):
    print("\n\n" + "=" * 70)
    print(f"CHẠY THỰC NGHIỆM ({num_trials} Trials, Độ khó {shuffle_steps})")
    print("=" * 70)

    header = f"{'Trial':>5} | {'Thuật toán':>16} | {'Cost':>5} | {'Expanded':>8} | {'Frontier':>8} | {'Time(s)':>8}"
    print(header)
    print("-" * len(header))

    results = run_comparison_experiments(num_trials, shuffle_steps)

    for res in results:
        trial = res["Trial"]
        name = res["Thuật toán"]
        cost = res["Cost"]
        exp = res["Nodes Expanded"]
        front = res["Max Frontier"]
        time_s = res["Thời gian (s)"]
        
        if cost is not None:
            print(f"{trial:5} | {name:>16} | {cost:5} | {exp:8} | {front:8} | {time_s:8.4f}")
        else:
            print(f"{trial:5} | {name:>16} | {'N/A':>5} | {'N/A':>8} | {'N/A':>8} | {time_s:8.4f}")

def run_comparison_experiments(num_trials=5, shuffle_steps=15, progress_callback=None):
    """
    Chạy thực nghiệm so sánh 3 thuật toán.
    - Trả về danh sách (list) các dictionary chứa kết quả.
    - Cung cấp progress_callback(trial_hien_tai, tong_so_trial) để cập nhật giao diện nếu cần.
    """
    configs = [
        ("A* (Chebyshev/2)", AStarSearch(ChebyshevSumHeuristic())),
        ("A* (Hamming/2)", AStarSearch(HammingHeuristic())),
        ("BFS", BreadthFirstSearch())
    ]
    
    results = []
    
    for trial in range(1, num_trials + 1):
        initial_state = generate_random_state(steps=shuffle_steps)
        problem = EightPuzzle(initial_state)
        
        for name, solver in configs:
            t0 = time.perf_counter()
            res = solver.search(problem)
            elapsed = time.perf_counter() - t0
            
            record = {
                "Trial": trial,
                "Thuật toán": name,
                "Cost": res.cost if res else None,
                "Nodes Expanded": res.nodes_expanded if res else None,
                "Max Frontier": res.max_frontier_size if res else None,
                "Thời gian (s)": round(elapsed, 4)
            }
            results.append(record)
            
        # Gọi hàm callback nếu có (dành cho việc vẽ Progress bar trên Streamlit)
        if progress_callback:
            progress_callback(trial, num_trials)
            
    return results