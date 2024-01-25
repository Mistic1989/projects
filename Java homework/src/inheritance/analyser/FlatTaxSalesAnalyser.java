package inheritance.analyser;

import java.util.List;

public final class FlatTaxSalesAnalyser extends AbstractSalesAnalyser {


    public FlatTaxSalesAnalyser(List<SalesRecord> records) {
        super(records);
    }

    protected Double getTaxRate() {
        return 0.2;
    }

    protected String getClassName() {
        return "FlatTaxSalesAnalyser";
    }
}