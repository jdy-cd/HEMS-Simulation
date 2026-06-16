import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import random

# ==========================================
# 页面全局高端配置
# ==========================================
st.set_page_config(
    page_title="高熵制造系统 - 分布式集群多主体协同平台",
    page_icon="🏭",
    layout="wide"
)

# === 1. 初始化多工厂私域动态数据库 ===
if "factories_db" not in st.session_state:
    st.session_state.factories_db = {
        "苏州智造一号园 (F01)": {
            "x": 120.6, "y": 31.3, "status": "空闲中", "color": "green",
            "secret_assets": {
                "cnc_count": 25, "equipment_oee": 92.5, "maintenance_schedule": "下周一常规维保",
                "workers_total": 45, "shift_pattern": "三班倒", "current_attendance": 96.0,
                "raw_materials_tons": 180.5, "bom_safety_stock": True, "material_shortage_risk": "极低"
            }
        },
        "宁波柔性先锋基地 (F02)": {
            "x": 121.5, "y": 29.8, "status": "轻度负荷", "color": "orange",
            "secret_assets": {
                "cnc_count": 12, "equipment_oee": 88.0, "maintenance_schedule": "无临近维保计划",
                "workers_total": 20, "shift_pattern": "两班倒", "current_attendance": 90.0,
                "raw_materials_tons": 45.0, "bom_safety_stock": False, "material_shortage_risk": "中等"
            }
        },
        "合肥精益规模化厂区 (F03)": {
            "x": 117.2, "y": 31.8, "status": "高负荷运转", "color": "red",
            "secret_assets": {
                "cnc_count": 50, "equipment_oee": 95.0, "maintenance_schedule": "当前正在进行3号线检修",
                "workers_total": 120, "shift_pattern": "三班倒", "current_attendance": 98.5,
                "raw_materials_tons": 350.0, "bom_safety_stock": True, "material_shortage_risk": "无风险"
            }
        },
        "常州分布式数字单元 (F04)": {
            "x": 119.9, "y": 31.8, "status": "空闲中", "color": "green",
            "secret_assets": {
                "cnc_count": 8, "equipment_oee": 91.0, "maintenance_schedule": "常规运行中",
                "workers_total": 15, "shift_pattern": "单班制", "current_attendance": 100.0,
                "raw_materials_tons": 35.0, "bom_safety_stock": True, "material_shortage_risk": "极低"
            }
        }
    }

# === 2. 初始化全局会话状态 ===
if "factory_a_demand" not in st.session_state:
    st.session_state.factory_a_demand = {}
if "bids_leaderboard" not in st.session_state:
    st.session_state.bids_leaderboard = {}
if "final_contract" not in st.session_state:
    st.session_state.final_contract = None
if "system_logs" not in st.session_state:
    st.session_state.system_logs = ["系统初始化成功。跨域分布式节点网络就绪。"]

# === 3. 初始化多源动态熵数据池 ===
if "entropy_data" not in st.session_state:
    st.session_state.entropy_data = pd.DataFrame({
        "阶段": ["初始平稳态"],
        "订单熵": [0.20], "资源熵": [0.25], "工艺熵": [0.15], "系统总熵": [0.60]
    })


def log_event(msg):
    t = time.strftime("%H:%M:%S", time.localtime())
    st.session_state.system_logs.append(f"[{t}] {msg}")


def update_entropy(stage_name, order_e, resource_e, process_e):
    total_e = order_e + resource_e + process_e
    new_row = pd.DataFrame({
        "阶段": [stage_name],
        "订单熵": [order_e], "资源熵": [resource_e], "工艺熵": [process_e], "系统总熵": [total_e]
    })
    st.session_state.entropy_data = pd.concat([st.session_state.entropy_data, new_row], ignore_index=True)


# ==========================================
# 顶层看板：分布式制造集群总控地图
# ==========================================
st.title("🏭 高熵制造系统：私域知识增强分布式自适应协同网络")
st.markdown("---")

st.subheader("🌐 全局大脑：分布式区域制造节点空间分布拓扑")
col_map, col_metrics = st.columns([2, 1])

with col_map:
    # 重新加回来的拓扑地图
    fig_map = go.Figure()
    fig_map.add_trace(go.Scatter(
        x=[118.8], y=[32.0], mode="markers+text",
        marker=dict(size=22, color="blue", symbol="hexagram"),
        name="需求发包方 (南京A工厂)", text=["南京A工厂"], textposition="top center"
    ))

    for f_name, f_info in st.session_state.factories_db.items():
        fig_map.add_trace(go.Scatter(
            x=[f_info["x"]], y=[f_info["y"]], mode="markers+text",
            marker=dict(size=16, color=f_info["color"]),
            name=f_name, text=[f_name.split(" ")[0]], textposition="bottom center"
        ))
        if st.session_state.factory_a_demand:
            fig_map.add_trace(go.Scatter(
                x=[118.8, f_info["x"]], y=[32.0, f_info["y"]],
                mode="lines", line=dict(color="gray", width=1, dash="dash"),
                showlegend=False
            ))

    fig_map.update_layout(
        xaxis=dict(title="经度", range=[116, 123]), yaxis=dict(title="纬度", range=[28, 34]),
        margin=dict(l=20, r=20, t=20, b=20), height=320, showlegend=True
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_metrics:
    st.markdown("#### 📊 集群当前运行态势")
    total_nodes = len(st.session_state.factories_db) + 1
    st.metric("制造网络节点总数", f"{total_nodes} 个自治Agent")
    active_bidders = [k for k, v in st.session_state.factories_db.items() if v["status"] != "高负荷运转"]
    st.metric("具备接单潜力厂区", f"{len(active_bidders)} / {len(st.session_state.factories_db)}")
    st.caption("注：高负荷流转的工厂将被边缘网关自动阻断投标。")

st.markdown("---")

# ==========================================
# 多视角控制台区域 (全五大视角)
# ==========================================
tab_a, tab_priv, tab_entropy, tab_contract, tab_log = st.tabs([
    "🎯 视角一：A工厂广播与定标",
    "🔒 视角二：各厂内部涉密底牌",
    "📈 视角三：多源动态熵视界",
    "🤝 视角四：博弈签约",
    "🛡️ 视角五：跨域安全日志"
])

# ------------------------------------------
# 🎯 视角一：A工厂广播与定标台
# ------------------------------------------
with tab_a:
    st.header("🛒 全网一键广播与智能选标")

    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        v_req = st.number_input("核心采购总量 (件)", value=6000, step=500)
    with col_a2:
        d_req = st.slider("最大交付期限 (天)", 1, 20, 6)
    with col_a3:
        b_req = st.number_input("全包最高代工总预算 (元)", value=200000, step=10000)

    p_req = st.selectbox("核心工艺精度门槛", ["普通级", "精密级", "航天级"])

    if st.button("🚀 向全网广播任务需求包", type="primary"):
        st.session_state.factory_a_demand = {"volume": v_req, "deadline": d_req, "budget": b_req, "precision": p_req}
        st.session_state.bids_leaderboard = {}
        st.session_state.final_contract = None
        log_event(f"A工厂发起全局广播：加工 {v_req} 件，限期 {d_req} 天。")
        update_entropy(f"需求突发扰动", 0.85, 0.40, 0.35)  # 引入熵增

        with st.spinner("多路自治Agent正调取本地涉密ERP进行计算..."):
            time.sleep(1.5)
            update_entropy(f"跨域多主体寻优", 0.75, 0.65, 0.55)  # 计算过程熵增

            for f_name, f_data in st.session_state.factories_db.items():
                secret = f_data["secret_assets"]
                if secret["material_shortage_risk"] == "高风险" or f_data["status"] == "高负荷运转":
                    continue

                shift_hours = 24 if "三班倒" in secret["shift_pattern"] else 16
                base_daily_capacity = secret["cnc_count"] * (secret["equipment_oee"] / 100) * (shift_hours / 8) * 40
                avail_daily_capacity = base_daily_capacity * (1 - (secret["current_attendance"] / 200))
                needed_days = round(v_req / avail_daily_capacity, 1) if avail_daily_capacity > 0 else 999

                cost_per_item = 25 if p_req == "精密级" else 15
                secret_cost = v_req * cost_per_item * (1 + (100 - secret["equipment_oee"]) / 100)
                bid_price = round(secret_cost * 1.15, 2)

                if needed_days <= d_req and bid_price <= b_req:
                    st.session_state.bids_leaderboard[f_name] = {
                        "price": bid_price, "days": needed_days,
                        "quality": f"{secret['equipment_oee']}%", "mode": "可用不可见验证核准"
                    }
        st.success("📢 全网响应完成！已在下方生成『代工竞标大盘』。")

    if st.session_state.bids_leaderboard:
        st.markdown("### 📥 分布式代工竞标大盘")
        bids_df = pd.DataFrame.from_dict(st.session_state.bids_leaderboard, orient="index")
        bids_df.columns = ["公开竞标报价 (元)", "承诺交期 (天)", "公开质量系数", "私域安全验证"]
        st.dataframe(bids_df, use_container_width=True)

        select_factory = st.selectbox("🎯 决策定标：选择承接厂区", list(st.session_state.bids_leaderboard.keys()))

        if st.button("🤝 确认签署智能代工合约", type="secondary"):
            st.session_state.final_contract = {
                "purchaser": "南京A工厂", "supplier": select_factory,
                "terms": st.session_state.bids_leaderboard[select_factory]
            }
            log_event(f"A工厂定标 【{select_factory}】。集群完成协同。")
            update_entropy(f"达成协同签约", 0.15, 0.20, 0.10)  # 达成协同，熵减
            st.balloons()
            st.success("✅ 合约锁定！请手动点击【📈 视角三】查看系统熵减变化曲线。")

# ------------------------------------------
# 🔒 视角二：各厂区内部涉密底牌
# ------------------------------------------
with tab_priv:
    st.header("🔒 各独立法人企业涉密核心资产")
    selected_f = st.selectbox("🔍 选择要审计的私域黑盒节点:", list(st.session_state.factories_db.keys()))
    f_assets = st.session_state.factories_db[selected_f]["secret_assets"]

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.metric("🔒 涉密CNC机床总数", f"{f_assets['cnc_count']} 台")
        st.metric("🔒 设备综合效率 (OEE)", f"{f_assets['equipment_oee']}%")
    with col_p2:
        st.metric("🔒 编制技术工人", f"{f_assets['workers_total']} 人")
        st.text_input("🔒 排班模式", f_assets["shift_pattern"], disabled=True)
    with col_p3:
        st.metric("🔒 原材料储备", f"{f_assets['raw_materials_tons']} 吨")
        st.error(f"🔒 突发缺料风险: {f_assets['material_shortage_risk']}")

# ------------------------------------------
# 📈 视角三：多源动态熵视界 (核心机理)
# ------------------------------------------
with tab_entropy:
    st.header("📈 制造系统多源熵增与协同熵减演化")
    df = st.session_state.entropy_data

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        fig_total = go.Figure()
        fig_total.add_trace(go.Scatter(
            x=df["阶段"], y=df["系统总熵"], mode='lines+markers',
            name='系统总熵(无序度)', line=dict(color='red', width=4), marker=dict(size=10)
        ))
        fig_total.update_layout(title="全局系统熵态演化轨迹", xaxis_title="生产演化阶段", yaxis_title="信息熵值 (nats)",
                                height=450)
        st.plotly_chart(fig_total, use_container_width=True)

    with col_e2:
        fig_bar = go.Figure(data=[
            go.Bar(name='订单熵', x=df["阶段"], y=df["订单熵"], marker_color='#1f77b4'),
            go.Bar(name='资源熵', x=df["阶段"], y=df["资源熵"], marker_color='#ff7f0e'),
            go.Bar(name='工艺熵', x=df["阶段"], y=df["工艺熵"], marker_color='#2ca02c')
        ])
        fig_bar.update_layout(barmode='stack', title="多源动态熵结构分析", xaxis_title="生产演化阶段",
                              yaxis_title="各源贡献", height=450)
        st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------------
# 🤝 视角四：签约与博弈分析
# ------------------------------------------
with tab_contract:
    st.header("🤝 智能合约与博弈存证")
    if st.session_state.final_contract:
        c = st.session_state.final_contract
        st.success(f"### 📜 代工双边协议 (编号: HEMS-{random.randint(10000, 99999)})")
        st.write(f"**核心发包方**: {c['purchaser']} | **中选代包方**: {c['supplier']}")
        st.write(f"**最终清算总价**: {c['terms']['price']} 元 | **承诺交期**: {c['terms']['days']} 天")
    else:
        st.info("尚未签约。请在『视角一』中定标。")

# ------------------------------------------
# 🛡️ 视角五：跨域安全日志
# ------------------------------------------
with tab_log:
    st.header("🛡️ 系统底层流转日志")
    for log in reversed(st.session_state.system_logs):
        st.code(log, language="bash")