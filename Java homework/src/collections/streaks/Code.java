package collections.streaks;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

public class Code {

    public static List<List<String>> getStreakList(String input) {
        LinkedList<List<String>> streaks = new LinkedList<>();

        for (Character character : input.toCharArray()) {

            String currentSymbol = String.valueOf(character);

            if (streaks.size() == 0)  {
                streaks.add(new LinkedList<>(Arrays.asList(currentSymbol)));
            } else if (streaks.getLast().contains(currentSymbol)) {
                streaks.getLast().add(currentSymbol);
            } else {
                streaks.add(new LinkedList<>(Arrays.asList(currentSymbol)));
            }
        }

        return streaks;
    }
}