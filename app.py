import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("電気シミュレータ")

# -------------------------
# RLCパラメータ
# -------------------------

st.header("RLC回路")

V = st.slider("電圧(V)", 0, 500, 100)
f = st.slider("周波数(Hz)", 1, 100, 50)
R = st.slider("抵抗(Ω)", 1, 100, 10)
L = st.slider("コイル(H)", 0.001, 1.0, 0.1)
C = st.slider("コンデンサ(F)", 0.000001, 0.01, 0.001)

XL = 2*np.pi*f*L
XC = 1/(2*np.pi*f*C)

Z = np.sqrt(R**2 + (XL-XC)**2)
I = V/Z

st.write("インピーダンス Z =", Z)
st.write("電流 I =", I)

# -------------------------
# 位相と力率
# -------------------------

theta = np.arctan((XL-XC)/R)
pf = np.cos(theta)

st.write("位相角 θ =", theta)
st.write("力率 cosθ =", pf)

# -------------------------
# 電力
# -------------------------

P = V * I * pf
S = V * I
Q = V * I * np.sin(theta)

st.write("有効電力 P =", P)
st.write("皮相電力 S =", S)
st.write("無効電力 Q =", Q)

# -------------------------
# 共振
# -------------------------

f_res = 1/(2*np.pi*np.sqrt(L*C))
st.write("共振周波数 =", f_res)

# -------------------------
# 電圧・電流波形
# -------------------------

st.subheader("電圧と電流の波形")

t = np.linspace(0,0.1,1000)

v = V*np.sin(2*np.pi*f*t)
i = I*np.sin(2*np.pi*f*t - theta)

fig, ax = plt.subplots()

ax.plot(t, v, label="電圧")
ax.plot(t, i, label="電流")

ax.legend()

st.pyplot(fig)

st.subheader("フェーザ図")

fig_ph, ax_ph = plt.subplots()

# 原点からのベクトルを描画
ax_ph.quiver(0, 0, 1, 0, angles='xy', scale_units='xy', scale=1, color='blue')
ax_ph.text(1.05, 0, "V", color='blue')

ax_ph.quiver(0, 0, np.cos(theta), -np.sin(theta), angles='xy', scale_units='xy', scale=1, color='red')
ax_ph.text(np.cos(theta)*1.05, -np.sin(theta)*1.05, "I", color='red')

# 見やすさ調整
ax_ph.set_xlim(-1.5, 1.5)
ax_ph.set_ylim(-1.5, 1.5)
ax_ph.axhline(0, color='gray', linewidth=0.5)
ax_ph.axvline(0, color='gray', linewidth=0.5)
ax_ph.set_aspect('equal')
ax_ph.grid(True)

st.pyplot(fig_ph)

# -------------------------
# 三相交流
# -------------------------

st.divider()
st.header("三相交流")

v_a = V*np.sin(2*np.pi*f*t)
v_b = V*np.sin(2*np.pi*f*t - 2*np.pi/3)
v_c = V*np.sin(2*np.pi*f*t - 4*np.pi/3)

fig2, ax2 = plt.subplots()

ax2.plot(t, v_a, label="A相")
ax2.plot(t, v_b, label="B相")
ax2.plot(t, v_c, label="C相")

ax2.legend()

st.pyplot(fig2)

# -------------------------
# 整流
# -------------------------

st.header("整流（ダイオード）")

v_ac = V*np.sin(2*np.pi*f*t)
v_rect = np.abs(v_ac)

fig3, ax3 = plt.subplots()

ax3.plot(t, v_ac, label="AC")
ax3.plot(t, v_rect, label="整流DC")

ax3.legend()

st.pyplot(fig3)

# -------------------------
# トランス
# -------------------------

st.divider()
st.header("トランスシミュレータ")

V1 = st.slider("一次電圧 V1", 0, 30000, 22000, step=100)
N1 = st.slider("一次巻数 N1", 1, 500, 100)
N2 = st.slider("二次巻数 N2", 1, 500, 50)
R_load = st.slider("負荷抵抗", 1, 100, 10)

V2 = V1 * (N2/N1)

I2 = V2 / R_load
I1 = I2 * (N2/N1)

V_line = np.sqrt(3) * V2

st.write("二次電圧 V2 =", V2)
st.write("線間電圧 =", V_line)
st.write("二次電流 I2 =", I2)
st.write("一次電流 I1 =", I1)

st.divider()
st.header("単線結線図エンジン（試作）")

source_on = st.checkbox("電源ON", value=True)
sw1_closed = st.checkbox("スイッチ1 CLOSED", value=True)
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
