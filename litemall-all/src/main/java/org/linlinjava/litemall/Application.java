package org.linlinjava.litemall;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@SpringBootApplication(scanBasePackages = {"org.linlinjava.litemall"})
@MapperScan("org.linlinjava.litemall.db.dao")
@EnableTransactionManagement
@EnableScheduling
public class Application {

    public static void main(String[] args) throws Exception {
//        SpringApplication.run(Application.class, args);

        double lilv = 0.03001;
        double year = 10;
        double benjin = 50000;
        double benxi = 50000;
        for(int i = 1;i<=5;i++){
            benxi = benxi*(1+lilv);
            System.out.println("第"+i+"年末本息:"+benxi);
        }

    }

}