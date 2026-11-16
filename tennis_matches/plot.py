import matplotlib.pyplot as plt

def plot_career(data):
    wins = data[data["result"] == "win"]
    losses = data[data["result"] == "loss"]
    plt.figure(figsize=(12, 7))
    plt.scatter(wins["player_age"], wins["age_difference"],
                color="lightblue", label="Match won", s=10)
    plt.scatter(losses["player_age"], losses["age_difference"],
                color="purple", label="Match lost", s=10)
    plt.axhline(0, color="black", linewidth=0.5)
    plt.xlabel("Player's age")
    plt.ylabel("Player's age − opponent's age")
    plt.title("Career matches by age and result")
    plt.legend()
    plt.show()