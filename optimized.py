import csv
import time
import argparse

def read_csv(file_path: str) -> list[dict]:
    """
    Read share data from a CSV file and return a sorted list of shares by profit/cost ratio.

    Args:
        file_path (str): Path to the CSV file containing share data

    Returns:
        list[dict]: List of dictionaries containing share information, sorted by profit/cost ratio
                    in descending order. Each dictionary contains:
                    - 'name' (str): Share name
                    - 'cost' (float): Share cost in euros
                    - 'profit' (float): Share profit as decimal
   """
    actions = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'Coût par action (en euros)' in row and 'Bénéfice (après 2 ans)' in row:
                cost = float(row['Coût par action (en euros)'])
                profit = float(row['Bénéfice (après 2 ans)'].strip('%'))
            elif 'price' in row and 'profit' in row:
                cost = float(row['price'])
                profit = float(row['profit'])
            else:
                continue

            if cost > 0:
                action = {
                    'name': row.get('name', row.get('Actions #')),
                    'cost': cost,
                    'profit': profit / 100
                }
                actions.append(action)
    return sorted(actions, key=lambda x: x['profit'] / x['cost'], reverse=True)

def knapsack(values: list[float], weights: list[float], capacity: float) -> tuple[float, list[int]]:
    """
    Solve the knapsack problem to find the optimal combination of items within a weight capacity.
    Uses dynamic programming to find the maximum value possible while respecting the weight constraint.

    Args:
        values (list[float]): List of values (profits) for each item
        weights (list[float]): List of weights (costs) for each item
        capacity (float): Maximum weight capacity (budget)

    Returns:
        tuple[float, list[int]]: A tuple containing:
            - float: Maximum value (profit) achievable
            - list[int]: List of indices of selected items in the optimal solution
    """
    n = len(values)
    capacity = int(capacity)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - int(weights[i - 1])] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity
    total_cost = 0
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            if total_cost + weights[i - 1] <= capacity:
                selected.append(i - 1)
                total_cost += weights[i - 1]
                w = w - int(weights[i - 1])

    return dp[n][capacity], selected


def find_best_combination(actions: list[dict], max_budget: float) -> tuple[list[dict], float]:
    """
    Find the optimal combination of shares that maximizes profit within the budget constraint
    using the knapsack algorithm.

    Args:
        actions (list[dict]): List of dictionaries containing share information
                             Each dict must have keys:
                             - 'cost' (float): Share cost
                             - 'profit' (float): Share profit as decimal
        max_budget (float): Maximum budget available for investment

    Returns:
        tuple[list[dict], float]: A tuple containing:
            - list[dict]: List of selected shares in the optimal combination
            - float: Maximum profit achievable with this combination
    """
    costs = [action['cost'] for action in actions]
    profits = [action['cost'] * action['profit'] for action in actions]

    max_profit, selected_indices = knapsack(profits, costs, max_budget)

    best_combination = [actions[i] for i in selected_indices]
    return best_combination, max_profit

def main(file_path):
    max_budget = 500

    start_time = time.time()

    actions = read_csv(file_path)
    best_combination, best_profit = find_best_combination(actions, max_budget)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Meilleure combinaison d'actions :")
    for action in best_combination:
        print(f"- {action['name']} : {action['cost']}€ (bénéfice : {action['profit'] * 100:.2f}%)")

    total_cost = sum(action['cost'] for action in best_combination)
    print(f"\nCoût total : {total_cost:.2f}€")
    print(f"Profit total après 2 ans : {best_profit:.2f}€")
    print(f"Rendement : {(best_profit / total_cost) * 100:.2f}%")

    print(f"\nTemps d'exécution : {execution_time:.2f} secondes")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimiser l'achat d'actions en fonction de leur prix et rendement.")
    parser.add_argument('file', type=str, help="Le nom du fichier CSV à analyser (sans l'extension .csv).")

    args = parser.parse_args()
    file_path = f'data/{args.file}.csv'

    main(file_path)
