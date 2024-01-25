package reflection.tester;

public class ExampleTests2 {

    @MyTest(expected = RuntimeException.class)
    public void test3() {
        throw new IllegalStateException();
    }

    @MyTest(expected = IllegalStateException.class)
    public void test4() {
        throw new RuntimeException();
    }

    @MyTest(expected = IllegalStateException.class)
    public void test5() {
        throw new IllegalStateException();
    }

    @MyTest(expected = IllegalStateException.class)
    public void test6() {
    }

    public void helperMethod() {
    }


}
