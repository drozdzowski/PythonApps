import math
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
    head_to_head = {}
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
                    team_stats[home] = {"scored": [], "conceded": [], "home_scored": [], "home_conceded": [], "away_scored": [], "away_conceded": []}
                team_stats[home]["scored"].append(home_score)
                team_stats[home]["conceded"].append(away_score)
                team_stats[home]["home_scored"].append(home_score)
                team_stats[home]["home_conceded"].append(away_score)
                # Away team stats
                if away not in team_stats:
                    team_stats[away] = {"scored": [], "conceded": [], "home_scored": [], "home_conceded": [], "away_scored": [], "away_conceded": []}
                team_stats[away]["scored"].append(away_score)
                team_stats[away]["conceded"].append(home_score)
                team_stats[away]["away_scored"].append(away_score)
                team_stats[away]["away_conceded"].append(home_score)
                # Head-to-head
                h2h_key = tuple(sorted([home, away]))
                if h2h_key not in head_to_head:
                    head_to_head[h2h_key] = []
                head_to_head[h2h_key].append((home, away, home_score, away_score))
        else:
            print("Error fetching past results:", resp.text)
    except Exception as e:
        print("Exception fetching past results:", e)
    return team_stats, head_to_head

# --- Prediction Model (Simple) ---

def safe_mean(arr, default=1):
    m = np.mean(arr) if arr else default
    return m if not math.isnan(m) else default

def weighted_mean(arr, weights=None, default=1):
    if not arr:
        return default
    arr = np.array(arr)
    if weights is None:
        weights = np.linspace(1, 2, len(arr))  # More weight to recent
    weights = np.array(weights)
    if len(weights) != len(arr):
        weights = np.ones(len(arr))
    m = np.average(arr, weights=weights)
    return m if not math.isnan(m) else default

def predict_score(home, away, team_stats, head_to_head):
    """Improved prediction: weighted recent form, home/away, goal diff, clean sheets, head-to-head."""
    home_form = team_stats.get(home, {"scored": [1], "conceded": [1], "home_scored": [1], "home_conceded": [1], "away_scored": [1], "away_conceded": [1]})
    away_form = team_stats.get(away, {"scored": [1], "conceded": [1], "home_scored": [1], "home_conceded": [1], "away_scored": [1], "away_conceded": [1]})
    # Weighted last 5 matches
    home_scored = home_form["home_scored"][-5:]
    home_conceded = home_form["home_conceded"][-5:]
    away_scored = away_form["away_scored"][-5:]
    away_conceded = away_form["away_conceded"][-5:]
    weights = np.linspace(1, 2, 5)[-len(home_scored):]
    # Goal difference
    home_goal_diff = [s-c for s, c in zip(home_form["scored"][-5:], home_form["conceded"][-5:])]
    away_goal_diff = [s-c for s, c in zip(away_form["scored"][-5:], away_form["conceded"][-5:])]
    # Clean sheets
    home_clean_sheets = sum(1 for c in home_conceded if c == 0)
    away_clean_sheets = sum(1 for c in away_conceded if c == 0)
    # Head-to-head (last 3, weighted)
    h2h_key = tuple(sorted([home, away]))
    h2h_matches = head_to_head.get(h2h_key, [])[-3:]
    h2h_home = [m[2] for m in h2h_matches if m[0] == home]
    h2h_away = [m[3] for m in h2h_matches if m[1] == away]
    h2h_weights = np.linspace(1, 2, len(h2h_home)) if h2h_home else None
    # Calculate prediction
    # Scale up all components to allow higher scores
    scale = 1.7
    home_pred = scale * (
        0.35 * weighted_mean(home_form["scored"][-5:], weights) +
        0.20 * weighted_mean(home_scored, weights) +
        0.10 * weighted_mean(home_goal_diff, weights) +
        0.10 * home_clean_sheets +
        0.15 * (weighted_mean(h2h_home, h2h_weights) if h2h_home else weighted_mean(home_scored, weights))
    )
    away_pred = scale * (
        0.35 * weighted_mean(away_form["scored"][-5:], weights) +
        0.20 * weighted_mean(away_scored, weights) +
        0.10 * weighted_mean(away_goal_diff, weights) +
        0.10 * away_clean_sheets +
        0.15 * (weighted_mean(h2h_away, h2h_weights) if h2h_away else weighted_mean(away_scored, weights))
    )
    # Draw logic: if teams are very close, increase draw probability
    if abs(home_pred - away_pred) < 0.3:
        home_pred = away_pred = round((home_pred + away_pred) / 2)
    return int(round(home_pred)), int(round(away_pred))

# --- GUI ---
class SoccerScorePredictor:
    def __init__(self, root):
        import random
        self.root = root
        self.root.title("Soccer Score Predictor - EPL")
        self.root.geometry("975x750")
        pastel_colors = ["#eaf6fb", "#ffe4e1", "#e0ffe0", "#fffbe0", "#e0eaff", "#fbeaf6"]
        bg_color = random.choice(pastel_colors)
        self.root.configure(bg=bg_color)

        self.title = tk.Label(root, text="EPL Soccer Score Predictor", font=("Arial", 20, "bold"), bg=bg_color)
        self.title.pack(pady=10)

        main_frame = tk.Frame(root, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        left_frame = tk.Frame(main_frame, bg=bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame = tk.Frame(main_frame, bg=bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.refresh_btn = tk.Button(left_frame, text="Fetch Fixtures", command=self.load_fixtures, font=("Arial", 12))
        self.refresh_btn.pack(pady=5)

        self.fixtures_list = tk.Listbox(left_frame, font=("Arial", 12), width=35, height=15)
        self.fixtures_list.pack(pady=10, fill=tk.BOTH, expand=True)

        self.predict_btn = tk.Button(left_frame, text="Predict Score", command=self.predict_selected, font=("Arial", 12, "bold"), bg="#b3e6ff")
        self.predict_btn.pack(pady=5)

        self.result_label = tk.Label(left_frame, text="", font=("Arial", 16, "bold"), bg=bg_color, fg="#333")
        self.result_label.pack(pady=10)

        # Team stats summary panel
        self.stats_title = tk.Label(right_frame, text="Team Stats (Last 5 Matches)", font=("Arial", 14, "bold"), bg=bg_color)
        self.stats_title.pack(pady=5)
        self.stats_text = tk.Text(right_frame, font=("Arial", 12), width=30, height=15, bg="#f7f7fa", fg="#222")
        self.stats_text.pack(pady=10, fill=tk.BOTH, expand=True)
        self.stats_text.config(state=tk.DISABLED)

        self.fixtures = []
        self.team_stats, self.head_to_head = fetch_team_recent_stats()
        self.load_fixtures()

    def load_fixtures(self):
        self.fixtures_list.delete(0, tk.END)
        all_fixtures = fetch_epl_fixtures()
        # Only show the next upcoming game for each team
        seen_teams = set()
        unique_fixtures = []
        self.prediction_cache = {}  # Cache predictions for performance
        for home, away in all_fixtures:
            if home not in seen_teams and away not in seen_teams:
                unique_fixtures.append((home, away))
                seen_teams.add(home)
                seen_teams.add(away)
        self.fixtures = unique_fixtures
        for home, away in self.fixtures:
            # Calculate prediction for display and cache
            home_score, away_score = predict_score(home, away, self.team_stats, self.head_to_head)
            self.prediction_cache[(home, away)] = (home_score, away_score)
            self.fixtures_list.insert(tk.END, f"{home} vs {away} ({home_score}-{away_score})")
        self.result_label.config(text="")
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.config(state=tk.DISABLED)

    def predict_selected(self):
        idx = self.fixtures_list.curselection()
        if not idx:
            messagebox.showwarning("Select Match", "Please select a fixture.")
            return
        home, away = self.fixtures[idx[0]]
        # Use cached prediction for performance
        home_score, away_score = self.prediction_cache.get((home, away), predict_score(home, away, self.team_stats, self.head_to_head))
        self.result_label.config(text=f"Prediction: {home} {home_score} - {away_score} {away}")
        # Show team stats summary
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        home_stats = self.team_stats.get(home, {"scored": [], "conceded": [], "home_scored": [], "away_scored": []})
        away_stats = self.team_stats.get(away, {"scored": [], "conceded": [], "home_scored": [], "away_scored": []})
        def stats_str(name, stats):
            scored = stats["scored"][-5:]
            home_scored = stats["home_scored"][-5:] if "home_scored" in stats else []
            away_scored = stats["away_scored"][-5:] if "away_scored" in stats else []
            conceded = stats["conceded"][-5:]
            return f"{name}\n  Scored: {scored}\n  Home Scored: {home_scored}\n  Away Scored: {away_scored}\n  Conceded: {conceded}\n"
        self.stats_text.insert(tk.END, stats_str(home, home_stats))
        self.stats_text.insert(tk.END, "\n")
        self.stats_text.insert(tk.END, stats_str(away, away_stats))
        self.stats_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SoccerScorePredictor(root)
    root.mainloop()
