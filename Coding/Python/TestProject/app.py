import streamlit as st
import pandas as pd
import numpy as np
import io

# --- 配置 ---
SUBJECTS = ['整车', '对标DVP', '底盘', '车身', '动总', '新能源', '仿真']
SCORES = [100, 95, 90, 85, 80, 75, 70]

# --- 获取 URL 参数 ---
query_params = st.query_params
reviewer = query_params.get("reviewer", [""])
is_admin = "admin" in query_params

# --- 初始化会话状态 ---
if 'peer_scores' not in st.session_state:
    st.session_state.peer_scores = {s: {} for s in SUBJECTS}
if 'manager_scores' not in st.session_state:
    st.session_state.manager_scores = {}

# --- 最终得分计算 ---
def calculate_final_scores():
    final_scores = {}
    for subject in SUBJECTS:
        peer_scores_list = []
        for evaluator in SUBJECTS:
            if subject in st.session_state.peer_scores[evaluator]:
                peer_scores_list.append(st.session_state.peer_scores[evaluator][subject])
        if subject in st.session_state.peer_scores[subject]:
            self_score = st.session_state.peer_scores[subject][subject]
            peer_scores_list = [s for s in peer_scores_list if s != self_score]
        else:
            self_score = None

        if len(peer_scores_list) > 2:
            peer_scores_list.remove(max(peer_scores_list))
            peer_scores_list.remove(min(peer_scores_list))

        peer_avg = np.mean(peer_scores_list) if peer_scores_list else 0
        manager_score = st.session_state.manager_scores.get(subject, 0)
        final_score = peer_avg * 0.7 + manager_score * 0.3
        final_scores[subject] = final_score
    return final_scores

# --- 互评分界面 ---
def peer_review():
    if reviewer not in SUBJECTS:
        st.error("链接无效或缺少身份参数。请通过指定链接访问。")
        return

    st.markdown(f"<h1 style='font-size:28px; font-weight:bold;'>欢迎，{reviewer}</h1>", unsafe_allow_html=True)
    st.markdown("<h4>请对其他主体进行打分，每个分数只能使用一次</h4>", unsafe_allow_html=True)

    other_subjects = [s for s in SUBJECTS if s != reviewer]
    scores_available = SCORES.copy()
    peer_scores = {}

    for subj in other_subjects:
        score = st.selectbox(f"给{subj}的分数：", options=scores_available, key=f"{reviewer}_{subj}")
        peer_scores[subj] = score
        scores_available.remove(score)

    self_score = st.selectbox(f"给自己({reviewer})的分数：", options=scores_available, key=f"{reviewer}_self")
    peer_scores[reviewer] = self_score

    if st.button("提交打分"):
        all_scores = list(peer_scores.values())
        if len(all_scores) != len(set(all_scores)):
            st.error("所有分数必须唯一，不能重复。")
            return
        st.session_state.peer_scores[reviewer] = peer_scores
        st.success("打分提交成功！")

# --- 主管评分界面 ---
def manager_review():
    st.title("主管评分")
    scores_available = SCORES.copy()
    manager_scores = {}

    for subj in SUBJECTS:
        score = st.selectbox(f"{subj} 的分数：", options=scores_available, key=f"manager_{subj}")
        manager_scores[subj] = score
        scores_available.remove(score)

    if st.button("提交主管评分"):
        if len(manager_scores.values()) != len(set(manager_scores.values())):
            st.error("所有分数必须唯一")
            return
        st.session_state.manager_scores = manager_scores
        st.success("主管评分提交成功！")

    if st.button("查看最终排名"):
        final_scores = calculate_final_scores()
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        st.write("### 最终排名：")
        for i, (s, score) in enumerate(ranked, 1):
            st.write(f"{i}. {s}：{score:.2f}")

    if st.button("导出Excel"):
        all_data = []
        for reviewer_, scores in st.session_state.peer_scores.items():
            for target, score in scores.items():
                all_data.append({"打分人": reviewer_, "被打分人": target, "分数": score, "来源": "互评"})

        for target, score in st.session_state.manager_scores.items():
            all_data.append({"打分人": "主管", "被打分人": target, "分数": score, "来源": "主管"})

        df = pd.DataFrame(all_data)
        final_scores = calculate_final_scores()
        ranking_df = pd.DataFrame([{"主体": k, "最终得分": v} for k, v in final_scores.items()]).sort_values("最终得分", ascending=False)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="详细打分")
            ranking_df.to_excel(writer, index=False, sheet_name="最终排名")
        output.seek(0)

        st.download_button("📥 下载Excel结果", data=output, file_name="评分结果.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# --- 主函数 ---
def main():
    if is_admin:
        manager_review()
    else:
        peer_review()

if __name__ == '__main__':
    main()
