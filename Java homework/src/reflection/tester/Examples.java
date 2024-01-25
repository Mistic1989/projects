package reflection.tester;

import java.util.Arrays;

public class Examples {

    public static void main(String[] args) throws Exception {

        Class<?> aClass = Class.forName("reflection.tester.ExampleTests1");

        System.out.println(Arrays.toString(aClass.getMethods()));

        Class<? extends Throwable> expected = RuntimeException.class;
        // expected = IllegalArgumentException.class;

        if (expected.isAssignableFrom(IllegalStateException.class)) {
            System.out.println("ok");
        }


    }

}
