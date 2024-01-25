package reflection.samples;

import java.lang.reflect.Method;

public class AccessOriginalException {

    public static void main(String[] args) throws Exception {

        Method method = AccessOriginalException.class
                .getDeclaredMethod("methodThatTrows");

        AccessOriginalException instance = new AccessOriginalException();

        try {
            method.invoke(instance);
        } catch (Exception e) {
            System.out.println(e); // ... InvocationTargetException

            System.out.println(e.getCause()); // ... RuntimeException

            System.out.println(e.getCause().getMessage()); // hello
        }
    }

    public void methodThatTrows() {
        throw new RuntimeException("hello");
    }

}
