<!DOCTYPE html>
<html>
<head>
 <title>Impact data</title>
<style>
  table {
   border-collapse: collapse;
   width: 100%;
   color: #000000;
   font-family: monospace;
   font-size: 20px;
   text-align: center;
     } 
  th {
   background-color: #588c7e;
   color: white;
    }
  tr:nth-child(even) {background-color: #f2f2f2}
 </style>
</head>
<body>
 <table>
 <tr>
  <th>time</th>
  <th>pincode</th> 
  <th>latitude</th> 
  <th>longitude</th>
  <th>severity</th>
  <th>google_maps</th>
 </tr>
 <?php
$conn = mysqli_connect("localhost", "root", "", "accident_inf");
  // Check connection
  if ($conn->connect_error) {
   die("Connection failed: " . $conn->connect_error);
  } 
  $sql = "SELECT time,pincode,latitude,longitude,severity,google_maps FROM severity_data";
  $result = $conn->query($sql);
  if ($result->num_rows > 0) {
   // output data of each row
   while($row = $result->fetch_assoc()) {
    echo "<tr> <td>" . $row["time"] . "</td> <td>" . $row["pincode"] . "</td> <td>" . $row["latitude"] . "</td> <td>" . $row["longitude"] . "</td> <td>"  . $row["severity"] . "</td> <td>". $row["google_maps"] . "</td></tr>";
}
echo "</table>";
} else { echo "0 results"; }
$conn->close();
?>
</table>
</body>
</html>