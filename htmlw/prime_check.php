<!DOCTYPE html>
<html>
<head>
    <title>Prime or Not Checker Result</title>
    <style>
        body {
            background-color: #ADD8E6; /* Unique background color */
        }
    </style>
</head>
<body>
    <h2>Prime or Not Checker Result</h2>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $number = $_POST["number"];
        $isPrime = isPrime($number);

        if ($isPrime) {
            echo "<p>$number is a prime number.</p>";
        } else {
            echo "<p>$number is not a prime number.</p>";
        }
    }

    function isPrime($n) {
        if ($n <= 1) {
            return false;
        }
        for ($i = 2; $i * $i <= $n; $i++) {
            if ($n % $i == 0) {
                return false;
            }
        }
        return true;
    }
    ?>
</body>
</html>
