package reflection.samples;

public class Deprecation {

    public static void main(String[] args) throws Exception {

        new MySampleClass3().someOldMethod();

        // real deprecation example from Java SDK
        MySampleClass3.class.newInstance();
    }

}
