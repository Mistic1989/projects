package reflection.tester;

import org.junit.Test;

import java.util.List;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.not;
import static org.junit.Assert.assertThat;

public class TestRunnerTests {

    @Test
    public void runsTestsFromDecoupledFiles() {

        List<String> testClassNames = List.of(
                "reflection.tester.ExampleTests1", "reflection.tester.ExampleTests2");

        TestRunner testRunner = new TestRunner();

        testRunner.runTests(testClassNames);

        String result = testRunner.getResult();

        assertThat(result, containsString("test1() - OK"));
        assertThat(result, containsString("test2() - FAILED"));
        assertThat(result, containsString("test3() - OK"));
        assertThat(result, containsString("test4() - FAILED"));
        assertThat(result, containsString("test5() - OK"));
        assertThat(result, containsString("test6() - FAILED"));

        assertThat(result, not(containsString("helperMethod()")));
    }
}