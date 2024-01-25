package collections.simulator;

import java.util.*;

import static collections.simulator.Helpers.getSuitedHand;

public class Simulator implements Iterable<Card> {

    Hand player1hand = null;
    Hand player2hand = null;
    private final List<Card> cards = new ArrayList<>();
    public static void main(String[] args) {
        Hand hand1 = getSuitedHand("9h9s");
        Hand hand2 = getSuitedHand("AdKc");

        Simulator simulator = new Simulator(7e4);

        double winningOdds = simulator.getWinningOdds(hand1, hand2);

        System.out.println(winningOdds);
    }

    @SuppressWarnings("PMD.UnusedPrivateField")
    private double iterations;

    public Simulator(double iterations) {
        this.iterations = iterations;
    }

    public Map<HandType, Double> calculateProbabilities() {

        Map<Integer, Card> packOfCards = getPackOfCards();
        Map<HandType, Double> result = new HashMap<>();

        Double count1 = 0.0;
        Double count2 = 0.0;
        Double count3 = 0.0;
        Double count4 = 0.0;

        for (int j = 0; j < iterations; j++) {

            Map<Integer, Card> tempPackOfCards = new HashMap<>();
            Hand hand = drawHand(packOfCards, tempPackOfCards, false);

            HandType handType = hand.getHandType();
            switch (handType) {
                case HIGH_CARD -> count1++;
                case ONE_PAIR -> count2++;
                case TWO_PAIRS -> count3++;
                case TRIPS -> count4++;
                default -> count1 += 0;
            }
        }

        result.put(HandType.HIGH_CARD, (count1 / iterations) * 100);
        result.put(HandType.ONE_PAIR, (count2 / iterations) * 100);
        result.put(HandType.TWO_PAIRS, (count3 / iterations) * 100);
        result.put(HandType.TRIPS, (count4 / iterations) * 100);

        return result;
    }

    private static Map<Integer, Card> getPackOfCards() {
        Map<Integer, Card> packOfCards = new HashMap<>();
        Integer suit = 0;
        Integer value = 0;
        for (int i = 0; i < 52; i++) {
            packOfCards.put(i, new Card(Card.CardValue.values()[value], Card.CardSuit.values()[suit]));
            value++;
            if (value > 12) {
                value = 0;
                suit++;
            }
        }
        return packOfCards;
    }

    private Hand drawHand(Map<Integer, Card> packOfCards, Map<Integer, Card> tempPackOfCards, Boolean texasHoldEm) {
        int i = 0;
        List<Card> cardList = new ArrayList<>();

        while (i < 5) {
            Integer randomIndex = new Random().nextInt(0, 52);
            Card cardVal = packOfCards.get(randomIndex);
            if (tempPackOfCards.size() == 52 && !texasHoldEm) {
                tempPackOfCards = new HashMap<>();
            }
            tempPackOfCards = initPackOfCardsIfTexasHoldem(tempPackOfCards);

            if (tempPackOfCards.containsKey(randomIndex)) {
                continue;
            }
            Boolean hasDuplicate = false;
            if (!cardList.isEmpty()) {
                hasDuplicate = getHasDuplicate(cardList, cardVal, hasDuplicate);
                if (!hasDuplicate) {
                    cardList.add(new Card(cardVal.getValue(), cardVal.getSuit()));
                    tempPackOfCards.put(randomIndex, new Card(cardVal.getValue(), cardVal.getSuit()));
                    i++;
                }
            } else {
                cardList.add(new Card(cardVal.getValue(), cardVal.getSuit()));
                tempPackOfCards.put(randomIndex, new Card(cardVal.getValue(), cardVal.getSuit()));
                i++;
            }
        }
        Hand hand = new Hand();
        for (Card card : cardList) {
            hand.addCard(card);
        }
        return hand;
    }

    private static Boolean getHasDuplicate(List<Card> cardList, Card cardVal, Boolean hasDuplicate) {
        for (Card card : cardList) {
            if (card.getValue() == cardVal.getValue() && card.getSuit() == cardVal.getSuit()) {
                hasDuplicate = true;
                break;
            }
        }
        return hasDuplicate;
    }

    private Map<Integer, Card> initPackOfCardsIfTexasHoldem(Map<Integer, Card> tempPackOfCards) {
        if (tempPackOfCards.size() == 52) {
            tempPackOfCards = new HashMap<>();
            Integer count = 0;
            for (Card card : player1hand) {
                tempPackOfCards.put(count, card);
                count++;
            }
            for (Card card : player2hand) {
                tempPackOfCards.put(count, card);
                count++;
            }
        }
        return tempPackOfCards;
    }

    public double getWinningOdds(Hand player1hand, Hand player2hand) {

        this.player1hand = player1hand;
        this.player2hand = player2hand;
        Double count1 = 0.0;
        Double count2 = 0.0;
        Map<Integer, Card> tempPackOfCards = new HashMap<>();

        for (int j = 0; j < iterations; j++) {
            Hand hand1 = new Hand();
            Hand hand2 = new Hand();

            createHands(player1hand, player2hand, tempPackOfCards, hand1, hand2);

            HandType hand1Type = hand1.getHandType();
            HandType hand2Type = hand2.getHandType();

            if (hand1Type == hand2Type) {
                Integer compare = hand1.compareTo(hand2);
                if (compare == 1) {
                    count1++;
                }
                if (compare == -1) {
                    count2++;
                }
            }

            if (List.of(HandType.values()).indexOf(hand1Type) > List.of(HandType.values()).indexOf(hand2Type)) {
                count1++;
            }
            if (List.of(HandType.values()).indexOf(hand1Type) < List.of(HandType.values()).indexOf(hand2Type)) {
                count2++;
            }
        }

        if (count1 > count2) {
            return (count1 / iterations) * 100;
        } else {
            return (count2 / iterations) * 100;
        }
    }

    private void createHands(Hand player1hand, Hand player2hand, Map<Integer, Card> tempPackOfCards, Hand hand1, Hand hand2) {
        Hand hand = drawHand(getPackOfCards(), tempPackOfCards, true);
        for (Card card : hand) {
            hand1.addCard(card);
            hand2.addCard(card);
        }
        for (Card card : player1hand) {
            hand1.addCard(card);
        }
        for (Card card : player2hand) {
            hand2.addCard(card);
        }
    }

    @Override
    public Iterator<Card> iterator() {
        return cards.iterator();
    }
}
