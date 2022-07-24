import project


def test_shuffle_cards():
    blackjack = project.Blackjack()
    assert len(blackjack.shuffle_cards()) == 52

def test_main():
    project.welcome()


def test_begin_hand():
    blackjack = project.Blackjack()
    blackjack.begin_hand(True)
    assert len(blackjack.players_hand) == 2
    assert len(blackjack.dealers_hand) == 2
    assert blackjack.dealers_hand[0] == "?"
    assert blackjack.dealers_down_card == "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" or "10" or "J" or "Q" or "K" or "A"
    assert len(blackjack.deck) == 48 

def test_deal_card():
    blackjack = project.Blackjack()
    x = blackjack.deal_card(True)
    assert blackjack.deck.count(x) == 3
    assert blackjack.deal_card(False) == "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" or "10" or "J" or "Q" or "K" or "A"
    assert len(blackjack.deck) == 50

def test_register_player():
    blackjack = project.Blackjack()
    assert blackjack.register_player("jOhn") == "\nYou received $100. You need $200 to win."
    assert blackjack.player["name"] == "John"
    assert blackjack.player["money"] == 100

def test_place_wager():
    blackjack = project.Blackjack()
    assert blackjack.register_player("jOhn")
    assert blackjack.place_wager("$5") == "\nYou wagered $5."

def test_get_hand_total():
    blackjack = project.Blackjack()
    blackjack.players_hand = ['A', '5']
    assert blackjack.get_hand_total(False) == 0
    assert blackjack.get_hand_total(True) == 16
    blackjack.players_hand = ['A', '5', '8']
    assert blackjack.get_hand_total(True) == 14
    blackjack.players_hand = ['A', '5', '8', 'A']
    assert blackjack.get_hand_total(True) == 15
