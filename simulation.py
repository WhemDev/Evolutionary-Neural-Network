import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from Agent import Agent
import random
import os
import Generation



# Simülasyon Parametreleri 64^2 = 4096
grid_size = 64
num_agents = 240 # ! Normal = 240 
in_rects_count = 0
grid = [[0 for _ in range(64)] for _ in range(64)]
generation = 0

# Ajanları oluşturma
agents = [Agent(random.randint(3, 61), random.randint(0, grid_size - 1), grid=grid) for _ in range(num_agents)]
all_positions = {(agent.X, agent.Y) for agent in agents}

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
fig, (ax, ax_text) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1.5, 1.5]})
ax.set_xlim(-1, grid_size)
ax.set_ylim(-1, grid_size)
scat = ax.scatter([agent.X for agent in agents], [agent.Y for agent in agents], s=2, color='blue')

# X ve Y eksenlerindeki numaraları gizle
ax.set_xticks([])
ax.set_yticks([])

# Yazı alanını ayarlama
ax_text.axis('off')
text = ax_text.text(0.1, 0.7, '', transform=ax_text.transAxes, va='center_baseline', ha='left', fontsize=10)
plt.subplots_adjust(left=0.05, right=0.85, top=0.95, bottom=0.05, wspace=0.1)


# Sağ tarafta yeşil dikdörtgen ekleme
background_rect = Rectangle((60, -1), 4, grid_size+1, facecolor=[88/255, 207/255, 57/255], alpha=0.5, fill=True, zorder=0)
background_rect1 = Rectangle((-1,-1), 4, grid_size+1, facecolor=[88/255, 207/255, 57/255], alpha=0.5, fill=True, zorder=0)
ax.add_patch(background_rect)
ax.add_patch(background_rect1)

# Başlangıç statlarını ayarlama
current_frame = 0
targetAgent = None
text_template = "GENERATION: {}\n\nFrame: {}\nTotal Agents: {}\nGrid Size: {}x{}\nSurvived: {}\n\nClose Fig: 'q'\nStart/Pause: 'e'\n\nTarget Agent:\n{}"
text.set_text(text_template.format(generation, current_frame, num_agents, grid_size, grid_size, in_rects_count, targetAgent))

# endregion

# Simülasyonu durdurma fonksiyonu
def on_key(event):
    if event.key == 'q':  # 'q' tuşuna basıldığında
        print("SIMULATION CLOSED (key_event)")
        plt.close()  # Tüm plotları kapat ve programı sonlandır



def on_Fig_click(event):
    global targetAgent
    # event.xdata ve event.ydata tıklanan yerin koordinatlarını verir
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        print(f"Tıklanan yerin koordinatları: x = {x}, y = {y}")

        for agent in agents:
            if (agent.X == x) and (agent.Y == y):
                targetAgent = agent 
                


pause = False
def onClick(event):
    global pause
    print('event')
    if (event.key == "e") and (pause == False):
        print("SIMULATION STOPPED")
        pause = True
        ani.event_source.stop()
    elif (event.key == "e") and (pause == True):
        print("SIMULATION STOPPED")
        pause = False
        ani.event_source.start()

def log(generation, agents, count):
    file_path = f'log/GenerationData/generation{generation}.txt'

    # Dosyayı yazma modunda ('w') açmak
    num = 1
    with open(file_path, 'w') as file:
        file.write(f"GENERATION : {generation}\n")
        file.write(f"Survived Count : {count}\n\n\n")
        for agent in agents:
            if agent.survived:
                file.write(f"{num}-\n{agent.genome}\n\n")
                num += 1

    file_path = f'log/surviveCount.txt'
    with open(file_path, 'a') as file:
        file.write(f"{count}\n")
    



# Güncelleme fonksiyonu
def update(frame):
    global agents, current_frame, in_rects_count, generation, targetAgent
    current_frame = frame
    #time.sleep(0.07)

    if (frame % 100 == 0) and (frame > 50): 
        print("STARTED NEW GENERATION")
        print(generation)
        log(generation, agents, in_rects_count)

        if not os.path.exists('generation_images'):
            os.makedirs('generation_images')
        plt.savefig(f'generation_images/generation_{generation}.png')

        generation += 1
        frame=0
        current_frame = 0
        grid = [[0 for _ in range(64)] for _ in range(64)]
        agents = Generation.create_new_generation(agents, grid)


    # Her ajanın sinir ağını güncelle ve pozisyonunu değiştir
    for agent in agents:
        from Simulation import grid
        # Set creature positions

        agent.grid = grid

        # Gerçek simülasyon verilerini hesapla
        plr, pfd = calculate_population_gradient(agent)


        simulation_data = {
            'Age': (frame - 50) / 50,  # -4.0 => frame 0; 4.0 => frame 200
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

        agent.survived = (agent.X <= 4) or (agent.X >= 60)

    # Yeni pozisyonları scatter grafiğine ayarla
    scat.set_offsets([(agent.X, agent.Y) for agent in agents])

    in_rects_count = sum(agent.survived == True for agent in agents)

    # Yazı alanındaki statları güncelle
    if targetAgent is not None:
        text.set_text(text_template.format(generation, current_frame, num_agents, grid_size, grid_size, in_rects_count, targetAgent.genome))
    else:
        text.set_text(text_template.format(generation, current_frame, num_agents, grid_size, grid_size, in_rects_count, targetAgent))


fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('key_press_event', onClick)
fig.canvas.mpl_connect('key_press_event', on_Fig_click)


# Animasyonu oluştur
ani = FuncAnimation(fig, update, frames=200000, interval=100)
# Grafiği göster
plt.show()