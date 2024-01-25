package reflection.tester;

public class ExampleTests1 {

    @MyTest
    public void test1() {
    }

    @MyTest
    public void test2() {
        throw new RuntimeException();
    }

}
