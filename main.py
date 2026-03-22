# main.py
from experiment import run_demo, run_experiments

if __name__ == "__main__":
    # 1. Chạy demo giải 1 bài toán chi tiết
    run_demo()
    
    # 2. Chạy thử nghiệm so sánh 3 thuật toán
    run_experiments(num_trials=5, shuffle_steps=15)