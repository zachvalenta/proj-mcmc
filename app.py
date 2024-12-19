import numpy as np
from rich.console import Console
from rich.table import Table

# Define possible states
# State 0: No purchase
# State 1: Coffee only
# State 2: Pastry only
# State 3: Coffee and Pastry

# Transition probabilities (Markov Chain)
transition_matrix = np.array([
    [0.4, 0.3, 0.2, 0.1],  # From no purchase
    [0.2, 0.4, 0.1, 0.3],  # From coffee only
    [0.2, 0.3, 0.3, 0.2],  # From pastry only
    [0.1, 0.3, 0.2, 0.4]   # From coffee and pastry
])

def run_mcmc_simulation(n_days=1000, initial_state=0):
    """
    Run MCMC simulation of customer purchase behavior
    
    Args:
        n_days: Number of days to simulate
        initial_state: Starting state (0-3)
    
    Returns:
        List of daily states and summary statistics
    """
    current_state = initial_state
    states = [current_state]
    
    # Run Markov Chain
    for _ in range(n_days - 1):
        # Propose next state based on transition probabilities
        current_state = np.random.choice(4, p=transition_matrix[current_state])
        states.append(current_state)
    
    # Calculate summary statistics
    states = np.array(states)
    summary = {
        'no_purchase_prob': int(np.mean(states == 0) * 100),
        'coffee_only_prob': int(np.mean(states == 1) * 100),
        'pastry_only_prob': int(np.mean(states == 2) * 100),
        'both_prob': int(np.mean(states == 3) * 100),
        'expected_daily_revenue': int(np.mean([
            0 if s == 0 else
            3.50 if s == 1 else  # Coffee price
            2.50 if s == 2 else  # Pastry price
            5.50 for s in states  # Discounted combo price
        ]))
    }
    
    return states, summary

# Run simulation
states, summary = run_mcmc_simulation()
print(summary)

# Calculate average length of "streaks" for each purchase type
def calculate_streaks(states):
    streaks = {0: [], 1: [], 2: [], 3: []}
    current_streak = 1
    current_state = states[0]
    
    for state in states[1:]:
        if state == current_state:
            current_streak += 1
        else:
            streaks[current_state].append(current_streak)
            current_streak = 1
            current_state = state
    
    return {k: np.mean(v) if v else 0 for k, v in streaks.items()}

streak_stats = calculate_streaks(states)
print(streak_stats)

console = Console()

# Create summary table
summary_table = Table(title="Coffee Shop Purchase Analysis")
summary_table.add_column("Metric", style="cyan")
summary_table.add_column("Value", justify="right", style="green")

# Add summary stats
summary_table.add_row("No Purchase Probability", f"{summary['no_purchase_prob']}%")
summary_table.add_row("Coffee Only Probability", f"{summary['coffee_only_prob']}%")
summary_table.add_row("Pastry Only Probability", f"{summary['pastry_only_prob']}%")
summary_table.add_row("Both Items Probability", f"{summary['both_prob']}%")
summary_table.add_row("Expected Daily Revenue", f"${summary['expected_daily_revenue']:.2f}")

# Create streaks table
streak_table = Table(title="Average Purchase Pattern Streaks")
streak_table.add_column("Purchase Type", style="cyan")
streak_table.add_column("Avg. Streak Length (Days)", justify="right", style="magenta")

# Add streak stats
purchase_types = {
    0: "No Purchase",
    1: "Coffee Only",
    2: "Pastry Only",
    3: "Both Items"
}

for state, desc in purchase_types.items():
    streak_table.add_row(desc, f"{streak_stats[state]:.1f}")

# Print both tables with a separator
console.print(summary_table)
console.print("\n")  # Add spacing between tables
console.print(streak_table)
