package exceptions.bad;

public class BadTryCatch {

    public static void main(String[] args) {
        System.out.println(new BadTryCatch().containsSingleLetters("aabc"));;
    }
    public boolean containsSingleLetters(String input) {

        int index = 0;

        if (input != null) {
            while (index < input.length() - 1) {
                if (input.charAt(index) == input.charAt(index + 1)) {
                    return false;
                }

                index++;
            }

            return true;
        }
        return false;
    }
}
