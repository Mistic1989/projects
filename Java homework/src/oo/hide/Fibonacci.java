package oo.hide;

public class Fibonacci {

    private int currentValue = 0;
    private int next = 1;

    public int nextValue() {
        int result = currentValue;

        currentValue = next;
        next = next + result;
        return result;
    }
}