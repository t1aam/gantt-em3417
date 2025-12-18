import matplotlib.pyplot as plt
from collections import defaultdict

# ========= 1) Khai báo màu theo NGUYÊN CÔNG (giữ nhất quán 2 hình) =========
COL = {
    "C1": "#8ecae6",
    "C2": "#219ebc",
    "C3": "#023047",
    "C4": "#ffb703",
    "C5": "#fb8500",
    "B1": "#90dbf4",
    "B2": "#cdb4db",
    "B3": "#ffc8dd",
    "R":  "#f1faee",
    "HC": "#e63946",
}

# ========= 2) Lập lịch theo BOM để ra CHU KỲ 26 GIỜ =========
# Ghi chú: do BOM thực tế cần lặp C1/C2/B1 nhiều lần, mình đặt tên instance (C1_1, C1_2,...)
# Lịch này là "earliest-start" (có thể làm song song, chưa xét giới hạn 5 CN).
tasks = [
    # name, op, start, dur, workers
    ("C1_1", "C1", 0, 8, 1),
    ("C2_1", "C2", 0, 8, 1),

    ("C1_2", "C1", 0, 8, 1),
    ("C2_2", "C2", 0, 8, 1),

    ("C1_3", "C1", 0, 8, 1),
    ("C2_3", "C2", 0, 8, 1),

    ("C1_4", "C1", 0, 8, 1),  # C1 riêng cho B2 (ngoài C1 nằm trong B1)

    ("C3_1", "C3", 0, 10, 1),
    ("C4_1", "C4", 0, 4, 1),
    ("C5_1", "C5", 0, 5, 1),

    ("B1_1", "B1", 8, 2, 2),   # từ C1_1 + C2_1
    ("B1_2", "B1", 8, 2, 2),   # từ C1_2 + C2_2
    ("B1_3", "B1", 8, 2, 2),   # từ C1_3 + C2_3

    ("B2_1", "B2", 10, 6, 1),  # từ B1_2 + C1_4
    ("B3_1", "B3", 10, 9, 2),  # từ B1_3 + C3_1

    ("R_1",  "R",  19, 5, 2),  # từ B1_1 + B2_1 + B3_1 + C4_1 + C5_1
    ("HC_1", "HC", 24, 2, 1),  # hoàn thiện
]

T_END = max(s + d for _, _, s, d, _ in tasks)  # phải ra 26

# ========= 3) HÌNH 1: Gantt theo THỜI GIAN (mỗi thanh là 1 instance) =========
fig1, ax1 = plt.subplots(figsize=(12, 6))

# vẽ từ trên xuống cho dễ nhìn
y_labels = [name for name, *_ in tasks]
y_pos = list(range(len(tasks)))[::-1]

for (y, (name, op, start, dur, workers)) in zip(y_pos, tasks):
    ax1.barh(
        y=y,
        width=dur,
        left=start,
        height=0.7,
        color=COL[op],
        edgecolor="black"
    )
    ax1.text(start + dur/2, y, f"{op} ({dur}h, {workers}CN)",
             ha="center", va="center", fontsize=8)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(y_labels, fontsize=8)
ax1.set_xlim(0, T_END)
ax1.set_xlabel("Thời gian (giờ)")
ax1.set_title("7.2a – Sơ đồ Gantt theo thời gian (tiến độ lắp ráp sản phẩm R)")
ax1.grid(axis="x", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()


# ========= 4) HÌNH 2: Gantt theo NHÂN LỰC (stack theo nguyên công, giữ màu theo op) =========
# Chia trục thời gian theo các mốc thay đổi (start/end của mọi task)
cut_points = sorted(set([0] + [s for _, _, s, _, _ in tasks] + [s+d for _, _, s, d, _ in tasks]))
segments = [(cut_points[i], cut_points[i+1]) for i in range(len(cut_points)-1)]

# Với mỗi đoạn (a,b), tính công nhân đang chạy theo từng op
seg_op_workers = []
for a, b in segments:
    w_by_op = defaultdict(float)
    for _, op, s, d, w in tasks:
        e = s + d
        # task active nếu đoạn [a,b] nằm trong [s,e]
        if a >= s and b <= e:
            w_by_op[op] += w
    seg_op_workers.append((a, b, dict(w_by_op)))

fig2, ax2 = plt.subplots(figsize=(12, 6))

# vẽ stacked rectangle theo từng đoạn thời gian, màu theo op
for a, b, w_by_op in seg_op_workers:
    bottom = 0
    for op, w in w_by_op.items():
        ax2.bar(
            x=a,
            height=w,
            width=b - a,
            bottom=bottom,
            align="edge",
            color=COL[op],
            edgecolor="black",
            linewidth=0.6
        )
        bottom += w

    # ghi tổng CN của đoạn
    if bottom > 0:
        ax2.text(a + (b-a)/2, bottom/2, f"{int(bottom)} CN",
                 ha="center", va="center", fontsize=8)

# đường ngang đậm (giới hạn 5 CN – dùng cho 7.4)
ax2.axhline(y=5, color="darkblue", linewidth=3)

ax2.set_xlim(0, T_END)
ax2.set_xlabel("Thời gian (giờ)")
ax2.set_ylabel("Số công nhân")
ax2.set_title("7.2b – Sơ đồ Gantt theo nhu cầu nhân lực (màu theo nguyên công)")
ax2.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.show()

print("Tổng thời gian chu kỳ (giờ):", T_END)
