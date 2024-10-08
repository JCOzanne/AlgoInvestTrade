import csv
import time

def read_csv(file_path):
    """
    :param file_path:
    :return: a list of shares sorted by profit/cost ratio in descending order
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

def knapsack(values, weights, capacity):
    """
    :param values:
    :param weights:
    :param capacity:
    :return: the list of share's index making the best profit and this best profit according to the "knapsack" method
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

def find_best_combination(actions, max_budget):
    """
    :param actions:
    :param max_budget:
    :return:the best profit and the list of shares achieving this best profit
    """
    costs = [action['cost'] for action in actions]
    profits = [action['cost'] * action['profit'] for action in actions]

    max_profit, selected_indices = knapsack(profits, costs, max_budget)

    best_combination = [actions[i] for i in selected_indices]
    return best_combination, max_profit

def main():
    file_path = 'data/dataset_brute_force.csv'
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
    main()
