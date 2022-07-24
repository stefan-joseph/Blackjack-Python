import sys
import random


def main():
    blackjack = Blackjack()
    name = blackjack.welcome()
    print(blackjack.register_player(name)) if name else sys.exit()
    new_game = True
    while True:
        w = blackjack.place_wager(input("\nHow much would you like to wager? $5, $10, or $25? "))
        if w: 
            print(w)
            blackjack.begin_hand(new_game)
            new_game = False
            print(blackjack)
            while True:
                if blackjack.players_turn():
                    break
            print(blackjack.check_hand_result())
            blackjack.clear_table()
            print(blackjack.game_status())
    


class Blackjack:
    def __init__(self):
        self.player = {}
        self.wager = 0
        self.deck = []
        self.players_hand = []
        self.dealers_hand = []
        self.dealers_down_card = ""

    def __str__(self):
        a = "'" if self.player['name'].endswith('s') else "'s"
        return f"\nDealer's hand: {self.dealers_hand}\n{self.player['name']}{a} hand: {self.players_hand}"
    

    def welcome(self):
         while True:
            begin = input("\nWelcome to the Casino! Would you like to play Blackjack? Yes? No? ").strip().lower()
            if begin == "yes":
                while True:
                    name = input("\nPlease provide your first name: ").strip()
                    if not " " in name and name.isalpha():
                        return name
            elif begin == "no":
                return False

    def register_player(self, name):
        name = name.lower().capitalize()
        self.player = {"name": name, "money": 100}
        return f"\nYou received ${self.player['money']}. You need $200 to win."

    def place_wager(self, wager):
            try:
                wager = int(wager.strip().replace("$", ""))
                if wager == 5 or wager == 10 or wager == 25:
                    if not wager > self.player['money']:
                        self.wager = wager
                        return f"\nYou wagered ${self.wager}."
                    else:
                        print(f"\nYou do not have enough money for that size wager. You only have ${self.player['money']}.")
                        return False
                else: raise ValueError
            except ValueError:
                print("\nYou can only bet $5, $10 or $25.")
                return False

    def begin_hand(self, new_game):
        for _ in range(2):
            self.players_hand.append(self.deal_card(new_game))
            self.dealers_hand.append(self.deal_card(new_game))
        self.dealers_down_card = self.dealers_hand[0]
        self.dealers_hand[0] = "?"
        return (self.dealers_hand, self.players_hand)

    def deal_card(self, new):
        if len(self.deck) < 1:
            if not new:
                print("\nThere are no more cards.")
            self.deck = self.shuffle_cards()
        index = random.randint(1, len(self.deck)) - 1
        card = self.deck[index]
        del self.deck[index]
        return card

    def shuffle_cards(self):
        print("\nShuffling cards...")
        cards = (['2', '3', '4', '5', '6', '7', '8', '9', '10', "J", "Q", "K", "A"] * 4)
        random.shuffle(cards)
        return cards

    def get_hand_total(self, player):
        if player:
            hand = self.players_hand.copy()
        else:
            hand = self.dealers_hand.copy()
        while True:
            total = 0
            for c in hand:
                try:
                    total += int(c)
                except ValueError:
                    if c == "J" or c == "Q" or c == "K":
                        total += 10
                    elif c == "A":
                        total += 11
            if total > 21 and "A" in hand:
                hand[hand.index("A")] = 1
            else:
                break
        return total

    def players_turn(self):
        if len(self.players_hand) == 2 and self.wager * 2 < self.player['money']:
            t = f"\nYou have {self.get_hand_total(True)}. Hit, stand or double? "
        else:
            t =  f"\nYou have {self.get_hand_total(True)}. Hit or stand? "
        d = input(t).strip().lower()
        if d == "hit":
            self.players_hand.append(self.deal_card(False))
            t = self.get_hand_total(True)
            print(self)
            if t <= 21:
                return False
            else:
                return True
        elif d == "stand":
            self.dealer_logic()
            return True
        elif d == "double" and len(self.players_hand) == 2 and self.wager * 2 < self.player['money']:
            self.wager = self.wager * 2
            print(f"\nYou doubled your wager to ${self.wager}")
            self.players_hand.append(self.deal_card(False))
            print(self)
            t = self.get_hand_total(True)
            if t <= 21:
                print(f"\nYou have {self.get_hand_total(True)}")
                self.dealer_logic()
                return True
            else:
                return True
        else:
            if len(self.players_hand) == 2 and self.wager * 2 < self.player['money']:
                print("\nYou can only hit, stand or double.")
            else:
                print("\nYou can only hit or stand.")
            return False

    
    def dealer_logic(self):
        self.dealers_hand[0] = self.dealers_down_card
        print("\nRevealing dealer's down card...")
        while True:
            print(self)
            t = self.get_hand_total(False)
            if t < 17:
                print(f"\nDealer has {t}. Dealer hits.")
                self.dealers_hand.append(self.deal_card(False))
            elif t > 21:
                print(f"\nDealer has {t}. Dealer busts.")
                break
            else:
                print(f"\nDealer has {t}. Dealer stands.")
                break
        
    def check_hand_result(self):
        p = self.get_hand_total(True)
        d = self.get_hand_total(False)
        if p > 21:
            self.player["money"] = self.player["money"] - self.wager
            return f"\nYou busted with {p}. You lose ${self.wager}."
        elif d > 21:
            self.player["money"] = self.player["money"] + self.wager
            return f"\nDealer busted with {d}. You win ${self.wager}."
        elif p > d:
            self.player["money"] = self.player["money"] + self.wager
            return f"\nYou won with {p}. You win ${self.wager}."
        elif p < d:
            self.player["money"] = self.player["money"] - self.wager
            return f"\nYou lost with {p}. You lose ${self.wager}."
        else:
            return f"\nIt's a draw on {p}. Nobody wins."
    
    def clear_table(self):
        self.players_hand = []
        self.dealers_hand = []
        self.dealers_down_card = ""
        self.wager = 0

    def game_status(self):
        m = self.player["money"]
        if m >= 200: sys.exit("\nCongatulations! You have ${m}. You won the game! Come back soon!")
        elif m <= 0: sys.exit("\nYou have no more money. The house (almost) always wins. Come back soon!")
        else: return f"\nYou have ${m}. You need $200 to win."


if __name__ == "__main__":
    main()