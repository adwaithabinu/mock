<!DOCTYPE html>
<html lang="en">
<head>
    <title>Employee Salary</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 20px;
            text-align: center;
        }

        h1 {
            font-family: 'Arial', sans-serif;
            font-size: 36px;
            color: #333;
        }

        p {
            font-size: 20px;
            color: #444;
        }
    </style>
</head>
<body>
    <h1>Employee Salary Status</h1>
    <?php
    $employee_id = $_GET["employee_id"];
    $new_salary = $_GET["new_salary"];
    $action = $_GET["action"];
    $conn = mysqli_connect("localhost", "root", "");

    if (!$conn) {
        die('Connection to MySQL database engine/server Failed : ' . mysqli_connect_error());
    }

    $db = "db_employee";
    $db_selection_status = mysqli_select_db($conn, $db);

    if (!$db_selection_status) {
        die("Can't establish a connection to the Database $db: " . mysqli_error());
    }

    $sql = "SELECT * FROM tb_employee WHERE emp_id = $employee_id";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        $row = $result->fetch_assoc();
        $current_salary = $row["salary"];

        if ($action == "increment") {
            $new_salary = $current_salary + $new_salary;
        } else if ($action == "decrement") {
            $new_salary = $current_salary - $new_salary;
        }

        $sql = "UPDATE tb_employee SET salary = $new_salary WHERE emp_id = $employee_id";
        if ($conn->query($sql) === TRUE) {
            echo "<p>Salary updated successfully.</p>";
            echo "<h2>Employee Details</h2>";
            echo "<p>Employee ID: " . $row["emp_id"] . "</p>";
            echo "<p>Name: " . $row["emp_name"] . "</p>";
            echo "<p>Old Salary: ₹" . $current_salary . "</p>";
            echo "<p>New Salary: ₹" . $new_salary . "</p>";
        } else {
            echo "<p>Error updating salary: " . $conn->error . "</p>";
        }
    } else {
        echo "<p>Employee not found.</p>";
    }

    $connection_close_status = mysqli_close($conn);

    if (!$connection_close_status) {
        echo "<p>Connection to MySQL database engine is not closed</p>";
    }
    ?>
</body>
</html>