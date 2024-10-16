import csv
from itertools import combinations
import time

def read_csv():
    """
    Read share data from a CSV file and convert it to a list of dictionaries.

    Returns:
        list[dict]: List of dictionaries containing share information
                    Each dictionary has keys:
                    - 'name' (str): Share name
                    - 'cost' (float): Share cost in euros
                    - 'profit' (float): Share profit as a decimal (e.g., 0.15 for 15%)
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

def calculate_profit(combination : list[dict])-> tuple[float, float]:
    """
    Calculate the total cost and total profit for a combination of shares provided in input
    :param combination:
    :return: total cost and total profit for each combination of shares
    """
    total_cost = sum(action['cost'] for action in combination)
    total_profit = sum(action['cost'] * action['profit'] for action in combination)
    return total_cost, total_profit

def find_best_combination(shares : list, max_budget : int) -> tuple[list[dict], float, int]:
    """
    Find the combination of shares that yields the highest profit within the budget constraint.
    :param shares (list[dict]): List of all available shares Each dict contains 'name', 'cost', and 'profit' keys:
    :param max_budget (float): Maximum amount that can be spent on shares
    :return: tuple[list[dict], float, int]: A tuple containing:
            - best_combination (list[dict]): List of dictionaries representing the best combination of shares
            - best_profit (float): Total profit of the best combination
            - compteur (int): Number of combinations tested
    """
    best_combination = None
    best_profit = 0
    compteur = 0
    for i in range(1, len(shares) + 1):
        for combination in combinations(shares, i):
            compteur +=1
            total_cost, total_profit = calculate_profit(combination)
            if total_cost <= max_budget and total_profit > best_profit:
                best_combination = combination
                best_profit = total_profit

    return best_combination, best_profit, compteur

def main():
    max_budget = 500

    start_time = time.time()

    shares = read_csv()
    best_combination, best_profit, compteur = find_best_combination(shares, max_budget)

    print("Meilleure combinaison d'actions :")
    for share in best_combination:
        print(f"- {share['name']} : {share['cost']:.2f}€ (bénéfice : {share['profit'] * 100:.2f}%)")

    total_cost = sum(share['cost'] for share in best_combination)
    print(f"\nCoût total : {total_cost:.2f}€")
    print(f"Bénéfice total après 2 ans : {best_profit:.2f}€")
    print(f"Rendement : {(best_profit/total_cost)*100:.2f}%")
    print(f"\nLe nombre de combinaisons testées est de : {compteur}")
    end_time = time.time()
    execution_time = end_time-start_time
    print(f"\nTemps d'exécution : {execution_time:.2f} secondes")

if __name__ == "__main__":
    main()
