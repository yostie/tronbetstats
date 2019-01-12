import random
import yaml
from pprint import pprint as pp

def simulate_betting(strategy, ante_cost, payout_table, sim_num, verbose=False):

    # INITIALIZE VARIABLES
    betting_bankroll = strategy['bankroll']
    starting_bankroll = strategy['bankroll']
    win_pct = strategy['win_pct']
    profit_pct = strategy['profit_pct']
    max_consecutive_losses = strategy['max_consecutive_losses']
    loss_multiplier = strategy['loss_multiplier']
    default_bet = strategy['default_bet']
    max_bets = strategy['max_bets']
    for payout in payout_table:
        if payout['win_pct'] == win_pct:
            prediction = payout['prediction']
            payout_multiplier = payout['multiplier']
    ante = 0
    total_wins = 0
    total_losses = 0
    profit_bankroll = 0
    profit_taking_offset = starting_bankroll * (profit_pct / 100)
    profit_taking_amount = starting_bankroll + (starting_bankroll * (profit_pct / 100))
    highest_bankroll = betting_bankroll
    consecutive_losses = 0

    while True:
        if consecutive_losses == 0:
            bet = default_bet
            pass
        elif consecutive_losses == max_consecutive_losses:
            if verbose: print(f"Consecutive losses hit max loss of {max_consecutive_losses}.  Resetting bet to {default_bet}.")
            consecutive_losses = 0
            bet = default_bet
        elif consecutive_losses <= max_consecutive_losses and bet == default_bet:
            bet *= loss_multiplier

        if bet > betting_bankroll:
            if verbose: print(f"SIM {sim_num} EXIT: Your bankroll of {bankroll} is less than the desired bet of: {bet}.")
            results = { "stop_reason": "insufficient_funds" }
            break     

        if verbose: print(f"Amount to bet: {bet}")
        lucky_number = random.randint(0,100)
        if lucky_number > prediction:
            payout = bet * payout_multiplier - bet
            betting_bankroll += round(payout)
            consecutive_losses = 0
            total_wins += 1
            if betting_bankroll > highest_bankroll:
                highest_bankroll = betting_bankroll
            if verbose: print(f"WIN - Current bankroll: {betting_bankroll}")
            if verbose: print(f"Highest bankroll: {highest_bankroll}")
        else:
            consecutive_losses += 1
            betting_bankroll -= bet
            total_losses += 1
            if verbose: print(f"LOSE - Current bankroll: {betting_bankroll}")

        ante += round(bet / ante_cost, 3)

        if betting_bankroll >= profit_taking_amount and profit_pct > 0:
            if verbose: print(f"Bankroll at {profit_pct} percent of starting bankroll - taking profit")
            profit_bankroll += profit_taking_offset
            betting_bankroll -= profit_taking_offset

        if max_bets == (total_wins + total_losses):
            if verbose: print(f"SIM {sim_num} EXIT: Maximum number of bets per simulation hit!")
            results = { "stop_reason": "max_bets" }
            break

    results['total_wins'] = total_wins
    results['total_losses'] = total_losses
    results['betting_bankroll'] = betting_bankroll
    results['highest_bankroll'] = highest_bankroll
    results['profit_bankroll'] = profit_bankroll
    results['ante'] = round(ante, 3)

    return results

def main():
    # LOAD AND GLOBAL SETTINGS
    payout_table = yaml.load(open("payout_table.yaml"))
    settings = yaml.load(open("settings.yaml"))

    ante_cost = settings['globals']['ante_cost']
    num_simulations = settings['globals']['num_simulations']

    print(f"\nSIMULATING {len(settings['strategies'])} STRATEGIES WITH THE FOLLOWING CONSTANTS...\n" + "="*54 + "\n")
    print(f"Number of simulations: {num_simulations}")
    print(f"ANTE cost: {ante_cost}\n")

    for strategy in settings['strategies']:
        strategy['results'] = []
        for x in range(num_simulations):
            strategy['results'].append(simulate_betting(strategy, ante_cost, payout_table, x))

    print("\nSIMULATION RESULTS\n" + "="*18)

    for strategy in settings['strategies']:
        print(f"{strategy['name']} had the following settings:")
        print(f"    Starting Bankroll: {strategy['bankroll']}")
        print(f"    Profit Taking Percentage: {strategy['profit_pct']}")
        print(f"    Desired Win Percentage: {strategy['win_pct']}")
        print(f"    Loss Multiplier: {strategy['loss_multiplier']}")
        print(f"    Default bet: {strategy['default_bet']}")
        print(f"    Max Bets: {strategy['max_bets']}\n")
        print(f"{strategy['name']} results:")
        for i, result in enumerate(strategy['results']):
            print(f"    Simulation: {i+1}")
            print(f"    Total wins: {result['total_wins']}")
            print(f"    Total losses: {result['total_losses']}")
            print(f"    Win percentage: {round(result['total_wins'] / (result['total_wins'] + result['total_losses']) * 100, 3)}")
            print(f"    Profit bankroll: {result['profit_bankroll']}")
            print(f"    Ending betting bankroll: {result['betting_bankroll']}")
            print(f"    Highest betting bankroll: {result['highest_bankroll']}")
            print(f"    ANTE earned: {result['ante']}")
            if result['stop_reason'] == 'insufficient_funds':
                print(f"    Stop bet reason: Insufficient funds to place desired bet\n")
            else:
                print(f"    Stop bet reason: Maxmimum number of bets {strategy['max_bets']} hit\n")

if __name__ == '__main__':
    main()
