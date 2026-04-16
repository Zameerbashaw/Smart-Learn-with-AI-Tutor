package com.example.smart_learn.controller;



import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.ArrayList;
import java.util.List;

// Data Structure for Courses
class Course {
    public String id;
    public String title;
    public String category;
    public String thumbnail;

    public Course(String id, String title, String category) {
        this.id = id;
        this.title = title;
        this.category = category;
        // Generates a cool dark-themed thumbnail automatically
        this.thumbnail = "https://placehold.co/600x400/1e3c72/FFF?text=" + title.replace(" ", "+");
    }
}

@Controller
public class WebsiteController {

    // 1. HOME PAGE (The Entry Point)
    @GetMapping("/")
    public String showHome(Model model) {
        List<Course> courses = new ArrayList<>();
        
        // --- ADD YOUR 20 VIDEOS HERE ---
        // Make sure these filenames match what is in your "static/videos" folder
        courses.add(new Course("java1", "Java Basics: Variables", "Programming"));
        courses.add(new Course("java3", "Java OOP Concepts", "Programming"));
        courses.add(new Course("java4", "Python for AI", "Data Science"));
        courses.add(new Course("java5", "HTML & CSS Masterclass", "Web Dev"));
        
        model.addAttribute("courses", courses);
        return "home"; // Loads home.html
    }

    // 2. ABOUT PAGE (Project Vision)
    @GetMapping("/about")
    public String showAbout() {
        return "about"; // Loads about.html
    }

    // 3. DASHBOARD (The AI Player)
    @GetMapping("/watch")
    public String showPlayer(@RequestParam String id, @RequestParam String title, Model model) {
        model.addAttribute("videoId", id);
        model.addAttribute("videoTitle", title);
        return "dashboard"; // Loads dashboard.html
    }
}