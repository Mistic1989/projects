package config.security;

import config.security.handlers.ApiAccessDeniedHandler;
import config.security.handlers.ApiEntryPoint;
import config.security.handlers.ApiLogoutSuccessHandler;
import config.security.jwt.JwtAuthenticationFilter;
import config.security.jwt.JwtAuthorizationFilter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.PropertySource;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.JdbcUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.intercept.AuthorizationFilter;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.servlet.util.matcher.MvcRequestMatcher;
import org.springframework.web.servlet.handler.HandlerMappingIntrospector;

import javax.sql.DataSource;

import static org.springframework.security.web.util.matcher.AntPathRequestMatcher.antMatcher;

@EnableWebSecurity
@EnableMethodSecurity
@PropertySource("classpath:/application.properties")
public class SecurityConfig {

    @Value("${jwt.signing.key}")
    private String jwtKey;

    private final MvcRequestMatcher.Builder mvc;

    public SecurityConfig(HandlerMappingIntrospector introspector) {
        this.mvc = new MvcRequestMatcher.Builder(introspector);
    }

    @Bean
    public UserDetailsService userDetailService(DataSource dataSource) {
        return new JdbcUserDetailsManager(dataSource);
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

//        http.formLogin(withDefaults());

        http.authorizeHttpRequests(conf -> conf
                .requestMatchers(mvcMatcher("/version")).permitAll()
                .requestMatchers(mvcMatcher("/login")).permitAll()
                .requestMatchers(mvcMatcher("/**")).authenticated()
                .requestMatchers(mvcMatcher("/users/**")).hasRole("ADMIN")

                .requestMatchers(antMatcher("/static/**")).permitAll()


        );

        http.logout(conf -> conf
                .logoutSuccessHandler(new ApiLogoutSuccessHandler())
                .logoutUrl("/logout"));

        http.csrf(AbstractHttpConfigurer::disable);

        http.exceptionHandling(conf -> conf
                .authenticationEntryPoint(new ApiEntryPoint())
                .accessDeniedHandler(new ApiAccessDeniedHandler()));

        http.apply(new FilterConfigurer());

        return http.build();
    }

    public class FilterConfigurer extends AbstractHttpConfigurer<FilterConfigurer, HttpSecurity> {
        @Override
        public void configure(HttpSecurity http) {
            AuthenticationManager manager = http.getSharedObject(AuthenticationManager.class);

//            var loginFilter = new ApiAuthenticationFilter(
//                    manager, "/api/login");

//            http.addFilterBefore(loginFilter,
//                    UsernamePasswordAuthenticationFilter.class);

            var loginFilter = new JwtAuthenticationFilter(
                    manager, "/api/login", jwtKey);

            http.addFilterBefore(loginFilter,
                UsernamePasswordAuthenticationFilter.class);

            var authorizationFilter = new JwtAuthorizationFilter(jwtKey);

            http.addFilterBefore(authorizationFilter, AuthorizationFilter.class);
        }
    }

    @Bean
    public static PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public WebSecurityCustomizer webSecurityCustomizer() {
        return web -> web.debug(false);
    }

    private MvcRequestMatcher mvcMatcher(String pattern) {
        return mvc.pattern(pattern);
    }
}