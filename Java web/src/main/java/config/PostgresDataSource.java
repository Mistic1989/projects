package config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;

//@Profile("postgres")
@Configuration
public class PostgresDataSource {

    private Environment env;
    public PostgresDataSource(Environment env) {
        this.env = env;
    }

    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource ds = new DriverManagerDataSource();
        ds.setDriverClassName("org.postgresql.Driver");
        ds.setUsername(env.getProperty("dbUser"));
        ds.setPassword(env.getProperty("dbPassword"));
        ds.setUrl(env.getProperty("dbUrl"));

        return ds;
    }

    @Bean("dialect")
    public String dialect() {
        return "org.hibernate.dialect.PostgreSQLDialect";
    }

}