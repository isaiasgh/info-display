import pygame
import matplotlib.pyplot as plt
import numpy as np
import threading
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Constants
TIME_SERIES_LIMIT = -350
TIME_SERIES_START = 0
GPU_USAGE_LIMIT = 100
GPU_TEMP_LIMIT = 110
DEFAULT_FIGSIZE = (8, 4)

class GPUPlot:
    def __init__(self, num_gpus, figsize=DEFAULT_FIGSIZE):
        self.num_gpus = num_gpus
        self.fig, self.ax = plt.subplots(2, 1, figsize=figsize)
        self.canvas = FigureCanvasAgg(self.fig)
        self.surface = None
        self.lock = threading.Lock()
        self.colors = plt.cm.rainbow(np.linspace(0, 1, num_gpus))

    def _configure_usage_graph(self):
        self.ax[0].set_ylim(0, GPU_USAGE_LIMIT)
        self.ax[0].set_xlim(TIME_SERIES_LIMIT, TIME_SERIES_START)
        self.ax[0].set_ylabel('Usage (%)')
        self.ax[0].grid()
        self.ax[0].legend()

    def _configure_temp_graph(self):
        self.ax[1].set_ylim(10, GPU_TEMP_LIMIT)
        self.ax[1].set_xlim(TIME_SERIES_LIMIT, TIME_SERIES_START)
        self.ax[1].set_ylabel('Temperature (C)')
        self.ax[1].grid()
        self.ax[1].legend()

    def _update_graph(self, time_series, gpu_monitor):
        for i in range(self.num_gpus):
            self.ax[0].plot(time_series, gpu_monitor.gpu_usage_data[i], 
                            label=f'GPU{i} Usage (%)', color=self.colors[i])
            self.ax[1].plot(time_series, gpu_monitor.gpu_temp_data[i], 
                            label=f'GPU{i} Temp (C)', color=self.colors[i])

    def update(self, gpu_monitor):
        time_series = np.arange(-len(gpu_monitor.gpu_usage_data[0]), 0)
        
        self.ax[0].clear()
        self.ax[1].clear()

        self._update_graph(time_series, gpu_monitor)
        self._configure_usage_graph()
        self._configure_temp_graph()

        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()
        raw_data = self.canvas.buffer_rgba()
        size = self.canvas.get_width_height()
        with self.lock:
            self.surface = pygame.image.frombuffer(raw_data, size, "RGBA").convert()

def gpu_monitoring_thread(gpu_monitor, gpu_plot, update_interval, running):
    gpu_graph_update_timer = 0
    while running:
        current_time = pygame.time.get_ticks()
        if current_time - gpu_graph_update_timer >= update_interval:
            gpu_graph_update_timer = current_time
            gpu_plot.update(gpu_monitor)
        pygame.time.wait(100)