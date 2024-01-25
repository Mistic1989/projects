package config;

import org.springframework.context.annotation.*;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;

//@Profile("hsql")
@Configuration
public class HsqlDataSource {

    @Bean
    public DataSource dataSource(Environment env) {
        DriverManagerDataSource ds = new DriverManagerDataSource();
        ds.setDriverClassName("org.hsqldb.jdbcDriver");
        ds.setUrl(env.getProperty("hsql.url"));

        return ds;
    }

    @Bean("dialect")
    public String dialect() {
        return "org.hibernate.dialect.HSQLDialect";
    }
}