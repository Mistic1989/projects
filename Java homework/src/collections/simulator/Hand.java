package collections.simulator;

import java.util.*;

import static collections.simulator.Helpers.getHand;

public class Hand implements Iterable<Card>, Comparable<Hand> {

    private Boolean isFlush = false;

    private final List<Card> cards = new ArrayList<>();

    public static void main(String[] args) {
        System.out.println(getHand("64777").getHandType());
    }

    public void addCard(Card card) {
        cards.add(card);
    }

    @Override
    public String toString() {
        return cards.toString();
    }

    public HandType getHandType() {

        Set<Card.CardValue> set = new HashSet<>();
        for (Card card : cards) {
            set.add(card.getValue());
        }
        // Find unique card values (suit is not important)
        List<Card.CardValue> uniqueCardValues = new ArrayList<>();
        for (Card card : cards) {
            if (!uniqueCardValues.contains(card.getValue())) {
                uniqueCardValues.add(card.getValue());
            }
        }

        // Count the cards and add these to the dictionary ('map').
        // Straights will not be handled here. findStraight() function is used to find straights.
        cards.sort(Collections.reverseOrder());
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 0);
        map.put(1, 0);
        Integer countFlush = 0;
        Integer countCards = 0;
        Integer key = 0;

        for (Card.CardValue cardValue : uniqueCardValues) {
            for (Card card : cards) {
                if (cardValue == card.getValue()) {
                    countCards++;
                }
            }
            if (countCards > 1) {
                map.put(key, countCards);
                key++;
            }
            countCards = 0;
        }
        countFlush(countFlush);
        return handMatch(map, set);
    }

    private void countFlush(Integer countFlush) {
        for (int i = 0; i < cards.size() - 1; i++) {
            String currentSuit = cards.get(i).getSuit().toString();
            String nextSuit = cards.get(i + 1).getSuit().toString();

            if (Objects.equals(currentSuit, nextSuit)) {
                countFlush++;
            }
        }

        if (countFlush == 4) {
            isFlush = true;
        }
    }

    private HandType handMatch(Map<Integer, Integer> map, Set<Card.CardValue> set) {

        Integer cardCount1 = map.get(0);
        Integer cardCount2 = map.get(1);

        // Collect data if certain hand exists or not (true or false) to the list
        List<Boolean> booleans = handBooleans(cardCount1, cardCount2, set);

        Boolean onePair = booleans.get(0);
        Boolean twoPairs = booleans.get(1);
        Boolean trips = booleans.get(2);
        Boolean babyStraight = booleans.get(3);
        Boolean straight = booleans.get(4);
        Boolean flush = booleans.get(5);
        Boolean fullHouse = booleans.get(6);
        Boolean fourOfAKind = booleans.get(7);
        Boolean straightFlush = booleans.get(8);

        // Add all the booleans of different hands to the dictionary
        Map<HandType, Boolean> finalResult = new HashMap<>();

        finalResult.put(HandType.FLUSH, flush);
        finalResult.put(HandType.STRAIGHT_FLUSH, straightFlush);
        if (babyStraight) {
            finalResult.put(HandType.STRAIGHT, true);
        } else {
            finalResult.put(HandType.STRAIGHT, straight);
        }
        finalResult.put(HandType.FOUR_OF_A_KIND, fourOfAKind);
        finalResult.put(HandType.FULL_HOUSE,fullHouse);
        finalResult.put(HandType.TRIPS, trips);
        finalResult.put(HandType.TWO_PAIRS, twoPairs);
        finalResult.put(HandType.ONE_PAIR, onePair);

        // Return the final result (HandType)
        for (Map.Entry<HandType, Boolean> item : finalResult.entrySet()) {
            if (item.getValue()) {
                return item.getKey();
            }
        }

        // If any previous conditions didn't match, return High Card
        return HandType.HIGH_CARD;
    }

    public List<Boolean> handBooleans(Integer cardCount1, Integer cardCount2, Set<Card.CardValue> set) {

        Boolean flush = isFlush;
        Boolean babyStraight = cards.get(0).getValue() == Card.CardValue.A
                && cards.get(1).getValue() == Card.CardValue.S5
                && cards.get(2).getValue() == Card.CardValue.S4
                && cards.get(3).getValue() == Card.CardValue.S3
                && cards.get(4).getValue() == Card.CardValue.S2;
        Boolean straight = findStraight(set) != null;
        Boolean straightFlush = straight && flush;
        Boolean fourOfAKind = cardCount1 == 4 || cardCount2 == 4;
        Boolean fullHouse = cardCount1 == 3 && cardCount2 == 2 || cardCount1 == 2 && cardCount2 == 3;
        Boolean trips = cardCount1 == 3 && cardCount2 == 0 || cardCount1 == 0 && cardCount2 == 3;
        Boolean twoPairs = cardCount1 == 2 && cardCount2 == 2;
        Boolean onePair = set.size() == cards.size() - 1;

        if (fullHouse) {
            flush = false;
        }
        if (straightFlush) {
            flush = false;
            straight = false;
        }

        return new ArrayList<>(Arrays.asList(onePair, twoPairs, trips, babyStraight, straight,
                flush, fullHouse, fourOfAKind, straightFlush));
    }

    private HandType findStraight(Set<Card.CardValue> set) {

        if (set.size() != 5) {
            return null;
        }

        Integer startIndex = null;
        Integer finalIndex = 0;

        startIndex = searchCardValues(startIndex, finalIndex, set).get(0);
        finalIndex = searchCardValues(startIndex, finalIndex, set).get(1);

        if (startIndex != null && (finalIndex - startIndex) - 4 == 0) {
            return HandType.STRAIGHT;
        }
        return null;
    }

    private List<Integer> searchCardValues(Integer startIndex, Integer finalIndex, Set<Card.CardValue> set) {
        for (int i = 0; i < Card.CardValue.values().length; i++) {
            Card.CardValue value = Card.CardValue.values()[i];
            if (set.contains(value)) {
                finalIndex++;
                if (startIndex == null) {
                    startIndex = 0;
                    startIndex++;
                }
                continue;
            }
            if (startIndex != null && (finalIndex - startIndex) - 4 == 0) {
                break;
            }
            finalIndex = 0;
        }

        return new ArrayList<>(Arrays.asList(startIndex, finalIndex));
    }

    public boolean contains(Card card) {
        return cards.contains(card);
    }

    public boolean isEmpty() {
        return cards.isEmpty();
    }

    @Override
    public Iterator<Card> iterator() {
        return cards.iterator();
    }

    @Override
    public int compareTo(Hand other) {
        cards.sort(Collections.reverseOrder());
        other.cards.sort(Collections.reverseOrder());
        List<Card> highestCards = cards.subList(0, cards.size());
        List<Card> otherHighestCards = other.cards.subList(0, other.cards.size());

        for (int i = 0; i < cards.size(); i++) {
            Integer temp = highestCards.get(i).compareTo(otherHighestCards.get(i));
            if (temp != 0) {
                return temp;
            }
        }

        return 0;
    }
}
