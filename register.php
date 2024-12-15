<?php
// Include config file
require_once "config.php";
 
// Define variables and initialize with empty values
$username = $email = $phone_no = $dob = $password = $confirm_password = "";
$username_err = $email_err = $phone_no_err = $dob_err = $password_err = $confirm_password_err = "";
 
// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST"){
 
    
    // Validate username
    if(empty(trim($_POST["username"]))){
        $username_err = "Please enter a username.";
    } else{
        // Prepare a select statement
        $sql = "SELECT id FROM registration WHERE username = ?";
        
        if($stmt = mysqli_prepare($link, $sql)){
            // Bind variables to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "s", $param_username);
            
            // Set parameters
            $param_username = trim($_POST["username"]);
            
            // Attempt to execute the prepared statement
            if(mysqli_stmt_execute($stmt)){
                /* store result */
                mysqli_stmt_store_result($stmt);
                
                if(mysqli_stmt_num_rows($stmt) == 1){
                    $username_err = "This username is already taken.";
                } else{
                    $username = trim($_POST["username"]);
                }
            } else{
                echo "Oops! Something went wrong. Please try again later.";
            }

            // Close statement
            mysqli_stmt_close($stmt);
        }
    }

// Validate email
if(empty(trim($_POST["email"]))){
    $email_err = "Please enter a email.";
} else{
    // Prepare a select statement
    $sql = "SELECT id FROM registration WHERE email = ?";
    
    if($stmt = mysqli_prepare($link, $sql)){
        // Bind variables to the prepared statement as parameters
        mysqli_stmt_bind_param($stmt, "s", $param_email);
        
        // Set parameters
        $param_email = trim($_POST["email"]);
        
        // Attempt to execute the prepared statement
        if(mysqli_stmt_execute($stmt)){
            /* store result */
            mysqli_stmt_store_result($stmt);
            
            if(mysqli_stmt_num_rows($stmt) == 1){
                $email_err = "This email is already taken.";
            } else{
                $email = trim($_POST["email"]);
            }
        } else{
            echo "Oops! Something went wrong. Please try again later.";
        }

        // Close statement
        mysqli_stmt_close($stmt);
    }
}
// Validate phone_no
if(empty(trim($_POST["phone_no"]))){
    $phone_no_err = "Please enter a phone number.";
} else{
    // Prepare a select statement
    $sql = "SELECT id FROM registration WHERE phone_no = ?";
    
    if($stmt = mysqli_prepare($link, $sql)){
        // Bind variables to the prepared statement as parameters
        mysqli_stmt_bind_param($stmt, "s", $param_phone_no);
        
        // Set parameters
        $param_phone_no = trim($_POST["phone_no"]);
        
        // Attempt to execute the prepared statement
        if(mysqli_stmt_execute($stmt)){
            /* store result */
            mysqli_stmt_store_result($stmt);
            
            if(mysqli_stmt_num_rows($stmt) == 1){
                $phone_no_err = "This phone number is already taken.";
            } else{
                $phone_no = trim($_POST["phone_no"]);
            }
        } else{
            echo "Oops! Something went wrong. Please try again later.";
        }

        // Close statement
        mysqli_stmt_close($stmt);
    }
}    
    // Validate dob
    if(empty(trim($_POST["dob"]))){
        $dob_err = "Please enter a dob.";     
    }else{
        $dob = trim($_POST["dob"]);
    }

    // Validate password
    if(empty(trim($_POST["password"]))){
        $password_err = "Please enter a password.";     
    } elseif(strlen(trim($_POST["password"])) < 6){
        $password_err = "Password must have atleast 6 characters.";
    } else{
        $password = trim($_POST["password"]);
    }
    
    // Validate confirm password
    if(empty(trim($_POST["confirm_password"]))){
        $confirm_password_err = "Please confirm password.";     
    } else{
        $confirm_password = trim($_POST["confirm_password"]);
        if(empty($password_err) && ($password != $confirm_password)){
            $confirm_password_err = "Password did not match.";
        }
    }


    
    
    // Check input errors before inserting in database
    if(empty($username_err) && empty($email_err) && empty($phone_no_err) && empty($dob_err) && empty($password_err) && empty($confirm_password_err)  ){
        
        // Prepare an insert statement
        $sql = "INSERT INTO registration (username, email, phone_no, dob, password ) VALUES (?, ?, ?, ?, ?)";
         
        if($stmt = mysqli_prepare($link, $sql)){
            // Bind variables to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "sssss", $param_username, $param_email, $param_phone_no, $param_dob, $param_password );
            
            // Set parameters
            $param_username = $username;
            $param_email = $email;
            $param_phone_no = $phone_no;
            $param_dob = $dob;
            $param_password = password_hash($password, PASSWORD_DEFAULT); // Creates a password hash
            
            // Attempt to execute the prepared statement
            if(mysqli_stmt_execute($stmt)){
                // Redirect to login page
                header("location: main.php");
            } else{
                echo "Oops! Something went wrong. Please try again later.";
            }

            // Close statement
            mysqli_stmt_close($stmt);
        }
    }
    
    // Close connection
    mysqli_close($link);
}
?>
 
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="UTF-8">
    <title>MEDICHECK</title>
    <link rel="icon" type="image/x-icon" href="img/1.png"/>
    <link rel="stylesheet" href="./form/rstyle.css">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <div class="medi">
<img src="./img/2.png" href="#" alt="icon" width="35" height="35">
            <a href="#" class="logo">medicheck</a>
</div>
   </head>
<body>
  <div class="container">
    <div class="title">Registration</div>
    <div class="content">

        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
        <div class="user-details">
                   
        <div class="input-box">
                <label>Username</label>
                <input type="text" name="username" class="details <?php echo (!empty($username_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                <span class="invalid-feedback"><?php echo $username_err; ?></span>
            </div> 
            <div class="input-box">
                <label>Email</label>
                <input type="text" name="email" class="details <?php echo (!empty($email_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $email; ?>">
                <span class="invalid-feedback"><?php echo $email_err; ?></span>
            </div>
            <div class="input-box">
                <label>Phone number</label>
                <input type="text" name="phone_no" class="details <?php echo (!empty($phone_no_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $phone_no; ?>">
                <span class="invalid-feedback"><?php echo $phone_no_err; ?></span>
            </div>   
            <div class="input-box">
                <label>Date Of Birth</label>
                <input type="date" name="dob" class="input-text" required>
</div>
            <div class="input-box">
                <label>Password</label>
                <input type="password" name="password" class="details <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $password; ?>">
                <span class="invalid-feedback"><?php echo $password_err; ?></span>
            </div>
            <div class="input-box">
                <label>Confirm Password</label>
                <input type="password" name="confirm_password" class="details <?php echo (!empty($confirm_password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $confirm_password; ?>">
                <span class="invalid-feedback"><?php echo $confirm_password_err; ?></span>
            </div>
</div>
<div class="button">
          <input type="submit" value="Register">
        </div>
        <div class="log">
        <p>Already have an account? <a href="login.php" style="color: #fff;">Login here</a></p>
</div>
        </form>
    </div> 
</div>   
</body>
</html>