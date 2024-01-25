package collections.benchmark;

import oo.hide.Timer;
import org.junit.Test;

import java.util.HashSet;
import java.util.Set;
import java.util.TreeSet;


public class Runner {

    @Test
    public void benchmarkDifferentImplementations() {

        Set<Integer> set1 = new MySet();
        Set<Integer> set2 = new TreeSet<>();
        Set<Integer> set3 = new HashSet<>();

        benchmark(set1);
        benchmark(set2);
        benchmark(set3);
    }

    private static void benchmark(Set<Integer> set) {
        Timer timer = new Timer();

        for (int i = 0; i < 50000; i++) {
            set.add(i);
        }

        System.out.println(timer.getPassedTime());
    }

}
