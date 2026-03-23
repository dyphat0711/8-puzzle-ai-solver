# main.py
from experiment import run_demo, run_experiments

if __name__ == "__main__":
    run_demo()
    
    run_experiments(num_trials=5, shuffle_steps=15)