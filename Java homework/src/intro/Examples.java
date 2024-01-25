package intro;

public class Examples {

    public static void main(String[] args) {

        // print to the console
        System.out.println("Hello!"); // Hello!

        // loop from 0 to 2
        for (int i = 0; i < 3; i++) {
            System.out.println(i); // 0 ...
        }

        // concatenate two strings
        // NB! double quotes
        String concatenated = "aa" + "bb";
        System.out.println(concatenated); // aabb

        // get single letter (character) from a string
        System.out.println(concatenated.charAt(2)); // b

        // add single letter to a string
        // NB! Letters are in single quotes.
        concatenated =  concatenated + 'c';
        System.out.println(concatenated); // aabbc

        // get string length
        System.out.println(concatenated.length()); // 5

        // compare two letters
        // NB! Letter is different from one letter string ("a" != 'a')
        if (concatenated.charAt(2) == 'b') {
            System.out.println(true); // true
        }

        // use modulo operator to check whether number is even or odd
        if (4 % 2 == 0) {
            System.out.println("even");
        }
        if (5 % 2 == 1) {
            System.out.println("odd");
        }

    }
}
