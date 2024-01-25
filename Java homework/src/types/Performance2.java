package types;

public class Performance2 {

    public static void main(String[] args) {

        double start = System.currentTimeMillis();

        int x = 1;
        int y = 2;
        double r = 0.0;
        for (int i = 0; i < 1e9; i++) {
            r += x / y;
        }

        System.out.println((System.currentTimeMillis() - start) / 1000);
    }

}
