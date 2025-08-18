"""
Soccer Score Predictor - English Premier League
"""
import tkinter as tk
from tkinter import ttk, messagebox


import requests
import pandas as pd
import numpy as np


# --- Data Fetching ---
def fetch_epl_fixtures():
    """Fetch upcoming EPL fixtures from football-data.org API."""
    API_KEY = "fe0d30ce7478494a9222ff4877b9449e"  # User's API key
    url = "https://api.football-data.org/v4/competitions/PL/matches?status=SCHEDULED"
    headers = {"X-Auth-Token": API_KEY}
    fixtures = []
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            for match in data.get("matches", []):
                home = match["homeTeam"]["name"]
                away = match["awayTeam"]["name"]
                fixtures.append((home, away))
        else:
            print("Error fetching fixtures:", resp.text)
    except Exception as e:
        print("Exception fetching fixtures:", e)
    return fixtures

# --- Fetch Past Results for Teams ---
def fetch_team_recent_stats():
    """Fetch recent EPL match results and compute team stats."""
    API_KEY = "fe0d30ce7478494a9222ff4877b9449e"
    url = "https://api.football-data.org/v4/competitions/PL/matches?status=FINISHED"
    headers = {"X-Auth-Token": API_KEY}
    team_stats = {}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            for match in data.get("matches", []):
                home = match["homeTeam"]["name"]
                away = match["awayTeam"]["name"]
                home_score = match["score"]["fullTime"]["home"]
                away_score = match["score"]["fullTime"]["away"]
                # Home team stats
                if home not in team_stats:
                    team_stats[home] = {"scored": [], "conceded": []}
                team_stats[home]["scored"].append(home_score)
                team_stats[home]["conceded"].append(away_score)
                # Away team stats
                if away not in team_stats:
                    team_stats[away] = {"scored": [], "conceded": []}
                team_stats[away]["scored"].append(away_score)
                team_stats[away]["conceded"].append(home_score)
        else:
            print("Error fetching past results:", resp.text)
    except Exception as e:
        print("Exception fetching past results:", e)
    return team_stats

# --- Prediction Model (Simple) ---
def predict_score(home, away, team_stats):
    """Predict score using average goals scored/conceded in last 5 matches."""
    home_scored = team_stats.get(home, {"scored": [1]} )["scored"][-5:]
    home_conceded = team_stats.get(home, {"conceded": [1]} )["conceded"][-5:]
    away_scored = team_stats.get(away, {"scored": [1]} )["scored"][-5:]
    away_conceded = team_stats.get(away, {"conceded": [1]} )["conceded"][-5:]
    home_pred = (np.mean(home_scored) + np.mean(away_conceded)) / 2
    away_pred = (np.mean(away_scored) + np.mean(home_conceded)) / 2
    return int(round(home_pred)), int(round(away_pred))

# --- GUI ---
class SoccerScorePredictor:
    def __init__(self, root):
        """Initialize Soccer Score Predictor GUI."""
        self.root = root
        self.root.title("Soccer Score Predictor - EPL")
        self.root.geometry("500x400")
        self.root.configure(bg="#eaf6fb")
        self.title = tk.Label(root, text="EPL Soccer Score Predictor", font=("Arial", 18, "bold"), bg="#eaf6fb")
        self.title.pack(pady=10)
        self.refresh_btn = tk.Button(root, text="Fetch Fixtures", command=self.load_fixtures)
        self.refresh_btn.pack(pady=5)
        self.fixtures_list = tk.Listbox(root, font=("Arial", 12), width=40, height=10)
        self.fixtures_list.pack(pady=10)
        self.predict_btn = tk.Button(root, text="Predict Score", command=self.predict_selected)
        self.predict_btn.pack(pady=5)
        self.result_label = tk.Label(root, text="", font=("Arial", 14), bg="#eaf6fb")
        self.result_label.pack(pady=10)
        self.fixtures = []
        self.team_stats = fetch_team_recent_stats()
        self.load_fixtures()

    def load_fixtures(self):
        self.fixtures_list.delete(0, tk.END)
        self.fixtures = fetch_epl_fixtures()
        for home, away in self.fixtures:
            self.fixtures_list.insert(tk.END, f"{home} vs {away}")

    def predict_selected(self):
        idx = self.fixtures_list.curselection()
        if not idx:
            messagebox.showwarning("Select Match", "Please select a fixture.")
            return
        home, away = self.fixtures[idx[0]]
        home_score, away_score = predict_score(home, away, self.team_stats)
        self.result_label.config(text=f"Prediction: {home} {home_score} - {away_score} {away}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SoccerScorePredictor(root)
    root.mainloop()
