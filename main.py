import random
import os
import BJart

card_dict = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]
user_bank = 500
dealer_bank = 500

def init():
  """initialize all the variables"""
  global user_choice, dealer_choice, user_score, user_hand, is_usr, user_bet, bank_flag, BJ_flag
  print(blackjackart.logo[0])
  user_choice = []
  dealer_choice = []
  is_usr = True                                      #This variable checks if the user is playing or the dealer
  user_hand = True                                   #This variable shows that user is done with their hand
  bank_flag = False                                  
  BJ_flag = False
  if(user_bank >0):                                  #If user has sufficient balance, ask him to place the bet
    user_bet = int(input(f"You have currently ${user_bank}. You can place bets of amount $1, $5, $25, $50, $100 or $500. Please enter your bet. "))
  else:
    print("You do not have sufficient amount to place the bet right now. Please try later")
    bank_flag = True                                 #Set the bank flag to true indicating that user is out of money

def clear():
  """Clears the terminal"""
  os.system('clear')

def deal_cards():
  """deals the first hand"""
  global user_choice, dealer_choice

  user_choice = random.sample(card_dict,2)            #Randomly selects two cards from the array
  dealer_choice = random.sample(card_dict, 2)         #Randomly selects two cards for the computer
  print(f"Dealer's hand is {dealer_choice[0]}")       #Prints computers first card

def is_blackjack():
  """Checks if either user or comp has a BlackJack"""
  global user_score, user_bet, user_bank, dealer_bank, BJ_flag

  if (user_score == 21):
    print(f"Your hand is {user_choice}")              #Prints user's hand
    print(f"Its a BlackJack. You won the game as well as ${1.5*user_bet}")
    user_bank += 1.5 * user_bet                       #Add amount in user's bank
    BJ_flag = True                                    #Set the black jack flag to true
  elif (dealer_score == 21):
    print(f"Dealer got a BlackJack. You lost the game as well as ${user_bet}")
    user_bank -= user_bet                             #Decrement money from user if dealer has black jack
    dealer_bank += user_bet
    BJ_flag = True

def score_sum():
  """Sums the total score of Dealer and user"""
  global user_score, dealer_score
  user_score = 0
  dealer_score = 0

  for i in range(len(user_choice)):
    if (user_choice[i] == 1):                         #Checks if the card is an ace
      if (user_score + 11 > 21):                      #If the score is greater than 21, then the ace is counted as 1
        user_score += 1                               #Add 1 to user_score
        user_choice[i] = 1                            #Place it as 1 in the user choice array
      else:
        user_score += 11                              #Otherwise, the ace is counted as 11
        user_choice[i] = 11                           #Place it as 11 in the user choice array
    else:
      user_score += user_choice[i]                    #Otherwise add 11 to user score
  for i in dealer_choice:                             #Add everything as it is in the dealer score
    dealer_score += i

def score_compare():
  """compares the score of user and dealer"""
  global user_score, dealer_score, is_usr, user_bank, user_bet

  if (user_hand):                                          #If user is playing
    print(f"Your hand is {user_choice} = {user_score}\n")  #Show their cards and score
    if (user_score > 21):                                  #If their score is greater than 21, they lose
      print(f"You LOST the game as well as ${user_bet}")
      user_bank -= user_bet                                #Bet amount deducted from user's bank
    elif (user_score <= 21):                               #If their score is less than 21
      draw_more(is_usr)                                    #Take them to the draw more function

  else:                                                    #Otherwise the dealer is playing
    is_usr = False                                         #Set is_user flag to False
    print(f"Dealer's hand is {dealer_choice} = {dealer_score}\n")
    if (dealer_score < 17):                                #Dealer's total is less than 17
      draw_more(is_usr)                                    #Send the dealer to draw more function

    elif (dealer_score> 21):                               #If dealer's score is greater than 21, they lose
      print(f"Dealer busts so you WON the game as well as ${2*user_bet}")
      user_bank += 2 * user_bet                            #Adding money in user's bank

    elif (dealer_score >= 17):                             #Otherwise, whoever with the highest score wins
      if (user_score > dealer_score):
        print(f"Your total is {user_score} and dealer's total is {dealer_score} so you WON the game as well as ${2*user_bet}")
        user_bank += 2 * user_bet
      elif (user_score < dealer_score):
        print(f"Your total is {user_score} and dealer's total is {dealer_score} so you LOST the game as well as ${user_bet}")
        user_bank -= user_bet                              #Deduct moeny from user's bank
      else:print(f"Your total is {user_score} and dealer's total is {dealer_score} so its a DRAW")

def draw_more(user_flag):
  """Allows user or dealer to draw more cards"""
  global user_hand

  if (user_flag):                                           #If its the user
    user_answer = input("Do you want to hit or stand? ")    #Ask them if they want to draw or pass
    if (user_answer == "hit"):                              #If they want to draw
      user_choice.append(random.choice(card_dict))          #Append a random card to user's list
      score_sum()                                           #Call the sum function
    elif (user_answer == "stand"):
      user_hand = False                                     #Otherwise, set the user_hand to false and let the game know that user is done with their hand

  else:                                                     #Dealer has come to draw cards so append them in the comp's list
    dealer_choice.append(random.choice(card_dict))
    score_sum()
  score_compare()                                           #Call compare function at the end

def play_again():
  """Asks the user if he/she wants to play again"""
  print(f"Your current amount after the last game is ${user_bank}")
  play_flag = input("\nDo you want to play again? Type 'yes' or 'no'. ")
  if (play_flag == "yes"):                                  #If the user wants to play again
    clear()                                                 #Call the clear function and clear the terminal
    main()                                                  #Call the main function
  else:
    print(blackjackart.logo[1])                             #Otherwise exit and print farewell logo

def main():
  init()                                                    
  if not bank_flag:                                         #If the bank flag is False
    deal_cards()                                            #Deal the 1st round of cards
    score_sum()                                             #Calculate the sum
    is_blackjack()                                          #See if user has a blackjack
    if not BJ_flag :                                        #If user does not have a blackjack
      score_compare()                                       #Compare the scores
      play_again()                                          #Call the play again function
    else: 
      play_again()                                          #Otherwise, just call the play again function

main()                                                      #Calling the main function 
