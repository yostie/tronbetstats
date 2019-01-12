# tronbetstats
Calculates Tronbet.io reward statistics

This script will allow you to specify multiple simple betting strategies and simulate betting sessions.  This should help you to determine what betting strategies will work best for you.  At the end of the simulation, it will produce statistics showing any profit in Tron (TRX), should you choose to take profit, as well as how much Tronbet ANTE you would have mined.

# Requirements

Python 3.6+

# settings.yaml

This file contains all the parameters for your betting strategies.

Globals - These settings will apply across all strategies.  
  - ante_cost: The current cost to mine 1 ANTE
  - num_simulations: The number of simulations to run per strategy.

Strategies
  - name: The name of your strategy.
  - bankroll: Your starting bankroll.
  - profit_pct: Once you hit this percentage of profit from your starting bankroll, it will subtract this percentage and act like you moved the profit to another wallet.
  - win_pct: The desired winning percentage you are going to bet with.  The value here must exist in the payout_table.yaml file.  The win percentage determines your payout.
  - max_consecutive_losses: After this number is hit, your betting multiplier will reset to your default bet.
  - loss_multiplier: After a loss, your default bet will be multiplied by this value until you hit max_consecutive_losses.  This multiplier does not compound after every loss and stays static across multiple losses.
  - default_bet: The minimum bet you are going to make.
  - max_bets: The maximum number of bets in a betting session.  Set this to a number you feel is realistic if you were really betting.  You can set this to 0, however if you keep winning, this will likely look like the script hung.  Tends to be more of an issue with large starting bankrolls.
  
# payout_table.yaml

Specifies the values for the betting and payout.  All of these values are pre-determined by Tronbet and should not be changed.

prediction: Your predicted number.  The simulator currently assumes if the lucky number is above this number, you win.
win_pct: Your chance of winning.
multiplier: The value your bet will be multiplied by to determine your winnings.

  
