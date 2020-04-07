import string
import os
import xml.etree.ElementTree as ET
BASE_DIR=os.getcwd()
test_set_php=open("load_test_set.php", "w")
test_set_php_base='''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title></title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <script
    src="http://code.jquery.com/jquery-3.1.1.js"
    integrity="sha256-16cdPddA6VdVInumRGo6IbivbERE8p7CQR3HzTBuELA="
    crossorigin="anonymous"></script>  <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
  </head>

  <body>
<!--All PHP SCRIP should be here########### -->
<?php
function Load_Test_Set()
{
  echo "load_test_set.php";
}
function TA_CGNAT_CONSUMER()
{
echo "http://google.com";
}
function TA_CGNAT_RESELLER()
{
exec('python /var/www/html/test.py');
}
function TA_NGINX_LB()
{
exec('python /var/www/html/test.py');
}
function TA_OAM_FW()
{
exec('python /var/www/html/test.py');
}
?>



  	<!-- DOCUMENTATION NAVBAR -->

  	<nav class="navbar navbar-default navbar-inverse navbar-fixed-top">

      <!-- Inside of a Container -->
    <div class="container-fluid">

      <!-- Brand and toggle get grouped for better mobile display -->
      <!-- This is the actual code that create the "hamburger icon" -->
      <!-- The data-target grabs ids to put into the icon -->
      <div class="navbar-header">
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">

          <!--  Code for the hamburger icon-->
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>

        <a class="navbar-brand" href="index.php">Home</a>
      </div>

      <!-- Anything inside of collapse navbar-collapse goes into the "hamburger" -->

      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav">
          <!-- <li class="active"><a href="#">Dashboards<span class="sr-only">(current)</span></a></li>
          <li><a href="#">Cloud VNFs</a></li> -->
      <!-- ####################Dashboards drop down starts here################### -->
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Test Automation <span class="caret"></span></a>
            <ul class="dropdown-menu">
              <li><a href='<?php Load_Test_Set(); ?>'>Load Test Set</a></li>
<!--              <li><a href='<?php TA_CGNAT_RESELLER(); ?>'>CGNAT-RESELLER</a></li>
              <li><a href='<?php TA_NGINX_LB(); ?>'>NGINX-LB</a></li>
              <li><a href='<?php TA_OAM_FW(); ?>'>OAM-FW</a></li>
-->          </ul>


            <!-- ####################Dashboards drop down stops here################### -->


      <!-- ####################VNFss drop down starts here################### -->
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Traffic Generator <span class="caret"></span></a>
            <ul class="dropdown-menu">
              <li><a href='<?php TA_CGNAT_CONSUMER(); ?>'>CGNAT-CONSUMER</a></li>
              <li><a href='<?php TA_CGNAT_RESELLER(); ?>'>CGNAT-RESELLER</a></li>
              <li><a href='<?php TA_NGINX_LB(); ?>'>NGINX-LB</a></li>
              <li><a href='<?php TA_OAM_FW(); ?>'>OAM-FW</a></li>
          </ul>

      <!-- ####################VNFs drop down stops here################### -->

            <!-- ####################Clouds drop down starts here################### -->
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Packet Capture <span class="caret"></span></a>
            <ul class="dropdown-menu">
              <li><a href='<?php TA_CGNAT_CONSUMER(); ?>'>CGNAT-CONSUMER</a></li>
              <li><a href='<?php TA_CGNAT_RESELLER(); ?>'>CGNAT-RESELLER</a></li>
              <li><a href='<?php TA_NGINX_LB(); ?>'>NGINX-LB</a></li>
              <li><a href='<?php TA_OAM_FW(); ?>'>OAM-FW</a></li>
          </ul>
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">CLI Executer<span class="caret"></span></a>
            <ul class="dropdown-menu">
              <li><a href='<?php TA_CGNAT_CONSUMER(); ?>'>CGNAT-CONSUMER</a></li>
              <li><a href='<?php TA_CGNAT_RESELLER(); ?>'>CGNAT-RESELLER</a></li>
              <li><a href='<?php TA_NGINX_LB(); ?>'>NGINX-LB</a></li>
              <li><a href='<?php TA_OAM_FW(); ?>'>OAM-FW</a></li>
          </ul>

            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Admin<span class="caret"></span></a>
              <ul class="dropdown-menu">
                    <li><a href="cloud6-vnfs.html">Add or Modify Test Library</a></li>
                    <li><a href="cloud7-vnfs.html">Add or Modify DUT</a></li>
                    <li><a href="cloud8-vnfs.html">Add or Modify APN</a></li>
              </ul>
      <!-- ####################Clouds drop down starts here################### -->

  <!-- ############################################ -->
<!--          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Server ILOs <span class="caret"></span></a>
            <ul class="dropdown-menu">
              <li><a href="cloud6-ilo.html">Cloud6</a></li>
              <li><a href="cloud7-ilo.html">Cloud7</a></li>
              <li><a href="cloud8-ilo.html">Cloud8</a></li>
            </ul>
-->
              <!-- Use this to separate a new link -->
  <!-- ############################################ -->


  <!-- ####################VNFss drop down starts here################### -->
      <!-- <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Router/Switches <span class="caret"></span></a>
        <ul class="dropdown-menu">
              <li><a href="ss.html">Spine Switch</a></li>
              <li><a href="ls1.html">Leaf Switch11</a></li>
              <li><a href="ls2.html">Leaf Switch12</a></li>
        </ul> -->
  <!-- ####################VNFs drop down stops here################### -->
<!--  <li class="nav navbar-nav"><a href="router-switch.html">Router/Switches</a></li>
  <li class="nav navbar-nav"><a href="kvm.html">KVMs</a></li>
-->
            <!-- <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a> -->
          <!-- ############################################ -->


  </ul>

        <!-- SEARCH BAR -->
<!--        <form class="navbar-form navbar-left" role="search">
          <div class="form-group">
            <input type="text" class="form-control" placeholder="Search">
          </div>
          <button type="submit" class="btn btn-default">Submit</button>
        </form>
-->

        <!-- Stuff on the Right -->
        <ul class="nav navbar-nav navbar-right">
          <li><a href="https://1drv.ms/x/s!AukKJgnzL8rjbgB_EH3dtcAkKS8" target="_blank">Help</a></li>
        </ul>

      </div><!-- /.navbar-collapse -->
    </div><!-- /.container-fluid -->
  </nav>
    <div class="container">
      <div class="jumbotron">
       <center>
       <br>
       <h2>Select Test Set to Run</h2>
       <br><br>
'''
test_set_php.write(test_set_php_base)
test_set_ls=os.system("ls -l Test_Set/ | grep FULL")
test_set_no=test_set_ls.split("\n")
for test_set in test_set_no:
        print test_set.split(" ")[8].split("FULL")[0]
#        test_set_php.write()

#         <button><h4>CGNAT_CONSUMER</h4></button>
#         <button><h4>CGNAT_RESELLER</h4></button>
#         <button><h4>NGINX_LB</h4></button>
#         <button><h4>OAM_FW</h4></button>
