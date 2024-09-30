import csv
from itertools import combinations
import time

def read_csv():
    """
    :return: list of dictionaries of shares with their name, cost and profit
    """
    shares = []
    with open('data/dataset_brute_force.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            share = {
                'name': row['Actions #'],
                'cost': float(row['Coût par action (en euros)']),
                'profit': float(row['Bénéfice (après 2 ans)'].rstrip('%')) / 100
            }
            shares.append(share)
    return shares

def calculate_profit(combination):
    """
    :param combination:
    :return: total cost and total profit for each combination of shares
    """
    total_cost = sum(action['cost'] for action in combination)
    total_profit = sum(action['cost'] * action['profit'] for action in combination)
    return total_cost, total_profit

def find_best_combination(shares, max_budget):
    """
    :param shares:
    :param max_budget:
    :return: the best profit and the best combination for this best rofit
    """
    best_combination = None
    best_profit = 0

    for r in range(1, len(shares) + 1):
        for combination in combinations(shares, r):
            total_cost, total_profit = calculate_profit(combination)
            if total_cost <= max_budget and total_profit > best_profit:
                best_combination = combination
                best_profit = total_profit

    return best_combination, best_profit

def main():
    max_budget = 500

    start_time = time.time()

    shares = read_csv()
    best_combination, best_profit = find_best_combination(shares, max_budget)

    print("Meilleure combinaison d'actions :")
    for share in best_combination:
        print(f"- {share['name']} : {share['cost']:.2f}€ (bénéfice : {share['profit'] * 100:.2f}%)")

    total_cost = sum(share['cost'] for share in best_combination)
    print(f"\nCoût total : {total_cost:.2f}€")
    print(f"Profit total après 2 ans : {best_profit:.2f}€")
    print(f"Rendement : {(best_profit/total_cost)*100:.2f}%")

    end_time = time.time()
    execution_time = end_time-start_time
    print(f"\nTemps d'exécution : {execution_time:.4f} secondes")

if __name__ == "__main__":
    main()
