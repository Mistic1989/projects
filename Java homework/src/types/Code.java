package types;

import java.util.Arrays;
import java.util.Random;

public class Code {

    public static void main(String[] args) {

        int[] numbers = {1, 3, -2, 9};
        int[] numbers2 = {1, 2};
        int[] numbers3 = {};

        System.out.println(sum(numbers)); // 11
        System.out.println(average(numbers2));
        System.out.println(minimumElement(numbers3));
        System.out.println(asString(numbers3));
        System.out.println(mode("ac"));
        System.out.println(squareDigits("a9b2"));
        System.out.println(isolatedSquareCount());
    }

    public static int sum(int[] numbers) {
        Integer result = 0;
        for (Integer number : numbers) {
            result += number;
        }

        return result;
    }

    public static double average(int[] numbers) {
        Double sum = 0.0;
        for (Integer number : numbers) {
            sum += number;
        }

        return sum / numbers.length;
    }

    public static Integer minimumElement(int[] integers) {
        if (integers.length == 0) {
            return null;
        }

        Integer min = integers[0];
        for (Integer element : integers) {
            if (element < min) {
                min = element;
            }
        }

        return min;
    }

    public static String asString(int[] elements) {
        String result = "";
        if (elements.length > 0) {
            for (int i = 0; i < elements.length; i++) {
                if (i < elements.length - 1) {
                    result += elements[i] + ", ";
                }
            }
            result += elements[elements.length - 1];
        }

        return result;
    }

    public static Character mode(String input) {
        if (input.length() > 1) {
            int finalCount = 1;
            int tempCount = 1;
            String tempResult = "";
            String finalResult = "";
            String[] split = input.split("");
            Arrays.sort(split);
            for (int i = 0; i < input.length() - 1; i++) {
                if (split[i].equals(split[i + 1])) {
                    tempResult = split[i];
                    tempCount++;
                }
                if (tempCount >= finalCount) {
                    finalCount = tempCount;
                    finalResult = tempResult;
                }
                if (!split[i].equals(split[i + 1])) {
                    tempResult = split[i];
                    tempCount = 1;
                }
            }
            if (finalResult.isEmpty()) {
                return tempResult.charAt(0);
            }
            return finalResult.charAt(0);
        }
        if (input.length() == 1) {
            return input.charAt(0);
        }

        return null;
    }

    public static String squareDigits(String s) {
        String result = "";
        char[] symbols = s.toCharArray();
        for (Character symbol : symbols) {
            if (Character.isDigit(symbol)) {
                Integer number = Integer.parseInt(Character.toString(symbol));
                result += number * number;
                continue;
            }
            result += symbol;
        }

        return result;
    }

    private static int upperCorners(int i, int j, boolean[][] matrix) {
        int addJ = 0;
        if (j == matrix.length - 1) {
            addJ = 2;
        }
        if (i == 0 && (j == 0 || j == matrix.length - 1)
                && !matrix[i][j + 1 - addJ] && !matrix[i + 1][j]
                && !matrix[i + 1][j + 1 - addJ]) {

            return 1;
        }
        if (i == 0 && !matrix[i][j + 1 - addJ] && !matrix[i + 1][j] && !matrix[i + 1][j + 1 - addJ]
                && !matrix[i][j - 1 - addJ] && !matrix[i + 1][j - 1 - addJ]) {

            return  1;
        }
        return 0;
    }

    private static int bottomCorners(int i, int j, boolean[][] matrix) {
        int addJ = 0;
        if (j == matrix.length - 1) {
            addJ = 2;
        }
        if (i == matrix.length - 1 && !matrix[i][j + 1 - addJ]
                && !matrix[i - 1][j] && !matrix[i - 1][j + 1 - addJ]) {

            return 1;
        }
        return 0;
    }

    private static int sides(int i, int j, boolean[][] matrix) {
        int addJ = 0;
        if (j == matrix.length - 1) {
            addJ = 2;
        }
        if ((j == 0 || j == matrix.length - 1) && i > 0 && i < matrix.length - 1
                && !matrix[i][j + 1 - addJ] && !matrix[i + 1][j] && !matrix[i + 1][j + 1 - addJ]
                && !matrix[i - 1][j + 1 - addJ] && !matrix[i - 1][j]) {

            return 1;
        }

        return 0;
    }

    private static int middlePart(int i, int j, boolean[][] matrix) {
        int addJ = 0;
        if (j == matrix.length - 1) {
            addJ = 2;
        }
        if (i > 0 && i < matrix.length - 1 && j > 0 && j < matrix.length - 1
                && !matrix[i][j + 1 - addJ] && !matrix[i + 1][j]
                && !matrix[i + 1][j + 1 - addJ]
                && !matrix[i - 1][j + 1 - addJ] && !matrix[i - 1][j]
                && !matrix[i - 1][j - 1] && !matrix[i][j -1]
                && !matrix[i + 1][j - 1]) {

            return 1;
        }

        return 0;
    }

    public static int isolatedSquareCount() {
        boolean[][] matrix = getSampleMatrix();

        printMatrix(matrix);

        int isolatedCount = 0;
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix.length; j++) {
                isolatedCount += upperCorners(i, j, matrix);
                isolatedCount += bottomCorners(i, j ,matrix);
                isolatedCount += sides(i, j, matrix);
                isolatedCount += middlePart(i, j, matrix);
            }
        }

        return isolatedCount;
    }

    private static void printMatrix(boolean[][] matrix) {
        for (boolean[] row : matrix) {
            System.out.println(Arrays.toString(row));
        }
    }

    private static boolean[][] getSampleMatrix() {
        boolean[][] matrix = new boolean[10][10];

        Random r = new Random(5);
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                matrix[i][j] = r.nextInt(5) < 2;
            }
        }

        return matrix;
    }
}