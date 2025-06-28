<?php
session_start();
if(!isset($_SESSION['userId']) && empty($_SESSION['userId'])){
    header('location:login');
    die();
}
include('../include/con.php');
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <title>Edit Profile</title>
    <?php
    include('../partials/_links.php')
    ?>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

    <style>
        .btn-secondary {
            color: white;
        }

        #cancelBtn {
            display: none;
        }
    </style>
    <style>
        .select2-container .select2-selection--single {
            box-sizing: border-box;
            cursor: pointer;
            padding: 1%;
            display: block;
            height: 37px;
            user-select: none;
            -webkit-user-select: none;
        }

        .select2-container--default .select2-selection--multiple .select2-selection__choice {
            font-size: 1rem;
        }
        .eye-toggle {
    cursor: pointer;
}


        .task {
            display: none;
        }

        .required {
            color: red;
        }
    </style>
    <!--<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>-->
    <script>
        $(document).ready(function () {
        });
    </script>
</head>

<body>
    <div class="container-scroller">

        <?php
        include('../partials/_navbar.php')
        ?>

        <div class="container-fluid page-body-wrapper">

            <?php 
            include('../partials/_sidebar.php');
            include('../partials/_settings-panel.php');
            ?>

            <div class="main-panel">
                <div class="content-wrapper">
                    <div class="row">
                        <div class="col-12 grid-margin stretch-card">
                            <div class="card">
                                <div class="card-body">
                                    <h4 class="card-title" id="pageTitle">Edit Profile</h4>

                                    <form class="forms-sample" action="editProfile_db" method="post"
                                        enctype="multipart/form-data">
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="row">

                                                    <div class="col-md-12">
                                                        <center>
                                                            <img src="../profile-photos/<?php echo $result['profilePhoto']; ?>"
                                                                style="width:15%;border-radius:50%;">
                                                        </center>
                                                    </div>
                                                    <div class="form-group col-md-12">
                                                        <label id="profileImage">Choose Profile Image</label>
                                                        <input type="file" class="file-upload-default" name="upload" id="imageUpload">
                                                        <div class="input-group col-xs-12">
                                                            <input type="text" class="form-control file-upload-info"
                                                                disabled="" placeholder="Upload Image">
                                                            <span class="input-group-append">
                                                                <button class="file-upload-browse btn btn-primary"
                                                                    type="button">Upload</button>
                                                            </span>
                                                        </div>
                                                    </div>

                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label for="fullName">Full Name</label>
                                                            <input type="text" class="form-control" name="fullName" id="fullName" value="<?php echo $result['fullName'] ?>">
                                                        </div>
                                                    </div>

                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label for="email">Email</label>
                                                            <input type="text" class="form-control" name="email" id="email" value="<?php echo $result['email'] ?>">
                                                        </div>
                                                    </div>

                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label for="username">Username</label>
                                                            <input type="text" class="form-control" name="username" id="username" value="<?php echo $result['username'] ?>">
                                                        </div>
                                                    </div>

                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label for="password">Password</label>
                                                           <div class="input-group">
    <input type="password" class="form-control" name="password" id="password" value="<?php echo $result['password'] ?>">
    <div class="input-group-append">
        <span class="input-group-text eye-toggle">
            <i class="fa fa-eye" id="togglePassword"></i>
        </span>
    </div>
</div>


                                                        </div>
                                                    </div>
                                                </div>
                                                <button type="submit" id="submitBtn" class="btn btn-primary mr-2"
                                                    name="update">Update</button>
                                            </div>
                                            <div class="col-md-6">
                                                <center>
                                                    <img src="../images/edit_profile.png" style="width:90%;">
                                                </center>
                                            </div>

                                        </div>

                                        <a href="projectMaster" id="cancelBtn">
                                            <button type="button" class="btn btn-dark">Cancel</button>
                                        </a>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

<script>
document.getElementById('imageUpload').addEventListener('change', function(e) {
    var file = this.files[0];
    if (file) {
        var fileName = file.name;
        var ext = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
        if (ext === 'jpeg' || ext === 'jpg' || ext === 'png') {
            // Valid file extension
            // You can provide feedback to the user if needed
        } else {
            alert('Please select a JPEG or PNG image file.');
            // Optionally, you can clear the file input value to allow the user to select another file
            this.value = ''; // Clear file input value
        }
    }
});
</script>

    <script src="../vendors/js/vendor.bundle.base.js"></script>


    <script src="../vendors/typeahead.js/typeahead.bundle.min.js"></script>
    <script src="../vendors/select2/select2.min.js"></script>
    <script src="../js/template.js"></script>
    <script src="../js/settings.js"></script>
    <script src="../js/select2.js"></script>
    <script src="../js/file-upload.js"></script>

    <!-- Date picker script -->
    <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
    <!-- Date picker script end -->

    <!-- This page script -->

    <!-- This page script end -->

    <!-- Data Table Script Link -->
    <script src="../vendors/datatables.net/jquery.dataTables.js"></script>
    <script src="../vendors/datatables.net-bs4/dataTables.bootstrap4.js"></script>
    <!-- Data Table Script Link End -->
    
    
    <!-- plugins:js -->
	<script src="../vendors/js/vendor.bundle.base.js"></script>
	<!-- endinject -->
	<!-- Plugin js for this page -->
	<script src="../vendors/chart.js/Chart.min.js"></script>
	<script src="../vendors/datatables.net/jquery.dataTables.js"></script>
	<script src="../vendors/datatables.net-bs4/dataTables.bootstrap4.js"></script>
	<script src="../js/dataTables.select.min.js"></script>

	<!-- End plugin js for this page -->
	<!-- inject:js -->
	<script src="../js/off-canvas.js"></script>
	<script src="../js/hoverable-collapse.js"></script>
	<script src="../js/template.js"></script>
	<script src="../js/settings.js"></script>
	<script src="../js/todolist.js"></script>
	<!-- endinject -->
	<!-- Custom js for this page-->
	<script src="../js/dashboard.js?v=<?php echo time(); ?>"></script>
	<script src="../js/Chart.roundedBarCharts.js"></script>
	<!-- End custom js for this page-->
    <script>
        flatpickr(".js-datepicker", {
            enableTime: true,
            dateFormat: "d-m-Y H:i",
            minDate: "<?php echo date('d-m-Y H:i') ?>"
            // minTime: ""
        });

        window.addEventListener('onbeforeunload', function (e) {
            status = document.getElementById("body").value;
            if (status == "running") {
                e.preventDefault();
                e.returnValue = '';
            }
        })



        $("#projectId").on("change", function () {
            var projectId = $("#projectId").val();

            $.ajax({
                type: 'POST',
                url: '../ajax/taskEntry',
                data: { projectId: projectId },
                success: function (result) {
                    console.log(result);
                    $("#task").html(result);
                }
            });
        });

        $(".remov option").each(function () {
            $(this).siblings('[value="' + this.value + '"]').remove();
        });
    </script>

   <script>
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');

    togglePassword.addEventListener('click', function () {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });
</script>


    
    
    <?php
    require_once('../include/sweetAlert.php');
    if(isset($_SESSION['status'])){
        $status = $_SESSION['status'];
        $msg = $_SESSION['msg'];
        if($status != true){
            toastMsg('error', $msg);
        } else {
            toastMsg('success', $msg);
        }
        unset($_SESSION['status']);
        unset($_SESSION['msg']);
    }
    ?>
</body>

</html>