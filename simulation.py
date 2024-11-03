import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from Agent import Agent
import random
import time

# Simülasyon Parametreleri 64^2 = 4096
grid_size = 64
num_agents = 240 # ! Normal = 240 
in_rects_count = 0
grid = [[0 for _ in range(64)] for _ in range(64)]
generation = 0

# Ajanları oluşturma
agents = [Agent(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1), grid=grid) for _ in range(num_agents)]
all_positions = {(agent.X, agent.Y) for agent in agents}

def reset_generation():
    """Yeni bir jenerasyona geçiş için ajanları sıfırla."""
    global agents, grid, generation
    generation += 1
    print(f"Yeni Jenerasyon: {generation}")
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    agents = [Agent(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1), grid=grid) for _ in range(num_agents)]

# Gerçek simülasyon verilerini hesaplayan yardımcı fonksiyonlar
def calculate_blockage(agent, direction):
    if direction == "forward":
        if agent.X == 63: return 0
        elif agent.grid[agent.Y][agent.X + 1] == 1: return 0 
        else: return 1

def calculate_population_gradient(agent):
    """Agent'ın çevresindeki diğer agent'ların yoğunluğunu hesaplar."""
    left_count = sum(1 for a in agents if a.X < agent.X)
    right_count = sum(1 for a in agents if a.X > agent.X)
    forward_count = sum(1 for a in agents if a.Y > agent.Y)
    
    # Sol-sağ gradyan ve ileri gradyan
    plr = right_count - left_count
    pfd = forward_count
    return plr / num_agents * 8, pfd / num_agents * 8  # Normalize et

# region Set and Creat Fig

# Grafik ve yazı alanı için iki eksen oluşturma
fig, (ax, ax_text) = plt.subplots(1, 2, figsize=(8, 5), gridspec_kw={'width_ratios': [3, 1]})
ax.set_xlim(-1, grid_size)
ax.set_ylim(-1, grid_size)
scat = ax.scatter([agent.X for agent in agents], [agent.Y for agent in agents], s=2, color='blue')

# X ve Y eksenlerindeki numaraları gizle
ax.set_xticks([])
ax.set_yticks([])

# Yazı alanını ayarlama
ax_text.axis('off')
text = ax_text.text(0.1, 0.7, '', transform=ax_text.transAxes, va='center', ha='left', fontsize=12)

# Sağ tarafta yeşil dikdörtgen ekleme
background_rect = Rectangle((60, -1), 4, grid_size+1, facecolor=[88/255, 207/255, 57/255], alpha=0.5, fill=True, zorder=0)
background_rect1 = Rectangle((-1,-1), 4, grid_size+1, facecolor=[88/255, 207/255, 57/255], alpha=0.5, fill=True, zorder=0)
ax.add_patch(background_rect)
ax.add_patch(background_rect1)

# Başlangıç statlarını ayarlama
current_frame = 0
text_template = "Frame: {}\nTotal Agents: {}\nGrid Size: {}x{}\nSurvived: {}"
text.set_text(text_template.format(current_frame, num_agents, grid_size, grid_size, in_rects_count))

# endregion

# Simülasyonu durdurma fonksiyonu
def on_key(event):
    if event.key == 'q':  # 'q' tuşuna basıldığında
        print("SIMULATION CLOSED (key_event)")
        plt.close()  # Tüm plotları kapat ve programı sonlandır


# Güncelleme fonksiyonu
def update(frame):
    global agents, current_frame, in_rects_count
    current_frame = frame
    #time.sleep(0.07)

    if frame >= 200: 
        reset_generation() 
        return


    # Her ajanın sinir ağını güncelle ve pozisyonunu değiştir
    for agent in agents:
        from Simulation import grid
        # Set creature positions

        agent.grid = grid

        # Gerçek simülasyon verilerini hesapla
        plr, pfd = calculate_population_gradient(agent)


        simulation_data = {
            'Age': (frame - 100) / 100,  # -4.0 => frame 0; 4.0 => frame 200
            'Plr': plr,
            'Pfd': pfd,
            'LMy': agent.last_move_y,
            'LMx': agent.last_move_x,
            'BDy': agent.Y / (grid_size - agent.Y),  # Kuzey-güney sınır mesafesi
            'BDx': agent.X / (grid_size - agent.X),  # Doğu-batı sınır mesafesi
            'BDd': min(agent.Y, grid_size - agent.Y, agent.X, grid_size - agent.X),  # En yakın sınır mesafesi
            'LPf': calculate_blockage(agent, "forward"),
            'Lx': (agent.X - (grid_size // 2) / 32),
            'Ly': (agent.Y - (grid_size // 2) / 32),
            'Rnd': random.uniform(-1, 1),
        }
        agent.update(simulation_data)
        grid = agent.grid # Neural network aktivasyonu ve pozisyon güncellemesi

        agent.survived = agent.X <= 4 or agent.X >= 60

    # Yeni pozisyonları scatter grafiğine ayarla
    scat.set_offsets([(agent.X, agent.Y) for agent in agents])

    in_rects_count = sum(agent.survived == True for agent in agents)

    # Yazı alanındaki statları güncelle
    text.set_text(text_template.format(current_frame, num_agents, grid_size, grid_size, in_rects_count))


fig.canvas.mpl_connect('key_press_event', on_key)


# Animasyonu oluştur
ani = FuncAnimation(fig, update, frames=200, interval=100)

# Grafiği göster
plt.show()