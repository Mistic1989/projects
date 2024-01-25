package inheritance.calc;

public class TaxFreePayCalculator extends PayCalculator {

    protected Double getTaxRate() {
        return 0.0;
    }
}
