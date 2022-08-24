<!DOCTYPE html>
<html>
<head>
	<title>Search Bar using PHP</title>
</head>
<body>

<form method="post">
<label>Search</label>
<input type="text" name="search">
<input type="submit" name="submit">
	
</form>

</body>
</html>

<?php

$con = new PDO("mysql:host=localhost;dbname=ahmkhalaf_app_database",'ahmkhalaf','ARNAS');

if (isset($_POST["submit"])) {
	$str = $_POST["shows"];
	$sth = $con->prepare("SELECT * FROM `shows` WHERE ShowName = '$str'");

	$sth->setFetchMode(PDO:: FETCH_OBJ);
	$sth -> execute();

	if($row = $sth->fetch())
	{
		?>
		<br><br><br>
		<table>
			<tr>
				<th>ShowName</th>
				<th>ShowDescription</th>
			</tr>
			<tr>
				<td><?php echo $row->ShowName; ?></td>
				<td><?php echo $row->ShowDescription;?></td>
			</tr>

		</table>
<?php 
	}
		
		
		else{
			echo "Show Does not exist";
		}


}

?>