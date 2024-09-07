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

# Functie voor push/fold-beslissing op basis van Nash ranges
def nash_push_fold(stack_in_bb, hand):
    # Nash push ranges op basis van stackgrootte in big blinds
    if stack_in_bb <= 5:
        return "Push", "Je hebt minder dan 5 BB, push elke hand!"
    elif stack_in_bb <= 10:
        nash_range = ['22+', 'K9+', 'QJ', 'A2+']
        if hand in nash_range:
            return "Push", f"Hand {hand} valt binnen de Nash push range bij 6-10 BB, push!"
        else:
            return "Fold", f"Hand {hand} valt buiten de Nash push range bij 6-10 BB, fold!"
    elif stack_in_bb <= 15:
        nash_range = ['55+', 'A7+', 'KQ', 'KJ']
        if hand in nash_range:
            return "Push", f"Hand {hand} valt binnen de Nash push range bij 11-15 BB, push!"
        else:
            return "Fold", f"Hand {hand} valt buiten de Nash push range bij 11-15 BB, fold!"
    elif stack_in_bb <= 20:
        nash_range = ['88+', 'AQ+', 'KJ']
        if hand in nash_range:
            return "Push", f"Hand {hand} valt binnen de Nash push range bij 16-20 BB, push!"
        else:
            return "Fold", f"Hand {hand} valt buiten de Nash push range bij 16-20 BB, fold!"
    else:
        nash_range = ['99+', 'AK']
        if hand in nash_range:
            return "Push", f"Hand {hand} valt binnen de Nash push range bij >20 BB, push!"
        else:
            return "Fold", f"Hand {hand} valt buiten de Nash push range bij >20 BB, fold!"

# Streamlit applicatie
def main():
    st.title("ICM Berekening en Nash Push/Fold Beslissing")

    # Vraag de prijzengeldverdeling eenmalig aan het begin
    payouts_input = st.text_input("Voer de prijzengeldverdeling in (bijv. 100 60 40):")
    if payouts_input:
        payouts = list(map(int, payouts_input.split()))

        # Jouw hand, stack, big blind en andere spelers
        hand = st.text_input("Voer je eigen hand in (bijv. AA, AK, 77, QJ):").upper()
        mijn_stack = st.number_input("Voer je eigen stack in chips in:", min_value=0, value=0)
        big_blind = st.number_input("Voer de huidige big blind in:", min_value=1, value=1)

        # Stacks van spelers vóór jou
        stacks_voor_mij_input = st.text_input("Voer de stacks van spelers voor jou die hebben ingezet (gescheiden door spaties):")
        stacks_voor_mij = list(map(int, stacks_voor_mij_input.split())) if stacks_voor_mij_input else []

        # Stacks van spelers achter jou
        stacks_achter_mij_input = st.text_input("Voer de stacks van spelers achter jou die nog kunnen inzetten (gescheiden door spaties):")
        stacks_achter_mij = list(map(int, stacks_achter_mij_input.split())) if stacks_achter_mij_input else []

        # Voeg jouw stack, de stacks voor je en achter je samen
        total_stacks = [mijn_stack] + stacks_voor_mij + stacks_achter_mij

        # Bereken jouw stack in termen van big blinds
        if big_blind > 0:
            mijn_stack_in_bb = mijn_stack / big_blind

            # Bereken ICM-waarden
            if st.button("Bereken ICM en Nash Push/Fold Beslissing"):
                icm_values = icm_calculate(total_stacks, payouts)

                # Resultaten tonen
                st.subheader("ICM Berekeningen")
                for i, value in enumerate(icm_values):
                    st.write(f"Stack: {total_stacks[i]} chips | ICM waarde = {value:.2f}")
                
                # Nash push/fold-beslissing op basis van je hand en je eigen stackgrootte
                beslissing, advies = nash_push_fold(mijn_stack_in_bb, hand)
                st.subheader("Nash Push/Fold-beslissing")
                st.write(f"Beslissing: {beslissing}")
                st.write(f"Advies: {advies}")

# Start de Streamlit applicatie
if __name__ == "__main__":
    main()
