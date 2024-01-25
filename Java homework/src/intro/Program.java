package intro;

public class Program {

    public static void main(String[] args) {

        int decimal = asDecimal("11001101");

        System.out.println(decimal); // 205
        System.out.println(pow(2, 2));
        System.out.println(asDecimal(" 11001101"));
        System.out.println(asString(205));
    }

    public static String asString(int input) {
        String result = "";
        while (input > 0) {
            if (input % 2 == 0) {
                result += '0';
            }
            else {
                result += '1';
            }
            input = input / 2;
        }
        return reverse(result);
    }

    public static int asDecimal(String input) {
        int result = 0;
        input = reverse(input);
        for (int i = 0; i < input.length(); i++) {
            if (input.charAt(i) == '1') {
                result += pow(2, i);
            }
        }
        return result;
    }

    private static String reverse(String input) {
        String result = "";
        for (int i = 0; i < input.length(); i++) {
            result = input.charAt(i) + result;
        }
        return result;
    }

    private static int pow(int arg, int power) {
        int result = 1;
        for (int i = 0; i < power; i++) {
            result = result * arg;
        }
        return result;
    }
}
