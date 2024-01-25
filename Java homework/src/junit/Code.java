package junit;

import java.util.Arrays;

public class Code {

    public static void main(String[] args) {
        System.out.println(isSpecial(4));
        System.out.println(getCharacterCount("aabbb", 'b'));
        System.out.println(mode("cbbc"));
        System.out.println(longestStreak("cbbc"));
        int[] newArray2 = {1, 1, 2, 3};
        int[] newArray = {0, 1, 1, 2, 1, 3, 3, 2, 2, 2, 2, 9, 0};
        System.out.println(Arrays.toString(removeDuplicates(newArray)));
        System.out.println(sumIgnoringDuplicates(newArray2));
    }

    public static boolean isSpecial(int candidate) {
        return candidate % 11 == 0 || candidate % 11 <= 3 && candidate % 11 > 0;
    }

    public static Character mode(String inputString) {
        if (inputString == null) {
            return null;
        }

        int count = 0;
        Character temp = null;
        for (int i = 0; i < inputString.length(); i++) {
            int tempCount = getCharacterCount(inputString, inputString.charAt(i));
            if (tempCount > count) {
                count = tempCount;
                temp = inputString.charAt(i);
            }
        }
        return temp;

    }

    public static int getCharacterCount(String allCharacters, char targetCharacter) {
        if (allCharacters == null) {
            return 0;
        }
        int count = 0;
        for (int i = 0; i < allCharacters.length(); i++) {
            if (allCharacters.charAt(i) == targetCharacter) {
                count++;
            }
        }
        return count;
    }

    public static int longestStreak(String inputString) {
        if (inputString.isEmpty()) {
            return 0;
        }

        int result = 0;
        int temp = 0;
        char tempChar = inputString.charAt(0);
        for (int i = 0; i < inputString.length(); i++) {
            if (tempChar == inputString.charAt(i)) {
                temp += 1;
                continue;
            }
            if (temp > result) {
                result = temp;
            }
            temp = 1;
            tempChar = inputString.charAt(i);
        }
        if (temp > result) {
            result = temp;
        }
        return result;
    }

    public static int[] removeDuplicates(int[] integers) {
        int[] tempArray = new int[integers.length];
        int count = 0;
        int countZeroes = 0;

        for (int integer : integers) {
            if (integer == 0 && countZeroes < 1) {
                tempArray[count] = integer;
                count++;
                countZeroes++;
                continue;
            }
            if (!isItemInArray(integer, tempArray)) {
                tempArray[count] = integer;
                count++;
            }
        }
        int[] result = new int[count];

        for (int i = 0; i < count; i++) {
            result[i] = tempArray[i];
        }
        return result;
    }

    public static boolean isItemInArray(int number, int[] integerArray) {
        for (int j : integerArray) {
            if (number == j) {
                return true;
            }
        }
        return false;
    }

    public static int sumIgnoringDuplicates(int[] integers) {
        int[] duplicatesRemoved = removeDuplicates(integers);
        int result;

        if (duplicatesRemoved.length > 1) {
            result = duplicatesRemoved[0];
            for (int i = 0; i < duplicatesRemoved.length - 1; i++) {
                result += duplicatesRemoved[i + 1];
            }
            return result;

        } else {
            return duplicatesRemoved[0];
        }
    }
}