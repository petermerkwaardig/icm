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

# Functie voor push/fold-beslissing op basis van hand en stack
def push_fold_decision(hand, stack_in_bb, total_stacks):
    # Handcategorie bepalen (vereenvoudigd)
    premium_hands = ['AA', 'KK', 'QQ', 'AK', 'AQ']
    strong_hands = ['JJ', 'TT', '99', '88', 'AQ', 'KQ']
    marginal_hands = ['77', '66', '55', 'A10', 'KJ', 'QJ']
    
    # Gemiddelde stack bepalen voor ICM-druk
    gemiddelde_stack = sum(total_stacks) / len(total_stacks)
    
    # ICM-druk verhogen bij kleinere stacks
    if stack_in_bb < gemiddelde_stack * 0.5:
        icm_pressure = "high"
    elif stack_in_bb < gemiddelde_stack:
        icm_pressure = "medium"
    else:
        icm_pressure = "low"
    
    # Beslissing maken op basis van de ICM-druk
    if hand in premium_hands:
        return "Push", f"premium hand, ICM-pressure {icm_pressure}: PUSH!"
    elif hand in strong_hands:
        if icm_pressure == "high":
            return "Push", "strong hand, small stack: PUSH!"
        else:
            return "Fold", "strong hand, low ICM-pressure low: fold."
    elif hand in marginal_hands:
        if icm_pressure == "high" or stack_in_bb <= 10:
            return "Push", "marginal hand, small stack, high ICM-pressure: PUSH!"
        else:
            return "Fold", "marginal hand: fold."
    else:
        return "Fold", "weak hand: fold."

# Streamlit applicatie
def main():
    st.title("ICM Push/Fold")

    # Vraag de prijzengeldverdeling eenmalig aan het begin
    payouts_input = st.text_input("Prijzengeld")
    if payouts_input:
        payouts = list(map(int, payouts_input.split()))

        # Jouw hand, stack, big blind en andere spelers
        hand = st.text_input("Je hand").upper()
        mijn_stack = st.number_input("Je stack", min_value=0, value=0)
        big_blind = st.number_input("Big blind", min_value=1, value=1)

        # Stacks van spelers vóór jou
        stacks_voor_mij_input = st.text_input("Stacks in pot")
        stacks_voor_mij = list(map(int, stacks_voor_mij_input.split())) if stacks_voor_mij_input else []

        # Stacks van spelers achter jou
        stacks_achter_mij_input = st.text_input("stacks achter jou")
        stacks_achter_mij = list(map(int, stacks_achter_mij_input.split())) if stacks_achter_mij_input else []

        # Voeg jouw stack, de stacks voor je en achter je samen
        total_stacks = [mijn_stack] + stacks_voor_mij + stacks_achter_mij

        # Bereken jouw stack in termen van big blinds
        if big_blind > 0:
            mijn_stack_in_bb = mijn_stack / big_blind

            # Bereken ICM-waarden
            if st.button("Bereken"):
                icm_values = icm_calculate(total_stacks, payouts)

                # Resultaten tonen
                st.subheader("ICM")
                for i, value in enumerate(icm_values):
                    st.write(f"Stack {total_stacks[i]}|{value:.2f}")
                
                # Push/Fold-beslissing op basis van je hand en je eigen stackgrootte
                beslissing, advies = push_fold_decision(hand, mijn_stack_in_bb, total_stacks)
                st.subheader("Push/Fold")
                st.write(f"{advies}")
                st.write(f"{beslissing}")
                

# Start de Streamlit applicatie
if __name__ == "__main__":
    main()
