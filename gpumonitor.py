import gpustat
import time
import threading
#code for gpu data
class GPUMonitor:
    def __init__(self, max_data_points=360, http_listen=False, http_endpoint=None):
        self.max_data_points = max_data_points
        self.gpu_usage_data = [0] * max_data_points
        self.gpu_temp_data = [0] * max_data_points
        self.http_listen = http_listen
        self.http_endpoint = http_endpoint

    def get_gpu_stats(self):
        if not(self.http_listen):
          gpu_stats = gpustat.GPUStatCollection.new_query().gpus[0]
          gpu_usage = gpu_stats.utilization
          gpu_temp = gpu_stats.temperature
          return gpu_usage, gpu_temp

    def update_gpu_stats(self):
        while True:
            gpu_usage, gpu_temp = self.get_gpu_stats()
            self.gpu_usage_data.append(gpu_usage)
            self.gpu_temp_data.append(gpu_temp)
            if len(self.gpu_usage_data) > self.max_data_points:
                self.gpu_usage_data.pop(0)
                self.gpu_temp_data.pop(0)
            time.sleep(5)

    def start_monitoring(self):
        monitoring_thread = threading.Thread(target=self.update_gpu_stats)
        monitoring_thread.daemon = True
        monitoring_thread.start()