package com.example.smart_learn;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class })
public class SmartLearnApplication {

	public static void main(String[] args) {
		SpringApplication.run(SmartLearnApplication.class, args);
	}

}
