package com.example.smart_learn.controller;



import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class StatusController {

    // This variable holds the current status for the whole app
    public static String currentStatus = "READY";

    // 1. Python calls this to UPDATE the status
    // Example: http://localhost:8080/api/update?status=SLEEPING
    @GetMapping("/update")
    public String updateStatus(@RequestParam String status) {
        currentStatus = status;
        System.out.println("⚠️ Received Status Update: " + status);
        return "Status updated to: " + status;
    }

    // 2. The Dashboard calls this to READ the status
    @GetMapping("/status")
    public String getStatus() {
        return currentStatus;
    }
}