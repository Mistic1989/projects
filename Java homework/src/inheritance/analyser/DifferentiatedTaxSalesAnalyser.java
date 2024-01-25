package inheritance.analyser;

import java.util.List;

public final class DifferentiatedTaxSalesAnalyser extends AbstractSalesAnalyser {

    public DifferentiatedTaxSalesAnalyser(List<SalesRecord> records) {
        super(records);
    }

    protected Double getTaxRate() {
        return 0.2;
    }

    protected String getClassName() {
        return "DifferentiatedTaxSalesAnalyser";
    }
}