import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="電気シミュレータ", layout="wide")

st.title("電気シミュレータ")

# -------------------------
# RLCパラメータ
# -------------------------

st.header("RLC回路")

col_in1, col_in2 = st.columns(2)

with col_in1:
    V = st.number_input("電圧(V)", min_value=0.0, max_value=500.0, value=100.0, step=10.0)
    f = st.number_input("周波数(Hz)", min_value=1.0, max_value=100.0, value=50.0, step=1.0)
    R = st.number_input("抵抗(Ω)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)

with col_in2:
    L = st.number_input("コイル(H)", min_value=0.001, max_value=1.0, value=0.1, step=0.01, format="%.3f")
    C = st.number_input("コンデンサ(F)", min_value=0.000001, max_value=0.01, value=0.001, step=0.0001, format="%.6f")

XL = 2 * np.pi * f * L
XC = 1 / (2 * np.pi * f * C)

Z = np.sqrt(R**2 + (XL - XC)**2)

# ゼロ割り防止
I = 0.0 if Z == 0 else V / Z

st.subheader("RLC計算結果")

col_calc1, col_calc2, col_calc3 = st.columns(3)

with col_calc1:
    st.metric("リアクタンス XL", f"{XL:.4f}")
    st.metric("リアクタンス XC", f"{XC:.4f}")

with col_calc2:
    st.metric("インピーダンス Z", f"{Z:.4f}")
    st.metric("電流 I", f"{I:.4f}")

# -------------------------
# 位相と力率
# -------------------------

theta = np.arctan((XL - XC) / R)
pf = np.cos(theta)

with col_calc3:
    st.metric("位相角 θ [rad]", f"{theta:.4f}")
    st.metric("力率 cosθ", f"{pf:.4f}")

# -------------------------
# 電力
# -------------------------

P = V * I * pf
S = V * I
Q = V * I * np.sin(theta)

st.subheader("電力")

col_power1, col_power2, col_power3 = st.columns(3)

with col_power1:
    st.metric("有効電力 P [W]", f"{P:.4f}")

with col_power2:
    st.metric("皮相電力 S [VA]", f"{S:.4f}")

with col_power3:
    st.metric("無効電力 Q [var]", f"{Q:.4f}")

# -------------------------
# 共振
# -------------------------

f_res = 1 / (2 * np.pi * np.sqrt(L * C))
st.metric("共振周波数 [Hz]", f"{f_res:.4f}")

# -------------------------
# 電圧・電流波形
# -------------------------

st.subheader("電圧と電流の波形")

t = np.linspace(0, 0.1, 1000)

v = V * np.sin(2 * np.pi * f * t)
i = I * np.sin(2 * np.pi * f * t - theta)

fig, ax = plt.subplots()
ax.plot(t, v, label="電圧")
ax.plot(t, i, label="電流")
ax.set_xlabel("時間 [s]")
ax.set_ylabel("振幅")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# -------------------------
# フェーザ図
# -------------------------

st.subheader("フェーザ図")

fig_ph, ax_ph = plt.subplots()

# 電圧ベクトル
ax_ph.quiver(0, 0, 1, 0, angles="xy", scale_units="xy", scale=1, color="blue")
ax_ph.text(1.05, 0, "V", color="blue")

# 電流ベクトル
ax_ph.quiver(
    0, 0,
    np.cos(theta), -np.sin(theta),
    angles="xy", scale_units="xy", scale=1, color="red"
)
ax_ph.text(np.cos(theta) * 1.05, -np.sin(theta) * 1.05, "I", color="red")

ax_ph.set_xlim(-1.5, 1.5)
ax_ph.set_ylim(-1.5, 1.5)
ax_ph.axhline(0, color="gray", linewidth=0.5)
ax_ph.axvline(0, color="gray", linewidth=0.5)
ax_ph.set_aspect("equal")
ax_ph.grid(True)

st.pyplot(fig_ph)

# -------------------------
# 三相交流
# -------------------------

st.divider()
st.header("三相交流")

v_a = V * np.sin(2 * np.pi * f * t)
v_b = V * np.sin(2 * np.pi * f * t - 2 * np.pi / 3)
v_c = V * np.sin(2 * np.pi * f * t - 4 * np.pi / 3)

fig2, ax2 = plt.subplots()
ax2.plot(t, v_a, label="A相")
ax2.plot(t, v_b, label="B相")
ax2.plot(t, v_c, label="C相")
ax2.set_xlabel("時間 [s]")
ax2.set_ylabel("電圧")
ax2.grid(True)
ax2.legend()

st.pyplot(fig2)

# -------------------------
# 三相電力
# -------------------------

st.subheader("三相電力")

col_tp1, col_tp2, col_tp3 = st.columns(3)

with col_tp1:
    V_line_input = st.number_input("線間電圧(V)", min_value=100.0, max_value=10000.0, value=6600.0, step=100.0)

with col_tp2:
    I_line = st.number_input("線電流(A)", min_value=1.0, max_value=500.0, value=100.0, step=1.0)

with col_tp3:
    pf_input = st.number_input("力率 cosθ", min_value=0.0, max_value=1.0, value=0.8, step=0.01, format="%.2f")

P_three = np.sqrt(3) * V_line_input * I_line * pf_input
S_three = np.sqrt(3) * V_line_input * I_line
Q_three = np.sqrt(max(S_three**2 - P_three**2, 0))

col_tp4, col_tp5, col_tp6 = st.columns(3)

with col_tp4:
    st.metric("三相有効電力 P [W]", f"{P_three:.2f}")

with col_tp5:
    st.metric("三相皮相電力 S [VA]", f"{S_three:.2f}")

with col_tp6:
    st.metric("三相無効電力 Q [var]", f"{Q_three:.2f}")

st.write("式: P = √3 × V × I × cosθ")

# -------------------------
# 整流
# -------------------------

st.header("整流（ダイオード）")

v_ac = V * np.sin(2 * np.pi * f * t)
v_rect = np.abs(v_ac)

fig3, ax3 = plt.subplots()
ax3.plot(t, v_ac, label="AC")
ax3.plot(t, v_rect, label="整流DC")
ax3.set_xlabel("時間 [s]")
ax3.set_ylabel("電圧")
ax3.grid(True)
ax3.legend()

st.pyplot(fig3)

# -------------------------
# トランス
# -------------------------

st.divider()
st.header("トランスシミュレータ")

col_tr1, col_tr2 = st.columns(2)

with col_tr1:
    V1 = st.number_input("一次電圧 V1", min_value=0.0, max_value=30000.0, value=22000.0, step=100.0)
    N1 = st.number_input("一次巻数 N1", min_value=1, max_value=500, value=100, step=1)

with col_tr2:
    N2 = st.number_input("二次巻数 N2", min_value=1, max_value=500, value=50, step=1)
    R_load = st.number_input("負荷抵抗", min_value=1.0, max_value=100.0, value=10.0, step=1.0)

V2 = V1 * (N2 / N1)
I2 = V2 / R_load
I1 = I2 * (N2 / N1)
V_line = np.sqrt(3) * V2

col_tr3, col_tr4 = st.columns(2)

with col_tr3:
    st.metric("二次電圧 V2", f"{V2:.4f}")
    st.metric("線間電圧", f"{V_line:.4f}")

with col_tr4:
    st.metric("二次電流 I2", f"{I2:.4f}")
    st.metric("一次電流 I1", f"{I1:.4f}")

# -------------------------
# 単線結線図エンジン（試作）
# -------------------------

st.divider()
st.header("単線結線図エンジン（試作）")

col_sw1, col_sw2, col_sw3 = st.columns(3)

with col_sw1:
    source_on = st.checkbox("電源ON", value=True)

with col_sw2:
    sw1_closed = st.checkbox("スイッチ1 CLOSED", value=True)

with col_sw3:
    sw2_closed = st.checkbox("スイッチ2 CLOSED", value=True)

bus_live = source_on
load1_live = bus_live and sw1_closed
load2_live = bus_live and sw2_closed

st.write("母線 BUS =", "活線" if bus_live else "非活線")
st.write("負荷1 =", "活線" if load1_live else "非活線")
st.write("負荷2 =", "活線" if load2_live else "非活線")

st.subheader("状態一覧")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("BUS", "活線" if bus_live else "非活線")

with col2:
    st.metric("負荷1", "活線" if load1_live else "非活線")

with col3:
    st.metric("負荷2", "活線" if load2_live else "非活線")
