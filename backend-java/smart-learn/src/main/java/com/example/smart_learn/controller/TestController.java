package com.example.smart_learn.controller;


import org.springframework.web.bind.annotation.CrossOrigin; // Import this!
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin(origins = "http://localhost:3000") // <--- ADD THIS LINE
public class TestController {

    @GetMapping("/hello")
    public String sayHello() {
        return "Active (Connected)";
    }
}