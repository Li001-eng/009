import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 页面标题
st.set_page_config(page_title="心跳包序号趋势", layout="wide")
st.title("❤️ 心跳包序号随时间变化")
st.markdown("本应用展示心跳包序号随时间的变化趋势，数据源来自 GitHub 或模拟生成。")

# 数据加载方式选择
data_source = st.sidebar.radio("选择数据来源", ("模拟数据", "GitHub CSV"))

if data_source == "GitHub CSV":
    # 这里替换为你的 GitHub raw CSV 地址
    csv_url = st.sidebar.text_input(
        "GitHub Raw CSV URL",
        value="https://raw.githubusercontent.com/example/repo/main/heartbeat_data.csv"
    )
    try:
        df = pd.read_csv(csv_url)
        st.sidebar.success("数据加载成功！")
    except Exception as e:
        st.sidebar.error(f"加载失败：{e}")
        st.stop()
else:
    # 模拟生成数据
    st.sidebar.info("使用模拟数据（最近 24 小时，每分钟一条）")
    # 生成时间序列（最近24小时，每分钟一次）
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    timestamps = pd.date_range(start=start_time, end=end_time, freq="1min")
    # 模拟心跳序号：从 0 开始，每分钟增加 1，加入微小波动
    base_seq = list(range(len(timestamps)))
    # 让序号偶尔有跳跃（模拟丢包或重传？这里简单保持递增）
    heartbeat_seq = base_seq
    df = pd.DataFrame({
        "timestamp": timestamps,
        "heartbeat_seq": heartbeat_seq
    })

# 确保 timestamp 列是 datetime 类型（若为字符串则转换）
if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# 显示原始数据（可折叠）
with st.expander("查看原始数据"):
    st.dataframe(df)

# 绘制折线图
st.subheader("心跳包序号趋势图")
fig = px.line(
    df,
    x="timestamp",
    y="heartbeat_seq",
    title="心跳包序号随时间变化",
    labels={"timestamp": "时间", "heartbeat_seq": "心跳包序号"},
    line_shape="linear"
)
fig.update_layout(
    hovermode="x unified",
    xaxis_title="时间",
    yaxis_title="心跳包序号",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# 额外统计信息
st.subheader("数据统计")
col1, col2, col3 = st.columns(3)
col1.metric("记录总数", len(df))
col2.metric("起始序号", df["heartbeat_seq"].iloc[0])
col3.metric("最新序号", df["heartbeat_seq"].iloc[-1])
