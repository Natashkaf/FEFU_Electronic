import json
import os
from settings import *

class Results:
    def __init__(self):
        self.results_file = "results.json"
        self.results = []
        self.load_results()
    
    def load_results(self):
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r') as f:
                    self.results = json.load(f)
            except:
                self.results = []
        else:
            self.results = []
    
    def save_results(self):
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f)
    
    def add_result(self, rau_score):
        self.results.append(rau_score)
        self.results = sorted(self.results, reverse=True)[:10]
        self.save_results()
    
    def get_top_results(self, count=10):
        return self.results[:count]