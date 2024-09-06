import streamlit as st

# Functie voor het berekenen van ICM
def icm_calculate(total_stacks, payouts):
    total_chips = sum(total_stacks)  # Totaal aantal chips in het spel
    probabilities = [stack / total_chips for stack in total_stacks]  # Kansen op basis van stackgrootte
    
    # Sorteer de spelers per stackgrootte (van groot naar klein)
    stack_ranks = sorted(range(len(total_stacks)), key=lambda i: total_stacks[i], reverse=True)
    
    # Winst per speler berekenen op basis van hun kansen en prijzengeldverdeling
    winnings = [0] * len(total_stacks)
    for i in range(len(payouts)):
        for j in range(len(total_stacks)):
            winnings[stack_ranks[j]] += probabilities[stack_ranks[j]] * payouts[i]
    
    return winnings

# Functie voor push/fold-beslissing op basis van hand
def push_fold_decision(hand, stack_in_bb):
    # Handcategorie bepalen (vereenvoudigd)
    premium_hands = ['AA', 'KK', 'QQ', 'AK', 'AQ']
    strong_hands = ['JJ', 'TT', '99', '88', 'AQ', 'KQ']
    marginal_hands = ['77', '66', '55', 'A10', 'KJ', 'QJ']
    
    # Push/fold-beslissing
    if hand in premium_hands:
        return "Push", "Je hebt een premium hand, push!"
    elif hand in strong_hands and stack_in_bb <= 15:
        return "Push", "Je hebt een sterke hand, en een stack onder 15 BB, push!"
    elif hand in marginal_hands and stack_in_bb <= 10:
        return "Push", "Je hebt een marginale hand, maar je stack is klein, push!"
    else:
        return "Fold", "Je hebt een zwakkere hand of een grote stack, fold."

# Streamlit applicatie
def main():
    st.title("ICM Berekening en Push/Fold Beslissing")

    # Vraag de prijzengeldverdeling eenmalig aan het begin
    payouts_input = st.text_input("Voer de prijzengeldverdeling in (bijv. 100 60 40):", "100 60 40")
    payouts = list(map(int, payouts_input.split()))

    # Jouw hand, stack, big blind en andere spelers
    hand = st.text_input("Voer je eigen hand in (bijv. AA, AK, 77, QJ):", "AK").upper()
    mijn_stack = st.number_input("Voer je eigen stack in chips in:", min_value=0, value=5000)
    big_blind = st.number_input("Voer de huidige big blind in:", min_value=1, value=100)

    # Stacks van spelers vóór jou
    stacks_voor_mij_input = st.text_input("Voer de stacks van spelers voor jou die hebben ingezet (gescheiden door spaties):", "3000 2000")
    stacks_voor_mij = list(map(int, stacks_voor_mij_input.split()))

    # Stacks van spelers achter jou
    stacks_achter_mij_input = st.text_input("Voer de stacks van spelers achter jou die nog kunnen inzetten (gescheiden door spaties):", "1500 2500")
    stacks_achter_mij = list(map(int, stacks_achter_mij_input.split()))

    # Voeg jouw stack, de stacks voor je en achter je samen
    total_stacks = [mijn_stack] + stacks_voor_mij + stacks_achter_mij

    # Bereken jouw stack in termen van big blinds
    mijn_stack_in_bb = mijn_stack / big_blind

    # Bereken ICM-waarden
    if st.button("Bereken ICM en Beslissing"):
        icm_values = icm_calculate(total_stacks, payouts)

        # Resultaten tonen
        st.subheader("ICM Berekeningen")
        for i, value in enumerate(icm_values):
            st.write(f"Stack: {total_stacks[i]} chips | ICM waarde = {value:.2f}")
        
        # Push/Fold-beslissing op basis van je hand en je eigen stackgrootte
        beslissing, advies = push_fold_decision(hand, mijn_stack_in_bb)
        st.subheader("Push/Fold-beslissing")
        st.write(f"Beslissing: {beslissing}")
        st.write(f"Advies: {advies}")

# Start de Streamlit applicatie
if __name__ == "__main__":
    main()
