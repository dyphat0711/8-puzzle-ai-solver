# app.py
import streamlit as st
import time
import pandas as pd
from datetime import datetime

# Import logic từ file modules 
from problem import EightPuzzle
from utils import generate_random_state
from search import BreadthFirstSearch, AStarSearch
from heuristics import HammingHeuristic, ChebyshevSumHeuristic
from visualization import render_tree_graphviz
from experiment import run_comparison_experiments

st.set_page_config(page_title="8-Puzzle Solver", page_icon="🧩", layout="wide")
st.title("🧩 8-Puzzle")

def draw_board(state):
    b = state.board
    html = "<table style='margin:auto; font-size:24px; text-align:center; border-collapse: separate; border-spacing: 5px;'>"
    for r in range(3):
        html += "<tr>"
        for c in range(3):
            val = b[r*3 + c]
            text = str(val) if val != 0 else ""
            bg = "#2196F3" if val != 0 else "#eeeeee"
            color = "white" if val != 0 else "black"
            shadow = "box-shadow: 2px 2px 5px rgba(0,0,0,0.2);" if val != 0 else ""
            html += f"<td style='width:60px; height:60px; background-color:{bg}; color:{color}; border-radius:10px; {shadow}'><b>{text}</b></td>"
        html += "</tr>"
    html += "</table><br>"
    return html

tab1, tab2 = st.tabs(["👁️ Minh hoạ từng bước", "🧪 Thực nghiệm & Lịch sử"])

# ==========================================
# TAB 1: MINH HOẠ TỪNG BƯỚC ĐI CỦA 1 BÀI TOÁN (Giữ nguyên)
# ==========================================
with tab1:
    st.markdown("### Xem cách thuật toán di chuyển các ô số để đạt trạng thái đích")
    if 'single_state' not in st.session_state:
        st.session_state.single_state = generate_random_state(steps=15)
        
    col_setup, col_visual = st.columns([1, 3])
    
    with col_setup:
        st.markdown("**1. Trạng thái ban đầu**")
        st.write(draw_board(st.session_state.single_state), unsafe_allow_html=True)
        diff = st.slider("Độ khó (Bước xáo trộn):", 5, 30, 15, key="single_diff")
        if st.button("🎲 Tạo bài toán mới", use_container_width=True):
            st.session_state.single_state = generate_random_state(steps=diff)
            st.rerun()
            
        st.divider()
        st.markdown("**2. Chọn thuật toán**")
        algo_choice = st.selectbox("Thuật toán:", ["A* (Chebyshev/2)", "A* (Hamming/2)", "BFS"])
        solve_btn = st.button("🚀 Giải và Xem các bước", type="primary", use_container_width=True)

    with col_visual:
        if solve_btn:
            problem = EightPuzzle(st.session_state.single_state)
            if algo_choice == "A* (Chebyshev/2)":
                solver = AStarSearch(ChebyshevSumHeuristic())
            elif algo_choice == "A* (Hamming/2)":
                solver = AStarSearch(HammingHeuristic())
            else:
                solver = BreadthFirstSearch()
                
            with st.spinner("Đang tìm đường đi..."):
                t0 = time.perf_counter()
                result = solver.search(problem)
                elapsed = time.perf_counter() - t0
                
            if result:
                st.success(f"🎉 Đã tìm thấy lời giải ({result.cost} bước) trong {elapsed:.4f} giây!")
                st.markdown("### 🗺️ Chi tiết các bước di chuyển")
                
                st.markdown("### 🌳 Sơ đồ cây tìm kiếm (Top 15 Node mở rộng)")
                dot_graph = render_tree_graphviz(solver.expanded_nodes, n=15, return_dot=True)
                if dot_graph:
                    st.graphviz_chart(dot_graph)
                else:
                    st.warning("Vui lòng cài đặt thư viện 'graphviz' (`pip install graphviz`) để xem sơ đồ cây trực quan.")
                st.divider()
                
                steps_per_row = 4
                for i in range(0, len(result.path), steps_per_row):
                    cols = st.columns(steps_per_row)
                    for j in range(steps_per_row):
                        idx = i + j
                        if idx < len(result.path):
                            state = result.path[idx]
                            action = result.actions[idx - 1] if idx > 0 else "TRẠNG THÁI BẮT ĐẦU"
                            with cols[j]:
                                st.markdown(f"<div style='text-align:center;'><b>Bước {idx}</b><br><span style='color:#E91E63; font-size:14px;'><i>{action}</i></span></div>", unsafe_allow_html=True)
                                st.write(draw_board(state), unsafe_allow_html=True)
            else:
                st.error("Không tìm thấy lời giải.")

# ==========================================
# TAB 2: THỰC NGHIỆM VÀ LỊCH SỬ (Sử dụng experiment.py)
# ==========================================
with tab2:
    if 'history_df' not in st.session_state:
        st.session_state.history_df = pd.DataFrame()

    with st.sidebar:
        st.header("⚙️ Cài đặt thực nghiệm (Tab 2)")
        num_trials = st.slider("Số bài toán mỗi đợt:", 1, 20, 5)
        shuffle_steps = st.slider("Độ khó (Bước xáo trộn):", 5, 25, 15)
        run_exp_btn = st.button("🚀 Chạy đợt thực nghiệm mới", type="primary", use_container_width=True)
        if st.button("🗑️ Xóa lịch sử", use_container_width=True):
            st.session_state.history_df = pd.DataFrame()
            st.rerun()

    if run_exp_btn:
        run_time = datetime.now().strftime("%H:%M:%S")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Callback để cập nhật thanh tiến trình từ bên trong hàm experiment
        def update_ui(current_trial, total_trials):
            status_text.text(f"Đang xử lý bài toán {current_trial} / {total_trials}...")
            progress_bar.progress(current_trial / total_trials)
            
        # Gọi hàm chung từ experiment.py thay vì tự viết vòng lặp
        results_list = run_comparison_experiments(num_trials, shuffle_steps, update_ui)
        
        # Thêm cột "Đợt chạy" vào kết quả trả về
        for r in results_list:
            r["Đợt chạy"] = run_time
            
        status_text.success(f"✅ Đã hoàn thành đợt chạy lúc {run_time}!")
        
        new_df = pd.DataFrame(results_list)
        if st.session_state.history_df.empty:
            st.session_state.history_df = new_df
        else:
            st.session_state.history_df = pd.concat([st.session_state.history_df, new_df], ignore_index=True)

    if not st.session_state.history_df.empty:
        df = st.session_state.history_df
        st.subheader("📋 Lịch sử chi tiết")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.subheader("📊 Bảng Tổng kết (Trung bình)")
        summary_df = df.groupby("Thuật toán").agg({
            "Cost": "mean", "Nodes Explored": "mean",
            "Max Frontier": "mean", "Thời gian (s)": "mean"
        }).reset_index()
        st.table(summary_df)
        
        st.subheader("📈 Biểu đồ hiệu năng")
        chart_df = summary_df.set_index("Thuật toán")
        c1, c2, c3 = st.columns(3)
        with c1: st.bar_chart(chart_df["Thời gian (s)"], color="#FF5722") 
        with c2: st.bar_chart(chart_df["Nodes Explored"], color="#4CAF50") 
        with c3: st.bar_chart(chart_df["Max Frontier"], color="#2196F3")
    else:
        st.info("Chưa có dữ liệu thực nghiệm. Bấm 'Chạy đợt thực nghiệm mới' ở sidebar để bắt đầu.")