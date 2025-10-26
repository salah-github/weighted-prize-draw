import random
import time
import os
from datetime import datetime
from collections import Counter

# --------------------------------------------------------------
#  Weighted random selection
# --------------------------------------------------------------
def weighted_choice(collection):
    """Choose one element from a dict based on its weight."""
    total_weight = sum(collection.values())
    if total_weight <= 0:
        print("Error: total weight must be greater than zero.")
        return None
    r = random.randint(1, total_weight)
    for name, weight in collection.items():
        r -= weight
        if r <= 0:
            return name
    return None  # fallback (shouldn’t happen)

# --------------------------------------------------------------
#  Draw multiple unique winners
# --------------------------------------------------------------
def draw_winners(participants, num_winners):
    """Draw multiple unique winners without replacement."""
    winners = []
    pool = dict(participants)
    for _ in range(min(num_winners, len(pool))):
        winner = weighted_choice(pool)
        if not winner:
            break
        winners.append(winner)
        del pool[winner]
    return winners

# --------------------------------------------------------------
#  Display odds (based on weights)
# --------------------------------------------------------------
def show_odds(participants):
    """Display each participant's odds of winning based on their entries."""
    total_weight = sum(participants.values())
    print("\n=== Odds of Winning ===")
    for name, weight in participants.items():
        odds = (weight / total_weight) * 100
        print(f"{name:12s} → {odds:6.2f}%")
    print("========================\n")

# --------------------------------------------------------------
#  Optional fairness simulation
# --------------------------------------------------------------
def simulate_probabilities(participants, draws=1000):
    """Run repeated draws to confirm fairness (quick simulation)."""
    results = Counter()
    for _ in range(draws):
        winner = weighted_choice(participants)
        results[winner] += 1

    total_weight = sum(participants.values())
    print("\nSimulated win rates (approximation from 1,000 draws):")
    for name, weight in participants.items():
        observed = results[name] / draws * 100
        print(f"{name:12s} → {observed:6.2f}%")
    print("========================\n")

# --------------------------------------------------------------
#  Log results to Desktop
# --------------------------------------------------------------
def log_results(participants, winners):
    """Append draw results with timestamp to a log file on Desktop."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "draw_log.txt")

    with open(desktop_path, "a", encoding="utf-8") as f:
        f.write(f"\n=== Draw at {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
        f.write("Participants:\n")
        for name, weight in participants.items():
            f.write(f"  - {name}: {weight}\n")
        f.write("Winners:\n")
        for i, w in enumerate(winners, 1):
            f.write(f"  Winner {i}: {w}\n")
        f.write("=============================================\n")

    print(f"\nResults logged to Desktop as 'draw_log.txt'")

# --------------------------------------------------------------
#  Main program
# --------------------------------------------------------------
def main():
    print("=== Weighted Prize Draw ===")
    participants = {}

    # Gather participants
    while True:
        name = input("Enter participant name (or 'done' to finish): ").strip()
        if not name:
            print("Name cannot be blank.")
            continue
        if name.lower() == "done":
            if participants:
                break
            else:
                print("You must enter at least one participant before finishing.")
                continue
        try:
            weight = int(input(f"How many entries for {name}? ").strip())
            if weight < 1:
                print("Weight must be at least 1.")
                continue
            participants[name] = weight
        except ValueError:
            print("Please enter a valid integer.")

    # Ask for number of winners
    while True:
        try:
            num_winners = int(input("How many winners to draw? ").strip())
            if num_winners < 1:
                print("Must draw at least one winner.")
                continue
            break
        except ValueError:
            print("Enter a whole number.")

    # ----------------------------------------------------------
    # Ask whether to run simulation first
    # ----------------------------------------------------------
    while True:
        choice = input("\nRun quick fairness simulation first? (y/n): ").strip().lower()
        if choice == "y":
            simulate_probabilities(participants, draws=1000)
            break
        elif choice == "n":
            print("Skipping simulation.\n")
            break
        else:
            print("Please enter 'y' or 'n'.")

    # ----------------------------------------------------------
    # Show odds before drawing winners
    # ----------------------------------------------------------
    show_odds(participants)

    # ----------------------------------------------------------
    # Draw the winners
    # ----------------------------------------------------------
    print("Drawing winners...\n")
    winners = draw_winners(participants, num_winners)

    if not winners:
        print("No winners selected.")
    else:
        for i, w in enumerate(winners, 1):
            time.sleep(2)
            print(f"🏆 Winner {i}: {w}")
        print("\nAll winners have been drawn.")

    # Log results to Desktop
    log_results(participants, winners)

    # Controlled exit
    while True:
        command = input("\nType 'exit' and press Enter to close the program: ").strip().lower()
        if command == "exit":
            print("Exiting program. Goodbye!")
            time.sleep(1)
            break
        else:
            print("Invalid input. Please type 'exit' to close.")

# --------------------------------------------------------------
#  Run the program
# --------------------------------------------------------------
if __name__ == "__main__":
    main()
