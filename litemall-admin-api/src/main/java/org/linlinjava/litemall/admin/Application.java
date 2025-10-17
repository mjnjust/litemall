package org.linlinjava.litemall.admin;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@SpringBootApplication(scanBasePackages = {"org.linlinjava.litemall.db", "org.linlinjava.litemall.core",
        "org.linlinjava.litemall.admin"})
@MapperScan("org.linlinjava.litemall.db.dao")
@EnableTransactionManagement
@EnableScheduling
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
//        System.out.println(InitExample.value);
    }

    public static class InitExample {
        public static int value = 50;             // 2. 再执行赋值

        static {
            System.out.println("静态代码块执行");  // 1. 先执行
            value = 100;
        }

        static {
            System.out.println("value = " + value); // 输出：value = 50
        }
    }

}