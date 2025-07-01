<?php
// PHP Example: example.php

// 1. Critical: SQL Injection Vulnerability (Direct use of GET parameter in query)
$user_id = $_GET['id']; // NO SANITIZATION
$conn = new mysqli("localhost", "user", "password", "database");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error); // Poor error handling
}
$sql = "SELECT * FROM users WHERE id = " . $user_id; // VULNERABLE TO SQL INJECTION
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "User: " . $row["username"]. "<br>";
    }
} else {
    echo "0 results";
}

// 2. High: Sensitive Data Exposure (Hardcoded credentials)
define("DB_PASS", "MySecretPassword123"); // Hardcoded sensitive data

// 3. Medium: Insecure Use of eval()
$code = $_POST['code_to_execute'] ?? 'echo "No code provided";';
eval($code); // Dangerous function, allows arbitrary code execution

// 4. Low: Missing Semicolon (Syntax error - often caught by PHP itself but good to show a linter finding)
$name = "John Doe" // Missing semicolon

// 5. Best Practice: Direct output without escaping (Potential XSS if used in HTML context)
$search_query = $_GET['q'];
echo "You searched for: " . $search_query; // No HTML escaping (e.g., htmlspecialchars)

// 6. Performance/Maintainability: Unused variable
$unused_variable = "This is never used";

// 7. Security: Use of old, insecure hashing function
$password = "testpass";
$hashed_password = md5($password); // MD5 is cryptographically weak

$conn->close();
?>