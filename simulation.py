import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from agent import Agent


# ! DONT USE 
# ! EDIT /TEST FOLDER



# Simülasyon Parametreleri
grid_size = 128
num_agents = 960
step_size = 1
in_rects_count = 0

# Ajanları oluşturma
agents = [Agent(['Lx', 'Ly'], ["Mfd", "Mrn", "Mrv", "MX", "MY"]) for _ in range(num_agents)]
all_positions = {(agent.X, agent.Y) for agent in agents}

# Grafik ve yazı alanı için iki eksen oluşturma
fig, (ax, ax_text) = plt.subplots(1, 2, figsize=(8, 5), gridspec_kw={'width_ratios': [3, 1]})
ax.set_xlim(0, grid_size)
ax.set_ylim(0, grid_size)
scat = ax.scatter([agent.X for agent in agents], [agent.Y for agent in agents], s=2, color='blue')

# X ve Y eksenlerindeki numaraları gizle
ax.set_xticks([])
ax.set_yticks([])

# Yazı alanını ayarlama
ax_text.axis('off')
text = ax_text.text(0.1, 0.7, '', transform=ax_text.transAxes, va='center', ha='left', fontsize=12)

# Sağ tarafta yeşil dikdörtgen ekleme
background_rect = Rectangle((113, 0), 15, 128, facecolor=[88/255, 207/255, 57/255], alpha=0.5, fill=True, zorder=0)
background_rect1 = Rectangle((0, 0), 15, 128, facecolor=[88/255, 207/255, 57/255], alpha=0.5, fill=True, zorder=0)
ax.add_patch(background_rect)
ax.add_patch(background_rect1)

# Başlangıç statlarını ayarlama
current_frame = 0
text_template = "Frame: {}\nTotal Agents: {}\nGrid Size: {}x{}\nSurvived: {}"
text.set_text(text_template.format(current_frame, num_agents, grid_size, grid_size, in_rects_count))

# Güncelleme fonksiyonu
def update(frame):
    global agents, current_frame
    current_frame = frame

    # Her ajanın sinir ağını güncelle ve pozisyonunu değiştir
    for agent in agents:
        agent.update(all_positions)  # Neural network activation and position update

    # Yeni pozisyonları scatter grafiğine ayarla
    scat.set_offsets([(agent.X, agent.Y) for agent in agents])

    # Dikdörtgen içindeki ajanları say
    in_left_rect = sum((0 <= agent.X <= 15 and 0 <= agent.Y <= 128) for agent in agents)
    in_right_rect = sum((113 <= agent.X <= 128 and 0 <= agent.Y <= 128) for agent in agents)
    in_rects_count = in_left_rect + in_right_rect

    # Yazı alanındaki statları güncelle
    text.set_text(text_template.format(current_frame, num_agents, grid_size, grid_size, in_rects_count))

ani = FuncAnimation(fig, update, frames=200, interval=100)

plt.show()