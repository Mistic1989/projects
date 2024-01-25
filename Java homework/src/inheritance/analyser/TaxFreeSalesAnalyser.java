package inheritance.analyser;

import java.util.List;

public final class TaxFreeSalesAnalyser extends AbstractSalesAnalyser {

    public TaxFreeSalesAnalyser(List<SalesRecord> records) {
        super(records);
    }

    protected Double getTaxRate() {
        return 0.0;
    }

    protected String getClassName() {
        return "TaxFreeSalesAnalyser";
    }
}