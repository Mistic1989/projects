package reflection;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import reflection.serializer.SerializerTests;
import reflection.tester.TestRunnerTests;

@RunWith(Suite.class)
@Suite.SuiteClasses({
        SerializerTests.class,
        TestRunnerTests.class})
public class TestSuite {

}